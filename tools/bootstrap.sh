#!/usr/bin/env bash
#
# Arcobaleno Research — prepare a fresh, single-engagement audit box.
# fctools v4 · sha256 4adc2698b3c2c2d4036a9e81453e7bcea2a3f1ec6ca06701f809b7585b264e99 · generated 2026-09-14
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
URL="https://arcobaleno.cloud/tools/fctools-v4.tar.gz"
WANT="4adc2698b3c2c2d4036a9e81453e7bcea2a3f1ec6ca06701f809b7585b264e99"
FPR="49B5D5935AECA188C6638A08B544B55244F50864"   # signing key fingerprint -- ALSO check this against DEPLOY.md, same reason as WANT

# Fresh cloud images usually log you in as root and often do NOT ship sudo. Calling sudo
# unconditionally aborts this script on its very first command under `set -e`.
SUDO=""
if [ "$(id -u)" -ne 0 ]; then
  if command -v sudo >/dev/null 2>&1; then SUDO="sudo"; else
    echo "Not root, and sudo is not installed. Re-run as root."; exit 1
  fi
fi

echo "==> python3 and venv"
if command -v apt-get >/dev/null 2>&1; then
  $SUDO apt-get update -qq
  $SUDO DEBIAN_FRONTEND=noninteractive apt-get install -y -qq python3 python3-venv gnupg
else
  echo "    not a Debian/Ubuntu box — ensure python3 and the venv module are present, then re-run."
fi

echo "==> fetching fctools v4"
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

echo "==> verifying the signature"
# The hash proves the bytes match a number. The SIGNATURE proves they were produced by whoever
# holds the release key -- which an attacker who controls the web host still does not have.
if command -v gpg >/dev/null 2>&1; then
  curl -fsSL "${URL%/*}/arcobaleno-release-pubkey.asc" -o pubkey.asc
  curl -fsSL "$URL.asc" -o fctools.tar.gz.asc
  gpg --quiet --import pubkey.asc 2>/dev/null || true
  if gpg --status-fd 1 --verify fctools.tar.gz.asc fctools.tar.gz 2>/dev/null | grep -q "VALIDSIG $FPR"; then
    echo "    ok  good signature from $FPR"
  else
    echo "    SIGNATURE DID NOT VERIFY AGAINST $FPR — STOPPING."
    echo "    Do not use this copy. Report it before going further."
    exit 1
  fi
  echo "    NOTE: the key was fetched from the same host as the bundle, so this proves the two"
  echo "    match each other. Confirm the fingerprint above against DEPLOY.md to make it mean more."
else
  echo "    gpg not installed — hash checked, signature NOT checked. Acceptable only if you"
  echo "    compared the hash above against your own off-box record."
fi

tar xzf fctools.tar.gz && rm -f fctools.tar.gz fctools.tar.gz.asc pubkey.asc

# A VIRTUALENV WITH PINNED VERSIONS, not the distro's packages. apt on Ubuntu 24.04 ships
# pandas 2.x; these instruments are written and self-tested against the versions pinned in
# fctools/requirements.txt, which is inside the verified tarball and therefore covered by the
# hash checked above. Running a reproducibility toolkit on an unpinned stack is the same defect
# it exists to find, one layer up.
echo "==> virtualenv with the pinned stack (fctools/requirements.txt, hash-covered)"
python3 -m venv .venv
./.venv/bin/pip install --quiet --disable-pip-version-check --upgrade pip
./.venv/bin/pip install --quiet --disable-pip-version-check -r fctools/requirements.txt

echo "==> running the toolkit's own self-test"
echo "    If an instrument cannot find its own planted bug, nothing it says about client code is"
echo "    safe to send. This is the gate, not a formality."
./.venv/bin/python fctools/selftest_all.py

cat <<'EOF'

==> ready.

    Next, in this order:

    1. Bring the client's material DIRECTLY here. Not via your laptop, never via the research
       box. Either give them an SFTP account on this machine, or curl their link from here.
    2. Record a sha256 of every file on arrival, before opening any of it. That hash is what the
       report's reproducibility claim is anchored to.
    3. FC-1 first — ./.venv/bin/python fctools/fc1_reproduce.py --cmd "<their command>".
       Use ./.venv/bin/python for EVERY instrument: the pinned stack is the one the findings
       were validated on, and the self-test prints it so the report can cite it.
       If the headline number will not come out twice, stop and report that. Everything
       downstream is worthless until it does, and this is the natural stop-and-report point.
    4. Work the rest of the checks in ../PLAYBOOK.md order.

    On delivery: destroy this instance and write the date in the engagement file.

EOF
