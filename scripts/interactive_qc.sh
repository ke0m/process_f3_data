#! /bin/bash

set -x

ROOT_DIR=/net/brick5/data3/northsea_dutch_f3/process_f3_data/windowed_data/all

#python scripts/interactive_qc.py \
#  --srcx=${ROOT_DIR}/f3_srcx_all_6073483-487273-wind100.H \
#  --srcy=${ROOT_DIR}/f3_srcy_all_6073483-487273-wind100.H \
#  --recx=${ROOT_DIR}/f3_recx_all_6073483-487273-wind100.H \
#  --recy=${ROOT_DIR}/f3_recy_all_6073483-487273-wind100.H \
#  --nrec-per-shot=${ROOT_DIR}/f3_nrec_all_6073483-487273-wind100.H \
#  --data=${ROOT_DIR}/f3_shots_all_6073483-487273-wind100_interp.H

python scripts/interactive_qc.py \
  --srcx=${ROOT_DIR}/f3_srcx_all_6073483-487273-wind100.H \
  --srcy=${ROOT_DIR}/f3_srcy_all_6073483-487273-wind100.H \
  --recx=${ROOT_DIR}/f3_recx_all_6073483-487273-wind100.H \
  --recy=${ROOT_DIR}/f3_recy_all_6073483-487273-wind100.H \
  --nrec-per-shot=${ROOT_DIR}/f3_nrec_all_6073483-487273-wind100.H \
  --data=${ROOT_DIR}/f3_shots_all_6073483-487273-wind100_mute.H \
  --pclip=0.1
