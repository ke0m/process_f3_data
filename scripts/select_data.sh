#! /bin/bash

ROOT_DIR=/net/brick5/data3/northsea_dutch_f3

set -x

python scripts/select_data.py \
  --src-hash-map=${ROOT_DIR}/segy/info_new/src_hmap.npy \
  --src-coords=${ROOT_DIR}/segy/info_new/scoords.npy \
  --dsx=100 \
  --dsy=50  \
  --nxg=500 \
  --nyg=500 \
  --output-srcx-coords=${ROOT_DIR}/process_f3_data/windowed_data/f3_srcx_new.H \
  --output-srcy-coords=${ROOT_DIR}/process_f3_data/windowed_data/f3_srcy_new.H \
  --output-recx-coords=${ROOT_DIR}/process_f3_data/windowed_data/f3_recx_new.H \
  --output-recy-coords=${ROOT_DIR}/process_f3_data/windowed_data/f3_recy_new.H \
  --output-recy-coords=${ROOT_DIR}/process_f3_data/windowed_data/f3_recy_new.H \
  --output-nrec-per-shot=${ROOT_DIR}/process_f3_data/windowed_data/f3_nrec_new.H \
  --output-streamer-hdr=${ROOT_DIR}/process_f3_data/windowed_data/f3_strm_new.H \
  --output-shots=${ROOT_DIR}/process_f3_data/windowed_data/f3_shots_new.H
