import argparse

from regio import seppy
from sivu.plot import plot_acq


def main(args):
  sep = seppy.sep()

  # Read in geometry
  sxaxes, srcx = sep.read_file(args.srcx_coords)
  syaxes, srcy = sep.read_file(args.srcy_coords)
  rxaxes, recx = sep.read_file(args.recx_coords)
  ryaxes, recy = sep.read_file(args.recy_coords)

  naxes, nrec = sep.read_file(args.nrec_per_shot)
  nrec = nrec.astype('int32')

  # Read in time slice for QC
  sep = seppy.sep()
  saxes, slc = sep.read_file(args.img)
  slc = slc.reshape(saxes.n, order='F')
  slcw = slc[args.slc_idx, 200:1200, 5:505]

  plot_acq(srcx, srcy, recx, recy, slcw, recs=False, show=True)


def attach_args(parser=argparse.ArgumentParser()):
  parser.add_argument("--srcx-coords", type=str, default=None)
  parser.add_argument("--srcy-coords", type=str, default=None)
  parser.add_argument("--recx-coords", type=str, default=None)
  parser.add_argument("--recy-coords", type=str, default=None)
  parser.add_argument("--nrec-per-shot", type=str, default=None)
  parser.add_argument(
      "--img",
      type=str,
      default="/net/brick5/data3/northsea_dutch_f3/mig/mig.T",
  )
  parser.add_argument("--slc-idx", type=int, default=400)
  return parser


if __name__ == "__main__":
  main(attach_args().parse_args())
