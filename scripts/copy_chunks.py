import os
import argparse
import subprocess

from adf.gradopt.utils import create_inttag


def main(args):

  with open(args.fg_chunk_list, 'r') as f:
    fg_chunks = [line.rstrip().split('chunk_')[-1] for line in f.readlines()]

  scp_cmd = "scp %s mazama:%s"
  for idx in range(args.beg_idx, args.end_idx + 1):
    tag = create_inttag(idx, 100)
    if tag in fg_chunks:
      name = 'chunk_%sfg' % tag
    else:
      name = "chunk_%s" % tag
    path = os.path.join(args.root_dir, name)
    chunk_file = os.path.join(path, name + '.npy')
    cmd = scp_cmd % (chunk_file, args.remote_dir)
    print(cmd)
    subprocess.check_call(cmd, shell=True)


def attach_args(parser=argparse.ArgumentParser()):
  parser.add_argument("--beg-idx", type=int, default=0)
  parser.add_argument("--end-idx", type=int, default=300)
  parser.add_argument(
      "--root-dir",
      type=str,
      default="./windowed_data/all/chunks",
  )
  parser.add_argument(
      "--remote-dir",
      type=str,
      default="/scratch/joseph29/f3_data_chunks/all_chunks",
  )
  parser.add_argument(
      "--fg-chunk-list",
      type=str,
      default='./doc/fg-chunks.txt',
  )
  return parser


if __name__ == "__main__":
  main(attach_args().parse_args())
