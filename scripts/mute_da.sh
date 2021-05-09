#! /bin/bash

ROOT_DIR=/net/brick5/data3/northsea_dutch_f3/process_f3_data/windowed_data/all

set -x

python ./scripts/mute_da.py \
  --input-data=${ROOT_DIR}/chunks/chunk_034/f3_shots_034.H \
  --srcx=${ROOT_DIR}/chunks/chunk_034/f3_srcx_034.H \
  --recx=${ROOT_DIR}/chunks/chunk_034/f3_recx_034.H \
  --srcy=${ROOT_DIR}/chunks/chunk_034/f3_srcy_034.H \
  --recy=${ROOT_DIR}/chunks/chunk_034/f3_recy_034.H \
  --nrec-per-shot=${ROOT_DIR}/chunks/chunk_034/f3_nrec_034.H \
  --streamer-header=${ROOT_DIR}/chunks/chunk_034/f3_strm_034.H \
  --output-data=${ROOT_DIR}/chunks/chunk_034/f3_mute_qc_034.H \
  --water-vel=1450 \
  --qc
