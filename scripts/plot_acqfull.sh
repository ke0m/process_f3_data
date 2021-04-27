#! /bin/bash

ROOT_DIR=/net/brick5/data3/northsea_dutch_f3/process_f3_data/windowed_data

python scripts/plot_acqfull.py \
  --srcx-coords=${ROOT_DIR}/f3_srcx_new.H \
  --srcy-coords=${ROOT_DIR}/f3_srcy_new.H \
  --recx-coords=${ROOT_DIR}/f3_recx_new.H \
  --recy-coords=${ROOT_DIR}/f3_recy_new.H \
  --nrec-per-shot=${ROOT_DIR}/f3_nrec_new.H &

PROC_DIR=/homes/sep/joseph29/projects/resfoc/bench/f3

python scripts/plot_acqfull.py \
  --srcx-coords=${PROC_DIR}/f3_srcx3_full_clean2.H \
  --srcy-coords=${PROC_DIR}/f3_srcy3_full_clean2.H \
  --recx-coords=${PROC_DIR}/f3_recx3_full_clean2.H \
  --recy-coords=${PROC_DIR}/f3_recy3_full_clean2.H \
  --nrec-per-shot=${PROC_DIR}/f3_nrec3_full_clean2.H &
