#! /bin/bash

python make_src_rec_info.py \
  --segy=/net/brick5/data3/northsea_dutch_f3/segy \
  --src-coords=./all_src_coords.H \
  --rec-coords=./all_rec_coords.H \
  --unique-src-coords=./unique_src_coords.H

