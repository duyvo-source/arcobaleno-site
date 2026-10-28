#!/bin/sh
# Rebuild everything from the chain (about 10 minutes on free public endpoints), then print the table.
set -e
cd "$(dirname "$0")"
python3 daily.py
python3 logs_stkgho.py
python3 exits.py
python3 blend.py
