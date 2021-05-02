#! /bin/bash

set -x

ROOT_DIR=/net/brick5/data3/northsea_dutch_f3

python ./scripts/qc_vel_geometry.py \
  --srcx=${ROOT_DIR}/process_f3_data/windowed_data/all/f3_srcx_all_6073483-487273-wind100.H \
  --srcy=${ROOT_DIR}/process_f3_data/windowed_data/all/f3_srcy_all_6073483-487273-wind100.H \
  --recx=${ROOT_DIR}/process_f3_data/windowed_data/all/f3_recx_all_6073483-487273-wind100.H \
  --recy=${ROOT_DIR}/process_f3_data/windowed_data/all/f3_recy_all_6073483-487273-wind100.H \
  --vel-model=/homes/sep/joseph29/projects/resfoc/bench/f3/miglintz5m.H \
  --img-cube=${ROOT_DIR}/mig/mig.T \
  --beg-inline-idx=0 \
  --end-inline-idx=500 \
  --max-xline-idx=500 \
  --max-depth-idx=1000 \
  --vel-slice-idx=500
