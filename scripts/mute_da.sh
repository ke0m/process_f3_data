#! /bin/bash

ROOT_DIR=/net/brick5/data3/northsea_dutch_f3/process_f3_data/windowed_data/all

set -x

python ./scripts/mute_da.py \
  --input-data=${ROOT_DIR}/f3_shots_all_6073483-487273-wind100_interp.H \
  --srcx=${ROOT_DIR}/f3_srcx_all_6073483-487273-wind100.H \
  --recx=${ROOT_DIR}/f3_recx_all_6073483-487273-wind100.H \
  --srcy=${ROOT_DIR}/f3_srcy_all_6073483-487273-wind100.H \
  --recy=${ROOT_DIR}/f3_recy_all_6073483-487273-wind100.H \
  --nrec-per-shot=${ROOT_DIR}/f3_nrec_all_6073483-487273-wind100.H \
  --streamer-header=${ROOT_DIR}/f3_strm_all_6073483-487273-wind100.H \
  --output-data=${ROOT_DIR}/f3_shots_all_6073483-487273-wind100_mute.H \
  --water-vel=1450
