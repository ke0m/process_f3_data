#! /bin/bash

set -x

ROOT_DIR=/net/brick5/data3/northsea_dutch_f3/process_f3_data/windowed_data/all

python ./scripts/debubble_shots.py \
  --input-data=${ROOT_DIR}/f3_shots_all_6073483-487273-wind100_mute.H \
  --output-data=${ROOT_DIR}/f3_shots_all_6073483-487273-wind100_debubble.H \
  --trace-idx=20 \
  --na=30 \
  --gap=10 \
  --niter=300 \
  --verb
