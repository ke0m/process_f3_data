#! /bin/bash

ROOT_DIR=/net/brick5/data3/northsea_dutch_f3

set -x

mpirun --hostfile=hostfile.txt -np=32 \
  python scripts/select_data_parallel.py \
  --src-hash-map=${ROOT_DIR}/segy/info_new/src_hmap.npy \
  --src-coords=${ROOT_DIR}/segy/info_new/scoords.npy \
  --dsx=100 \
  --dsy=50  \
  --nxg=500 \
  --nyg=500 \
  --output-base-srcx-coords=${ROOT_DIR}/process_f3_data/windowed_data/dsy50/f3_srcx_dsy50_%d-%d.H \
  --output-base-srcy-coords=${ROOT_DIR}/process_f3_data/windowed_data/dsy50/f3_srcy_dsy50_%d-%d.H \
  --output-base-recx-coords=${ROOT_DIR}/process_f3_data/windowed_data/dsy50/f3_recx_dsy50_%d-%d.H \
  --output-base-recy-coords=${ROOT_DIR}/process_f3_data/windowed_data/dsy50/f3_recy_dsy50_%d-%d.H \
  --output-base-recy-coords=${ROOT_DIR}/process_f3_data/windowed_data/dsy50/f3_recy_dsy50_%d-%d.H \
  --output-base-nrec-per-shot=${ROOT_DIR}/process_f3_data/windowed_data/dsy50/f3_nrec_dsy50_%d-%d.H \
  --output-base-streamer-hdr=${ROOT_DIR}/process_f3_data/windowed_data/dsy50/f3_strm_dsy50_%d-%d.H \
  --output-base-shots=${ROOT_DIR}/process_f3_data/windowed_data/dsy50/f3_shots_dsy50_%d-%d.H
