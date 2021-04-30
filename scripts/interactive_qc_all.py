import os
import argparse
from tqdm import tqdm

from regio import seppy
from sivu.movie import qc_f3data


def main(args):

  suffixes = sorted([
      ifile.split('f3_shots')[-1]
      for ifile in os.listdir(args.data_dir)
      if 'f3_shots' in ifile
  ])

  # Read in the image slice
  sep = seppy.sep()
  saxes, slc = sep.read_file(args.img)
  slc = slc.reshape(saxes.n, order='F')
  slcw = slc[args.slc_idx, 200:1200, 5:505]

  print("Press 'n' to move forward, 'm' to move back one shot")
  print("Press 'y' to move forward, 'u' to move back %d shots" % (args.sjump))

  for suffix in tqdm(suffixes[args.start_idx:args.end_idx], desc='file'):
    # Read in the geometry
    _, srcx = sep.read_file(os.path.join(args.data_dir, 'f3_srcx' + suffix))
    _, srcy = sep.read_file(os.path.join(args.data_dir, 'f3_srcy' + suffix))
    _, recx = sep.read_file(os.path.join(args.data_dir, 'f3_recx' + suffix))
    _, recy = sep.read_file(os.path.join(args.data_dir, 'f3_recy' + suffix))
    _, nrec = sep.read_file(os.path.join(args.data_dir, 'f3_nrec' + suffix))
    nrec = nrec.astype('int32')
    # Read in the data
    dname = 'f3_shots' + suffix
    daxes, data = sep.read_file(os.path.join(args.data_dir, dname))
    data = data.reshape(daxes.n, order='F').T

    qc_f3data(
        data,
        srcx,
        recx,
        srcy,
        recy,
        nrec,
        slcw,
        pclip=args.pclip,
        sjump=args.sjump,
    )


def attach_args(parser=argparse.ArgumentParser()):
  parser.add_argument("--data-dir", type=str, default=None)
  parser.add_argument(
      "--img",
      type=str,
      default="/net/brick5/data3/northsea_dutch_f3/mig/mig.T",
  )
  parser.add_argument("--slc-idx", type=int, default=400)
  parser.add_argument("--pclip", type=float, default=0.02)
  parser.add_argument("--sjump", type=int, default=10)
  parser.add_argument("--start-idx", type=int, default=0)
  parser.add_argument("--end-idx", type=int, default=-1)
  return parser


if __name__ == "__main__":
  main(attach_args().parse_args())
