import os
import argparse
from tqdm import tqdm

from regio import seppy


def main(args):

  sep = seppy.sep()

  keys = [
      'f3_shots', 'f3_srcx', 'f3_recx', 'f3_srcy', 'f3_recy', 'f3_nrec',
      'f3_strm'
  ]

  for key in keys:

    files = sorted([
        os.path.join(args.data_dir, ifile)
        for ifile in os.listdir(args.data_dir)
        if key in ifile
    ])

    output_file = os.path.join(args.data_dir, key + '_all_combined.H')
    for k, ifile in tqdm(enumerate(files),
                         desc='%s files' % (key),
                         total=len(files)):
      daxes, data = sep.read_file(ifile)
      data = data.reshape(daxes.n, order='F')
      if k == 0:
        sep.write_file(output_file, data, os=daxes.o, ds=daxes.d)
      else:
        sep.append_file(output_file, data)


def attach_args(parser=argparse.ArgumentParser()):
  path = "/net/brick5/data3/northsea_dutch_f3/process_f3_data/windowed_data/all"
  parser.add_argument("--data-dir", type=str, default=path)
  return parser


if __name__ == "__main__":
  main(attach_args().parse_args())
