import os
import argparse
import numpy as np
from tqdm import tqdm


def main(args):
  files = sorted([
      os.path.join(args.src_info_dir, ifile)
      for ifile in os.listdir(args.src_info_dir)
      if '.txt' in ifile
  ])

  odict, srcx, srcy = {}, [], []
  for ifile in tqdm(files, desc='files'):
    # Read in in the file
    with open(ifile, 'r') as f:
      scoords = f.readlines()
    # Change the file extension to SEGY
    sfile = os.path.join(
        args.segy,
        os.path.splitext(os.path.basename(ifile))[0] + '.segy',
    )
    for icrd in scoords:
      key = icrd.rstrip()[:14]
      srcx.append(int(key[:7]))
      srcy.append(int(key[8:]))
      if (key not in odict.keys()):
        odict[key] = [sfile]
      else:
        odict[key].append(sfile)

  # Get unique source coordinates
  srcx = np.asarray(srcx)
  srcy = np.asarray(srcy)
  srcs = np.zeros([len(srcx), 2])
  srcs[:, 0] = srcx
  srcs[:, 1] = srcy
  usrcs = np.unique(srcs, axis=0)

  np.save(args.output_hmap, odict)
  np.save(args.output_scoords, usrcs)


def attach_args(parser=argparse.ArgumentParser()):
  parser.add_argument(
      "--segy",
      type=str,
      default="/net/brick5/data3/northsea_dutch_f3/segy",
      help="Path to segy files",
  )
  parser.add_argument(
      "--src-info-dir",
      type=str,
      default="/net/brick5/data3/northsea_dutch_f3/segy/info_new",
  )
  parser.add_argument(
      "--output-hmap",
      type=str,
      default="/net/brick5/data3/northsea_dutch_f3/segy/info_new/src_hmap.npy",
  )
  parser.add_argument(
      "--output-scoords",
      type=str,
      default="/net/brick5/data3/northsea_dutch_f3/segy/info_new/scoords.npy",
  )
  return parser


if __name__ == "__main__":
  main(attach_args().parse_args())
