#!/usr/bin/env bash
#
# Arcobaleno Research — prepare a fresh, single-engagement audit box.
# fctools v1 · sha256 c7c97a6ba3d1a90170e39b0018e60dc805d99173c6577deaec1981bbfbdbc770 · generated 2026-09-14
#
# READ THIS BEFORE RUNNING IT. Do not pipe it into a shell. Download it, read it, then run it.
# A forensics practice that tells clients to check their inputs does not curl|bash its own.
#
#   curl -fsSLO https://arcobaleno.cloud/tools/bootstrap.sh
#   less bootstrap.sh
#   bash bootstrap.sh
#
# WHAT THIS BOX IS: one client, one engagement, destroyed on delivery.
# WHAT MUST NEVER BE ON IT: no deploy key, no exchange credentials, no research registry, no
# route back to the research box. If this machine is fully compromised the attacker gets the
# client's data and nothing of ours — that property is the entire point, and it is only true if
# nothing of ours is ever copied here.
# NO SNAPSHOTS AND NO BACKUPS, at any point. A snapshot is a copy that outlives the destruction
# promised to the client.
set -euo pipefail

# ---------------------------------------------------------------------------------------------
# BEFORE YOU RUN THIS: check the WANT= line below against the hash recorded in YOUR OWN copy --
# the engagement file, or DEPLOY.md "Published bundles" in the research repo. Do NOT take this
# value on trust just because it came from the website.
#
# Why: this script and the tarball are served from the SAME host. Anyone who could substitute
# the tarball could substitute this line too, and the check would verify the artifact against a
# value they also control. The hash is only meaningful when its authority sits somewhere the
# web host does not reach. That is a written step you perform, not something a script can do
# for itself.
# ---------------------------------------------------------------------------------------------
URL="https://arcobaleno.cloud/tools/fctools-v1.tar.gz"
WANT="c7c97a6ba3d1a90170e39b0018e60dc805d99173c6577deaec1981bbfbdbc770"

echo "==> python3 and the two libraries the instruments need"
if command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update -qq
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq python3 python3-pip python3-numpy python3-pandas
else
  echo "    not a Debian/Ubuntu box — install python3, numpy and pandas yourself, then re-run."
fi

echo "==> fetching fctools v1"
curl -fsSL "$URL" -o fctools.tar.gz

echo "==> verifying against the published hash"
GOT="$(sha256sum fctools.tar.gz | cut -d' ' -f1)"
if [ "$GOT" != "$WANT" ]; then
  echo "    HASH MISMATCH — STOPPING."
  echo "      expected $WANT"
  echo "      got      $GOT"
  echo "    Do not use this copy. Re-download; if it still differs, say so before going further."
  exit 1
fi
echo "    ok  $GOT"

tar xzf fctools.tar.gz && rm -f fctools.tar.gz

echo "==> running the toolkit's own self-test"
echo "    If an instrument cannot find its own planted bug, nothing it says about client code is"
echo "    safe to send. This is the gate, not a formality."
python3 fctools/selftest_all.py

cat <<'EOF'

==> ready.

    Next, in this order:

    1. Bring the client's material DIRECTLY here. Not via your laptop, never via the research
       box. Either give them an SFTP account on this machine, or curl their link from here.
    2. Record a sha256 of every file on arrival, before opening any of it. That hash is what the
       report's reproducibility claim is anchored to.
    3. FC-1 first — python3 fctools/fc1_reproduce.py --cmd "<their command>".
       If the headline number will not come out twice, stop and report that. Everything
       downstream is worthless until it does, and this is the natural stop-and-report point.
    4. Work the rest of the checks in ../PLAYBOOK.md order.

    On delivery: destroy this instance and write the date in the engagement file.

EOF
