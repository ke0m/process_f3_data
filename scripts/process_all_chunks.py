import os
import argparse
import subprocess

from adf.gradopt.utils import create_inttag


def main(args):

  # Read in file lists
  with open(args.noisy_chunk_list, 'r') as f:
    noisy_chunks = [line.rstrip() for line in f.readlines()]

  with open(args.omit_chunk_list, 'r') as f:
    omit_chunks = [line.rstrip() for line in f.readlines()]

  with open(args.fg_chunk_list, 'r') as f:
    fg_chunks = [line.rstrip().split('chunk_')[-1] for line in f.readlines()]

  base_cmd = """
  python scripts/process_chunk.py \
    --chunk-dir=%s \
    --output-data=%s
  """

  noisy_cmd = """
  python scripts/process_chunk.py \
    --chunk-dir=%s \
    --output-data=%s \
    --energy-level=1e8
  """

  # Make chunk names
  for i in range(args.start_idx, args.end_idx+1):
    tag = create_inttag(i, 100)
    if tag in fg_chunks:
      chunk_name = 'chunk_%sfg' % create_inttag(i, 100)
    else:
      chunk_name = 'chunk_%s' % create_inttag(i, 100)
    print(chunk_name)
    chunk_dir = os.path.join(args.root_dir, chunk_name)
    if chunk_name not in omit_chunks:
      if chunk_name in noisy_chunks:
        output_name = os.path.join(chunk_dir, chunk_name + '.npy')
        cmd = noisy_cmd % (chunk_dir, output_name)
      else:
        output_name = os.path.join(chunk_dir, chunk_name + '.npy')
        cmd = base_cmd % (chunk_dir, output_name)
      subprocess.check_call(cmd, shell=True)


def attach_args(parser=argparse.ArgumentParser()):
  parser.add_argument("--root-dir", type=str, default="./windowed_data/all/chunks")
  parser.add_argument("--start-idx", type=int, default=0)
  parser.add_argument("--end-idx", type=int, default=299)
  parser.add_argument("--noisy-chunk-list", type=str, default='noisy-chunks.txt')
  parser.add_argument("--omit-chunk-list", type=str, default='omit-chunks.txt')
  parser.add_argument("--fg-chunk-list", type=str, default='fg-chunks.txt')
  return parser


if __name__ == "__main__":
  main(attach_args().parse_args())
