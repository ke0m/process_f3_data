#! /bin/bash

set -x

python ./scripts/combine_remove_dupes.py \
  --data-dir=/net/brick5/data3/northsea_dutch_f3/process_f3_data/windowed_data/dsy50 \
  --output-prefix=_clean \
  --output-dir=/net/brick5/data3/northsea_dutch_f3/process_f3_data/windowed_data/dsy50/clean \
