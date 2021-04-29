#! /bin/bash

set -x

ROOT_DIR=/net/brick5/data3/northsea_dutch_f3/process_f3_data/windowed_data/dsy50/clean

python scripts/interactive_qc.py \
  --srcx=${ROOT_DIR}/f3_srcx_clean_dsy50_6072475-6072825.H \
  --srcy=${ROOT_DIR}/f3_srcy_clean_dsy50_6072475-6072825.H \
  --recx=${ROOT_DIR}/f3_recx_clean_dsy50_6072475-6072825.H \
  --recy=${ROOT_DIR}/f3_recy_clean_dsy50_6072475-6072825.H \
  --nrec-per-shot=${ROOT_DIR}/f3_nrec_clean_dsy50_6072475-6072825.H \
  --data=${ROOT_DIR}/f3_shots_clean_dsy50_6072475-6072825.H
