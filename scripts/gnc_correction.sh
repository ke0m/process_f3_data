#! /bin/bash

set -x

ROOT_DIR=/net/brick5/data3/northsea_dutch_f3/process_f3_data/windowed_data/all

python scripts/gnc_correction.py  \
  --input-data=${ROOT_DIR}/f3_shots_all_6073483-487273-wind100_debubble.H \
  --output-data=${ROOT_DIR}/f3_shots_all_6073483-487273-wind100_gnc.H \
  --time-shift=0.008 \
  --max-time=6
