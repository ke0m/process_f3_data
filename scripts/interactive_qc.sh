#! /bin/bash

set -x

ROOT_DIR=/net/brick5/data3/northsea_dutch_f3/process_f3_data/windowed_data

#python scripts/interactive_qc.py \
#  --srcx=${ROOT_DIR}/f3_srcx_all_6073483-487273-wind100.H \
#  --srcy=${ROOT_DIR}/f3_srcy_all_6073483-487273-wind100.H \
#  --recx=${ROOT_DIR}/f3_recx_all_6073483-487273-wind100.H \
#  --recy=${ROOT_DIR}/f3_recy_all_6073483-487273-wind100.H \
#  --nrec-per-shot=${ROOT_DIR}/f3_nrec_all_6073483-487273-wind100.H \
#  --data=${ROOT_DIR}/f3_shots_all_6073483-487273-wind100_interp.H

python scripts/interactive_qc.py \
  --srcx=${ROOT_DIR}/all_inlines/f3_srcx_all_inlines.H \
  --srcy=${ROOT_DIR}/all_inlines/f3_srcy_all_inlines.H \
  --recx=${ROOT_DIR}/all_inlines/f3_recx_all_inlines.H \
  --recy=${ROOT_DIR}/all_inlines/f3_recy_all_inlines.H \
  --nrec-per-shot=${ROOT_DIR}/all_inlines/f3_nrec_all_inlines.H \
  --data=${ROOT_DIR}/all_inlines/f3_shots_all_inlines.H \
  --pclip=0.1
