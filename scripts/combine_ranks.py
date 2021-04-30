import os
import argparse
from tqdm import tqdm

from regio import seppy


def main(args):

  sep = seppy.sep()

  files = [
      os.path.join(args.data_dir, ifile)
      for ifile in os.listdir(args.data_dir)
      if 'f3_shots' in ifile
  ]

  for k, ifile in tqdm(enumerate(files), desc='files', total=len(files)):
    daxes, data = sep.read_file(ifile)
    data = data.reshape(daxes.n, order='F')
    if k == 0:
      sep.write_file(args.output_file, data, os=daxes.o, ds=daxes.d)
    else:
      sep.append_file(args.output_file, data)


def attach_args(parser=argparse.ArgumentParser()):
  path = "/net/brick5/data3/northsea_dutch_f3/process_f3_data/windowed_data/all"
  parser.add_argument("--data-dir", type=str, default=path)
  parser.add_argument(
      "--output-file",
      type=str,
      default=os.path.join(path, 'f3_shots_all_combined.H'),
  )
  return parser


if __name__ == "__main__":
  main(attach_args().parse_args())
