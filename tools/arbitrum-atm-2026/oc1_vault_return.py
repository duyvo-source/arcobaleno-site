"""OC-1: what did one share of a vault earn? Rebuilt from the vault contract itself, at past blocks.

Works for standard vaults (ERC-4626: Morpho, Euler, Yearn v3, most curators) and for async vaults (ERC-7540,
e.g. Lagoon), on the chains in ocrpc.CHAINS. The return is the change
in the value of one share, in the vault's own asset (USDC vault -> USDC, not dollars), so fees taken by
the vault are already netted out and no price data is needed.

Prints findings, not a number to interpret:
  DROP         the share value fell on some step (a loss the depositors took)
  JUMP         one step carries more than a quarter of the period's whole return
  MISMATCH     the vault's own per-share answer disagrees with its totals (assets / shares)
  THIN         under 90 days of history
  LATE START   the vault did not exist yet at the requested start date
  SHRANK       money in the vault fell >90% from its peak (context only: share value can still be fine)
  STALE        the share value did not change for more than 14 days in a row
  REPORTED VALUE  async vault: the share value is a valuation someone submits, so reading it from the chain
               confirms what was reported, not what the positions were worth
  ENDPOINTS DISAGREE / SOURCES DISAGREE  a second endpoint or the protocol's own series reads differently

What it does NOT do: depositor-level anything (we never read who deposited), off-chain legs, prices, or
the valuation behind an async vault's share price (that needs the fund-level tool, scope phases 2-4).
See ../ONCHAIN_REBUILD_SCOPE.md.

  python3 oc1_vault_return.py --vault 0x... --chain base --start 2025-01-01 --end 2025-12-31 [--step 1]
  python3 oc1_vault_return.py --selftest
"""
import argparse
import csv
import datetime as dt
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ocrpc import Rpc, RpcError, IFACE, endpoint, word_int, word_addr, decode_string  # noqa: E402

VERSION = "oc1 0.2 (2026-10-06, phase 1: chains, async vaults, second endpoint)"
PROBE_SHARES = 10**6  # read the value of a million shares, so 6-decimal assets keep ~12 significant digits
MOVE_EPS = 1e-12      # relative change smaller than this is no change (we read a million shares)
DROP_EPS = 1e-6       # a fall under 0.0001% is listed, not flagged: Syntropia (10-06) had real falls of 2e-7
JUMP_SHARE = 0.25
MISMATCH_TOL = 1e-3   # pending fee shares make a small gap normal (Morpho mints fees lazily)
THIN_DAYS = 90
STALE_DAYS = 14
RPC2_SAMPLES = 12     # dates re-read from the second endpoint (plus every date a finding points at)


def utc_ts(d):
    return int(dt.datetime(d.year, d.month, d.day, tzinfo=dt.timezone.utc).timestamp())


def vault_meta(rpc, vault, block):
    a = rpc.call(vault, "asset()", block)
    if not a or len(a) < 66:
        raise RpcError(f"{vault} has no asset() at block {block}: not a standard (ERC-4626) vault, or not deployed yet")
    asset = word_addr(a)
    vdec = word_int(rpc.call(vault, "decimals()", block))
    adec = word_int(rpc.call(asset, "decimals()", block))
    vsym = decode_string(rpc.call(vault, "symbol()", block) or "0x")
    asym = decode_string(rpc.call(asset, "symbol()", block) or "0x")
    meta = {"asset": asset, "vault_decimals": vdec, "asset_decimals": adec, "vault_symbol": vsym, "asset_symbol": asym}
    # async (ERC-7540)? A plain vault reverts on supportsInterface, which call() returns as None
    flags = [rpc.call(vault, "supportsInterface(bytes4)", block, IFACE[k]) for k in ("7540deposit", "7540redeem")]
    meta["async"] = any(f and f != "0x" and word_int(f) == 1 for f in flags)
    safe, ver = rpc.call(vault, "safe()", block), rpc.call(vault, "version()", block)
    if meta["async"] and safe and ver and len(safe) >= 66:
        meta["lagoon"] = {"safe": word_addr(safe), "version": decode_string(ver)}
    meta["kind"] = ("async, Lagoon " + meta["lagoon"]["version"]) if "lagoon" in meta else ("async (ERC-7540)" if meta["async"] else "standard (ERC-4626)")
    return meta


def read_point(rpc, vault, meta, block):
    if not rpc.has_code(vault, block):
        return None
    r = rpc.call(vault, "convertToAssets(uint256)", block, PROBE_SHARES * 10**meta["vault_decimals"])
    if r is None or r == "0x":
        return None
    sv = word_int(r) / (PROBE_SHARES * 10**meta["asset_decimals"])
    ta = rpc.call(vault, "totalAssets()", block)
    ts_ = rpc.call(vault, "totalSupply()", block)
    total_assets = word_int(ta) / 10**meta["asset_decimals"] if ta and ta != "0x" else None
    total_supply = word_int(ts_) / 10**meta["vault_decimals"] if ts_ and ts_ != "0x" else None
    return {"share_value": sv, "total_assets": total_assets, "total_supply": total_supply}


def read_series(rpc, vault, start, end, step_days=1, log=None):
    head = rpc.head()
    dates = []
    d = start
    while d <= end:
        dates.append(d)
        d += dt.timedelta(days=step_days)
    end_block = rpc.block_at(utc_ts(dates[-1]), head)
    meta = vault_meta(rpc, vault, end_block)
    rows = []
    for i, d in enumerate(dates):
        b = rpc.block_at(utc_ts(d), head)
        p = read_point(rpc, vault, meta, b)
        if p is not None:
            rows.append({"date": d.isoformat(), "block": b, "block_ts": rpc.block_ts(b), **p})
        if log and (i % 30 == 0 or i == len(dates) - 1):
            log(f"  {d} ({i + 1}/{len(dates)}) rpc calls so far: {rpc.calls}")
            rpc.save()
    rpc.save()
    return meta, dates, rows


def analyse(rows, requested_start, step_days, meta=None):
    meta = meta or {}
    f = {"findings": []}
    if len(rows) < 2:
        f["findings"].append(("THIN", "fewer than two readable dates: nothing to measure"))
        return f
    first, last = rows[0], rows[-1]
    days = (dt.date.fromisoformat(last["date"]) - dt.date.fromisoformat(first["date"])).days
    total = last["share_value"] / first["share_value"] - 1
    f.update(start=first["date"], end=last["date"], days=days, start_value=first["share_value"],
             end_value=last["share_value"], total_return=total, steps=len(rows) - 1,
             annualised=(1 + total) ** (365.25 / days) - 1 if days > 0 and total > -1 else None)

    if first["date"] != requested_start.isoformat():
        f["findings"].append(("LATE START", f"vault not readable before {first['date']} (requested {requested_start}); "
                                            "the return is measured from its first readable date"))
    if days < THIN_DAYS:
        f["findings"].append(("THIN", f"only {days} days of history: too short to say much about a track record"))

    # step changes
    steps = []
    for a, b in zip(rows, rows[1:]):
        steps.append((b["date"], b["share_value"] / a["share_value"] - 1))
    drops = [(d, r) for d, r in steps if r < -DROP_EPS]
    f["tiny_falls"] = [(d, r) for d, r in steps if -DROP_EPS <= r < -MOVE_EPS]
    moved = sum(1 for _, r in steps if abs(r) > MOVE_EPS)
    f["updates"] = moved
    # longest run of steps with no change in share value
    run, best_run, run_end, run_start, cur_start = 0, 0, None, None, None
    for (d, r), prev in zip(steps, rows):
        if abs(r) <= MOVE_EPS:
            if run == 0:
                cur_start = prev["date"]
            run += step_days
            if run > best_run:
                best_run, run_start, run_end = run, cur_start, d
        else:
            run = 0
    f["longest_flat"] = {"days": best_run, "from": run_start, "to": run_end}
    if best_run > STALE_DAYS:
        f["findings"].append(("STALE", f"share value unchanged for {best_run} days ({run_start} to {run_end}): "
                                       "no interest, no revaluation, or a vault that stopped being updated"))
    if meta.get("async"):
        who = (f"; the money sits with the curator address {meta['lagoon']['safe']}, and checking the valuation "
               "means valuing what that address holds (fund-level tool, not built)") if "lagoon" in meta else ""
        f["findings"].append(("REPORTED VALUE", f"async vault: the share value moves only when a submitted valuation is "
                                                f"settled ({moved} updates in the period), so this confirms what was "
                                                f"reported, not what the positions were worth{who}"))
    peak, mdd, mdd_at, peak_at = rows[0]["share_value"], 0.0, None, rows[0]["date"]
    mdd_peak = None
    for r in rows:
        if r["share_value"] > peak:
            peak, peak_at = r["share_value"], r["date"]
        dd = r["share_value"] / peak - 1
        if dd < mdd:
            mdd, mdd_at, mdd_peak = dd, r["date"], peak_at
    f["max_drawdown"] = mdd
    if drops:
        worst = min(drops, key=lambda x: x[1])
        f["findings"].append(("DROP", f"share value fell on {len(drops)} of {len(steps)} steps; worst {worst[1]:.4%} "
                                      f"on the step ending {worst[0]}; deepest fall {mdd:.4%} "
                                      f"(peak {mdd_peak} to {mdd_at})"))
    f["drops"] = drops

    # concentration of the return in a single step (log terms, so steps add up)
    if total > 0:
        best = max(steps, key=lambda x: x[1])
        share = math.log1p(best[1]) / math.log1p(total)
        f["largest_step"] = {"date": best[0], "return": best[1], "share_of_total": share}
        # count only steps where the value moved: an async vault that revalues weekly has ~6 quiet days
        # between updates, and those quiet days must not make each update look like a one-off jump
        if share > JUMP_SHARE and moved >= 30:
            f["findings"].append(("JUMP", f"the step ending {best[0]} ({best[1]:.4%}) carries {share:.0%} of the whole "
                                          "period's return: one day, not a track record. Find out what happened that day"))

    # the vault's per-share answer vs its own totals
    gaps = []
    for r in rows:
        if r["total_assets"] and r["total_supply"]:
            implied = r["total_assets"] / r["total_supply"]
            gaps.append((r["date"], implied / r["share_value"] - 1))
    if gaps:
        g = max(gaps, key=lambda x: abs(x[1]))
        f["max_mismatch"] = {"date": g[0], "gap": g[1]}
        if abs(g[1]) > MISMATCH_TOL:
            f["findings"].append(("MISMATCH", f"on {g[0]} the vault's per-share value and its totals disagree by {g[1]:.3%}; "
                                              "the vault may be reporting something other than what a depositor can redeem"))

    tas = [(r["date"], r["total_assets"]) for r in rows if r["total_assets"] is not None]
    if tas:
        pk = max(tas, key=lambda x: x[1])
        f["assets_peak"], f["assets_end"] = pk, tas[-1]
        if pk[1] > 0 and tas[-1][1] < 0.1 * pk[1]:
            f["findings"].append(("SHRANK", f"money in the vault fell from {pk[1]:,.0f} ({pk[0]}) to {tas[-1][1]:,.0f}; "
                                            "share value is unaffected, but say which period a quoted figure covers"))
    return f


def verify_rpc2(rpc2, vault, meta, rows, f):
    """Re-read a sample of the same blocks from an independent second endpoint. The answers must be identical:
    same block, same contract, same chain. Any difference means one endpoint is serving wrong history."""
    n = len(rows)
    pick = {round(i * (n - 1) / max(RPC2_SAMPLES - 1, 1)) for i in range(min(RPC2_SAMPLES, n))}
    flagged = {d for d, _ in f.get("drops", [])}
    for k in ("largest_step", "max_mismatch"):
        if k in f:
            flagged.add(f[k]["date"])
    pick |= {i for i, r in enumerate(rows) if r["date"] in flagged}
    bad = []
    for i in sorted(pick):
        r = rows[i]
        p = read_point(rpc2, vault, meta, r["block"])
        ts2 = rpc2.block_ts(r["block"])
        if p is None or ts2 != r["block_ts"] or any(p[k] != r[k] for k in ("share_value", "total_assets", "total_supply")):
            bad.append((r["date"], r["block"], r["share_value"], None if p is None else p["share_value"]))
    out = {"checked": len(pick), "endpoint": rpc2.url, "bad": bad,
           "line": f"second endpoint ({rpc2.url}): {len(pick) - len(bad)}/{len(pick)} re-read blocks identical"}
    if bad:
        d, b, ours, theirs = bad[0]
        out["finding"] = ("ENDPOINTS DISAGREE", f"{len(bad)} of {len(pick)} re-read blocks differ, first {d} (block {b}): "
                                                f"{ours} vs {theirs}. One endpoint is serving wrong history: nothing here can be quoted until resolved")
    return out


def report(vault, chain, meta, f, step_days, compare=None):
    L = [f"OC-1 vault return  ·  {VERSION}",
         f"vault  {vault} on {chain}  ({meta['vault_symbol']}, asset {meta['asset_symbol']} {meta['asset']})",
         f"kind   {meta.get('kind', 'standard (ERC-4626)')}"]
    if "start" in f:
        ann = f"{f['annualised']:.3%} a year" if f.get("annualised") is not None else "n/a"
        L += [f"period {f['start']} to {f['end']} ({f['days']} days, {f['steps']} steps of {step_days} day(s), 00:00 UTC)",
              f"one share: {f['start_value']:.8f} -> {f['end_value']:.8f} {meta['asset_symbol']}",
              f"return:    {f['total_return']:.4%} over the period = {ann} (in {meta['asset_symbol']}, after the vault's fees)",
              f"deepest fall in share value: {f['max_drawdown']:.6%}",
              f"value changed on {f['updates']} of {f['steps']} steps; longest unchanged stretch {f['longest_flat']['days']} days"]
        if f.get("tiny_falls"):
            tf = min(f["tiny_falls"], key=lambda x: x[1])
            L.append(f"tiny falls below the {DROP_EPS:.4%} threshold: {len(f['tiny_falls'])} (largest {tf[1]:.6%} on {tf[0]}); listed, not a finding")
        if "max_mismatch" in f:
            L.append(f"largest per-share vs totals gap: {f['max_mismatch']['gap']:.5%} ({f['max_mismatch']['date']})")
    for c in (compare or []):
        L.append(c["line"])
        if c.get("finding"):
            f["findings"].append(c["finding"])
    L.append("")
    if f["findings"]:
        for k, msg in f["findings"]:
            L.append(f"[{k}] {msg}")
    else:
        L.append("[CLEAN] no drop, no single-day jump, no long flat stretch, totals agree, sources agree, enough history.")
    L.append("Not covered: dollar value, off-chain legs, per-depositor results (never read).")
    return "\n".join(L)


# ------------------------------------------------------------------ self-test (simulated chain)

def _selftest():
    import hashlib
    from ocrpc import SEL

    T0 = utc_ts(dt.date(2025, 1, 1)) - 86400 * 30
    HALT_AT, HALT_SECS = 900_000, 7_200  # a two-hour halt: block times are irregular

    def bts(n):
        j = int(hashlib.sha256(str(n).encode()).hexdigest()[:2], 16) % 12
        return T0 + 12 * n + j + (HALT_SECS if n >= HALT_AT else 0)

    HEAD = 3_000_000
    VAULT, ASSET = "0x" + "aa" * 20, "0x" + "bb" * 20

    def enc_int(x):
        return "0x" + format(int(x), "064x")

    def enc_str(s):
        b = s.encode().hex()
        return "0x" + format(32, "064x") + format(len(s), "064x") + b.ljust(64, "0")

    class FakeRpc(Rpc):
        def __init__(self, sv, exists_from=0, mismatch=0.0, assets=lambda t: 5e7, async_=False, lagoon=False, bump=0.0):
            self.sv, self.exists_from, self.mismatch, self.assets = sv, exists_from, mismatch, assets
            self.async_, self.lagoon, self.bump = async_, lagoon, bump  # bump: this endpoint serves values off by that much
            super().__init__("ethereum", url="fake://", cache_path=None, min_interval=0)

        def _post(self, method, params):
            self.calls += 1
            if method == "eth_blockNumber":
                return hex(HEAD)
            n = int(params[-1], 16) if method != "eth_getBlockByNumber" else int(params[0], 16)
            t = bts(n)
            if method == "eth_getBlockByNumber":
                return {"timestamp": hex(t)}
            alive = t >= self.exists_from
            if method == "eth_getCode":
                return "0x60" if alive or params[0] == ASSET else "0x"
            to, data = params[0]["to"], params[0]["data"][2:]
            sel = data[:8]
            if to == ASSET:
                return {SEL["decimals()"]: enc_int(6), SEL["symbol()"]: enc_str("USDC")}[sel]
            if not alive:
                return "0x"
            v = self.sv(t) * (1 + self.bump)
            supply = self.assets(t) / v
            if sel == SEL["supportsInterface(bytes4)"]:
                if not self.async_:
                    raise RpcError("execution reverted")
                return enc_int(int(data[8:16], 16) in (0xce3bbe50, 0x620ee8e4))
            if sel in (SEL["safe()"], SEL["version()"]):
                if not self.lagoon:
                    raise RpcError("execution reverted")
                return "0x" + ("cc" * 20).rjust(64, "0") if sel == SEL["safe()"] else enc_str("v0.5.0")
            if sel == SEL["asset()"]:
                return "0x" + ASSET[2:].rjust(64, "0")
            if sel == SEL["decimals()"]:
                return enc_int(18)
            if sel == SEL["symbol()"]:
                return enc_str("tVAULT")
            if sel == SEL["convertToAssets(uint256)"]:
                shares = int(data[8:], 16)
                return enc_int(shares * v * 10**6 // 10**18)
            if sel == SEL["totalAssets()"]:
                return enc_int(self.assets(t) * (1 + self.mismatch) * 10**6)
            if sel == SEL["totalSupply()"]:
                return enc_int(supply * 10**18)
            raise AssertionError(sel)

    def yearfrac(t):
        return (t - utc_ts(dt.date(2025, 1, 1))) / (365.25 * 86400)

    def day_ts(y, m, d):
        return utc_ts(dt.date(y, m, d))

    def run(name, rpc, start, end, want, step=1, rpc2=None):
        meta, dates, rows = read_series(rpc, VAULT, start, end, step)
        f = analyse(rows, start, step, meta)
        if rpc2 is not None:
            c = verify_rpc2(rpc2, VAULT, meta, rows, f)
            if c.get("finding"):
                f["findings"].append(c["finding"])
        got = {k for k, _ in f["findings"]}
        ok = got == set(want)
        print(f"  {'PASS' if ok else 'FAIL'}  {name:<34} findings={sorted(got) or ['CLEAN']}  want={sorted(want) or ['CLEAN']}")
        return ok, f

    results = []
    S, E = dt.date(2025, 1, 1), dt.date(2025, 12, 31)
    steady = lambda t: 1.05 ** yearfrac(t)  # noqa: E731

    # block search against brute force, including dates across the halt
    rpc = FakeRpc(steady)
    bad = 0
    for k in range(40):
        target = T0 + 86400 + k * 997_331 % (HEAD * 12 - 2 * 86400)
        b = rpc.block_at(target, HEAD)
        if not (bts(b) >= target and (b == 0 or bts(b - 1) < target)):
            bad += 1
    print(f"  {'PASS' if bad == 0 else 'FAIL'}  block-for-date search vs brute force  ({40 - bad}/40 exact)")
    results.append(bad == 0)

    ok, f = run("negative control: steady 5%/yr", FakeRpc(steady), S, E, [])
    results.append(ok and abs(f["annualised"] - 0.05) < 2e-4)
    print(f"        annualised {f['annualised']:.5%} (expect 5.000% +- 0.02%)")

    loss_day = day_ts(2025, 7, 20)
    ok, f = run("planted 2% loss on 2025-07-20", FakeRpc(lambda t: steady(t) * (0.98 if t >= loss_day else 1)), S, E, ["DROP"])
    results.append(ok and f["drops"] and f["drops"][0][0] == "2025-07-20")

    ok, f = run("2e-7 fall is listed, not a DROP", FakeRpc(lambda t: steady(t) * (1 - 2e-7 * (t >= loss_day)) if abs(t - loss_day) > 86400 * 2 or t < loss_day else steady(loss_day - 86400) * (1 - 2e-7)), S, E, [])
    results.append(ok and len(f["tiny_falls"]) == 1)

    jump_day = day_ts(2025, 3, 3)
    ok, _ = run("planted one-day +3% jump", FakeRpc(lambda t: 1.01 ** yearfrac(t) * (1.03 if t >= jump_day else 1)), S, E, ["JUMP"])
    results.append(ok)

    ok, _ = run("only 30 days", FakeRpc(steady), S, dt.date(2025, 1, 31), ["THIN"])
    results.append(ok)

    ok, _ = run("totals disagree by 1%", FakeRpc(steady, mismatch=0.01), S, E, ["MISMATCH"])
    results.append(ok)

    ok, _ = run("tiny gap (0.01%) is not a finding", FakeRpc(steady, mismatch=0.0001), S, E, [])
    results.append(ok)

    ok, f = run("vault deployed 2025-04-10", FakeRpc(steady, exists_from=day_ts(2025, 4, 10) - 3600), S, E, ["LATE START"])
    results.append(ok and f["start"] == "2025-04-10")

    ok, _ = run("money left (share value fine)", FakeRpc(steady, assets=lambda t: 5e7 if yearfrac(t) < 0.5 else 1e6), S, E, ["SHRANK"])
    results.append(ok)

    ok, _ = run("weekly steps, steady", FakeRpc(steady), S, E, [], step=7)
    results.append(ok)

    # phase 1: async vaults, flat stretches, a second endpoint
    WEEK = 7 * 86400
    weekly = lambda t: steady(t - (t - T0) % WEEK)  # noqa: E731  value moves only at weekly settlements
    ok, f = run("async vault, weekly settlements", FakeRpc(weekly, async_=True, lagoon=True), S, E, ["REPORTED VALUE"])
    results.append(ok and "cccc" in dict(f["findings"])["REPORTED VALUE"])

    ok, _ = run("async but not Lagoon", FakeRpc(weekly, async_=True), S, E, ["REPORTED VALUE"])
    results.append(ok)

    gap0, gap1 = day_ts(2025, 6, 1), day_ts(2025, 7, 1)
    ok, _ = run("lending vault flat for 30 days", FakeRpc(lambda t: steady(min(t, gap0)) if t < gap1 else steady(t)), S, E, ["STALE"])
    results.append(ok)

    ok, _ = run("async, no settlement for 30 days", FakeRpc(lambda t: weekly(gap0) if gap0 <= t < gap1 else weekly(t), async_=True), S, E, ["REPORTED VALUE", "STALE"])
    results.append(ok)

    ok, _ = run("second endpoint identical", FakeRpc(steady), S, E, [], rpc2=FakeRpc(steady))
    results.append(ok)

    ok, _ = run("second endpoint off by 0.01%", FakeRpc(steady), S, E, ["ENDPOINTS DISAGREE"], rpc2=FakeRpc(steady, bump=1e-4))
    results.append(ok)

    # few updates in a short window: each carries a big share by construction, which is not a JUMP
    fortnight = lambda t: steady(t - (t - day_ts(2025, 1, 1)) % (14 * 86400))  # noqa: E731
    ok, _ = run("async, 3 settlements in 45 days", FakeRpc(fortnight, async_=True), S, dt.date(2025, 2, 15), ["REPORTED VALUE", "THIN"])
    results.append(ok)

    # the protocol cross-checks, offline: feed them a published series that agrees, then one that does not
    import oc_crosscheck
    meta, _, rows = read_series(FakeRpc(weekly, async_=True, lagoon=True), VAULT, S, E, 1)
    real_gql = oc_crosscheck._gql
    for label, factor, want_finding in (("Lagoon series agrees", 1.0, False), ("Lagoon series 0.1% off", 1.001, True)):
        pts = [{"x": r["block_ts"] - 60, "y": str(int(r["share_value"] * factor * 10**6))} for r in rows]
        oc_crosscheck._gql = lambda url, q, pts=pts: {"vaultByAddress": {"stateHistory": {"pricePerShare": pts}}}
        c = oc_crosscheck.compare_lagoon(VAULT, "ethereum", rows, meta)
        ok = bool(c.get("finding")) == want_finding and c.get("matched_dates") == len(rows)
        print(f"  {'PASS' if ok else 'FAIL'}  {label:<34} finding={'yes' if c.get('finding') else 'no'}")
        results.append(ok)
    for label, factor, want_finding in (("Morpho series agrees", 1.0, False), ("Morpho series 0.01% off", 1.0001, True)):
        pts = [{"x": utc_ts(dt.date.fromisoformat(r["date"])), "y": r["share_value"] * factor} for r in rows]
        oc_crosscheck._gql = lambda url, q, pts=pts: {"vaultByAddress": {"historicalState": {"sharePriceNumber": pts}}}
        c = oc_crosscheck.compare_morpho(VAULT, "ethereum", rows, meta)
        ok = bool(c.get("finding")) == want_finding and c.get("matched_dates") == len(rows)
        print(f"  {'PASS' if ok else 'FAIL'}  {label:<34} finding={'yes' if c.get('finding') else 'no'}")
        results.append(ok)
    oc_crosscheck._gql = real_gql

    n_ok = sum(bool(r) for r in results)
    print(f"OC-1 selftest: {n_ok}/{len(results)} passed")
    return n_ok == len(results)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--vault")
    ap.add_argument("--chain", default="ethereum")
    ap.add_argument("--start")
    ap.add_argument("--end")
    ap.add_argument("--step", type=int, default=1, help="days between readings (default 1)")
    ap.add_argument("--compare", choices=["auto", "morpho", "lagoon", "none"], default="auto",
                    help="cross-check against the protocol's own published series (auto: Lagoon for Lagoon vaults, else Morpho)")
    ap.add_argument("--no-rpc2", action="store_true", help="skip the re-read from the chain's second endpoint")
    ap.add_argument("--out", help="directory for series.csv, report.txt, summary.json (default: print only)")
    ap.add_argument("--cache", help="cache file for chain answers (default: <out>/rpc_cache.json)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(0 if _selftest() else 1)
    if not (a.vault and a.start and a.end):
        ap.error("--vault, --start and --end are required")
    start, end = dt.date.fromisoformat(a.start), dt.date.fromisoformat(a.end)
    if a.out:
        os.makedirs(a.out, exist_ok=True)
    cache = a.cache or (os.path.join(a.out, "rpc_cache.json") if a.out else None)
    rpc = Rpc(a.chain, cache_path=cache)
    print(f"reading {a.vault} on {a.chain} via {rpc.url} ...", file=sys.stderr)
    meta, dates, rows = read_series(rpc, a.vault, start, end, a.step, log=lambda m: print(m, file=sys.stderr))
    f = analyse(rows, start, a.step, meta)
    cmp_ = []
    if not a.no_rpc2:
        if endpoint(a.chain, 1):
            rpc2 = Rpc(a.chain, which=1, cache_path=(cache + ".rpc2") if cache else None)
            cmp_.append(verify_rpc2(rpc2, a.vault, meta, rows, f))
            rpc2.save()
        else:
            cmp_.append({"line": f"second endpoint: none known for {a.chain}, so the chain reading rests on one endpoint "
                                 f"(set ARC_RPC2_{a.chain.upper()})"})
    which = a.compare if a.compare != "auto" else ("lagoon" if "lagoon" in meta else "morpho")
    if which != "none":
        import oc_crosscheck
        cmp_.append(getattr(oc_crosscheck, "compare_" + which)(a.vault, a.chain, rows, meta))
    text = report(a.vault, a.chain, meta, f, a.step, cmp_)
    print(text)
    if a.out:
        with open(os.path.join(a.out, "series.csv"), "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        with open(os.path.join(a.out, "report.txt"), "w") as fh:
            fh.write(text + "\n")
        with open(os.path.join(a.out, "summary.json"), "w") as fh:
            json.dump({"version": VERSION, "vault": a.vault, "chain": a.chain, "rpc": rpc.url, "meta": meta,
                       "step_days": a.step, "rpc_calls": rpc.calls,
                       **{k: v for k, v in f.items() if k != "drops"}, "compare": cmp_}, fh, indent=1, default=str)


if __name__ == "__main__":
    main()
