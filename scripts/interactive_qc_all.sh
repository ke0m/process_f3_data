#! /bin/bash

set -x

python scripts/interactive_qc_all.py \
  --data-dir=/net/brick5/data3/northsea_dutch_f3/process_f3_data/windowed_data/all/chunks/chunk_000 \
  --start-idx=0 \
  --ntw=750
