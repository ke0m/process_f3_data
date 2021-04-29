#! /bin/bash

ROOT_DIR=/net/brick5/data3/northsea_dutch_f3

set -x

mpirun --hostfile=hostfile.txt -np=32 \
  python scripts/select_data_all_parallel.py \
  --src-hash-map=${ROOT_DIR}/segy/info_new/src_hmap.npy \
  --src-coords=${ROOT_DIR}/segy/info_new/scoords.npy \
  --nxg=500 \
  --nyg=500 \
  --output-base-srcx-coords=${ROOT_DIR}/process_f3_data/windowed_data/all/f3_srcx_all_%d-%d.H \
  --output-base-srcy-coords=${ROOT_DIR}/process_f3_data/windowed_data/all/f3_srcy_all_%d-%d.H \
  --output-base-recx-coords=${ROOT_DIR}/process_f3_data/windowed_data/all/f3_recx_all_%d-%d.H \
  --output-base-recy-coords=${ROOT_DIR}/process_f3_data/windowed_data/all/f3_recy_all_%d-%d.H \
  --output-base-recy-coords=${ROOT_DIR}/process_f3_data/windowed_data/all/f3_recy_all_%d-%d.H \
  --output-base-nrec-per-shot=${ROOT_DIR}/process_f3_data/windowed_data/all/f3_nrec_all_%d-%d.H \
  --output-base-streamer-hdr=${ROOT_DIR}/process_f3_data/windowed_data/all/f3_strm_all_%d-%d.H \
  --output-base-shots=${ROOT_DIR}/process_f3_data/windowed_data/all/f3_shots_all_%d-%d.H
