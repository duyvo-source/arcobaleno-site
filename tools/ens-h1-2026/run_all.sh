#!/bin/sh
# Rebuild everything from the chain on free public endpoints, then print the tables. Can take hours if endpoints throttle.
set -e
cd "$(dirname "$0")"
python3 transfers.py
python3 daily.py
python3 aave_rewards.py
python3 rewards.py
python3 blend.py
python3 idle.py
