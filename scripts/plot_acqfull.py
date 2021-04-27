import argparse

from regio import seppy
from utils import plot_acq


def main(args):
  sep = seppy.sep()

  # Read in geometry
  sxaxes, srcx = sep.read_file(args.srcx_coords)
  syaxes, srcy = sep.read_file(args.srcy_coords)
  rxaxes, recx = sep.read_file(args.recx_coords)
  ryaxes, recy = sep.read_file(args.recy_coords)

  naxes, nrec = sep.read_file(args.nrec_per_shot)
  nrec = nrec.astype('int32')

  srcx *= 0.001
  srcy *= 0.001
  recx *= 0.001
  recy *= 0.001

  # Read in time slice for QC
  saxes, slc = sep.read_file(args.img)
  dt, dx, dy = saxes.d
  ot, ox, oy = saxes.o
  ox, oy = 469.800, 6072.350
  slc = slc.reshape(saxes.n, order='F')
  oxv, oyv = 200, 5
  nxv, nyv = 1000, 600
  oxw = ox + oxv * dx
  oyw = oy + oyv * dy
  slcw = slc[args.slc_idx, oxv:oxv + nxv, oyv:oyv + nyv].T

  plot_acq(
      srcx,
      srcy,
      recx,
      recy,
      slcw,
      ox=oxw,
      oy=oyw,
      recs=False,
      show=True,
  )


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
