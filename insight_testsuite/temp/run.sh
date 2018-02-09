#!/usr/bin/env bash

set -x
#Execute the following command from the root directory
python ./src/donation_analytics.py ./input/percentile.txt ./input/itcont.txt ./output/repeat_donors.txt

read
set +x