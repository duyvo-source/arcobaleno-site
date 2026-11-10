#!/bin/sh
# Read everything again from the chain on free public endpoints, then print the base and the value per BAL.
# Slow: can take hours if endpoints throttle. Run one at a time: the scripts share the cache files in data/.
# discover.py and hist_tokens.py are left out on purpose: they read today's state from the block explorers
# (which now refuse automated reads); their October output ships in data/.
set -e
cd "$(dirname "$0")"
python3 scripts/assets.py
python3 scripts/fixes.py
python3 scripts/denom.py
python3 scripts/denom2.py
python3 scripts/window.py
python3 scripts/mimic.py
python3 scripts/multisig.py
python3 scripts/candidates.py
python3 scripts/unpriced.py
python3 scripts/rule3.py
