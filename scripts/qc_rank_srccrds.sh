#! /bin/bash

python scripts/qc_rank_srccrds.py \
	--data-dir=/net/brick5/data3/northsea_dutch_f3/process_f3_data/windowed_data/dsy50 &

python scripts/qc_rank_srccrds.py \
	--data-dir=/net/brick5/data3/northsea_dutch_f3/process_f3_data/windowed_data/ranks

#python scripts/qc_rank_srccrds.py \
#	--data-dir=/net/brick5/data3/northsea_dutch_f3/process_f3_data/windowed_data/dsy100
