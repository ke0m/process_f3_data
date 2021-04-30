import argparse

from regio import seppy
from sivu.movie import qc_f3data


def main(args):
  sep = seppy.sep()
  # Read in the geometry
  _, srcx = sep.read_file(args.srcx)
  _, srcy = sep.read_file(args.srcy)
  _, recx = sep.read_file(args.recx)
  _, recy = sep.read_file(args.recy)
  _, nrec = sep.read_file(args.nrec_per_shot)
  nrec = nrec.astype('int32')
  # Read in the data
  daxes, data = sep.read_file(args.data)
  data = data.reshape(daxes.n, order='F').T
  dt, _ = daxes.d

  # Read in the image slice
  saxes, slc = sep.read_file(args.img)
  slc = slc.reshape(saxes.n, order='F')
  slcw = slc[args.slc_idx, 200:1200, 5:505]

  print("Press 'n' to move forward, 'm' to move back one shot")
  print("Press 'y' to move forward, 'u' to move back %d shots" % (args.sjump))
  ntw = 750 if dt == 0.004 else 1500
  qc_f3data(
      data,
      srcx,
      recx,
      srcy,
      recy,
      nrec,
      slcw,
      dt=dt,
      ntw=ntw,
      pclip=args.pclip,
      sjump=args.sjump,
  )


def attach_args(parser=argparse.ArgumentParser()):
  parser.add_argument("--srcx", type=str, default=None)
  parser.add_argument("--srcy", type=str, default=None)
  parser.add_argument("--recx", type=str, default=None)
  parser.add_argument("--recy", type=str, default=None)
  parser.add_argument("--nrec-per-shot", type=str, default=None)
  parser.add_argument("--data", type=str, default=None)
  parser.add_argument(
      "--img",
      type=str,
      default="/net/brick5/data3/northsea_dutch_f3/mig/mig.T",
  )
  parser.add_argument("--slc-idx", type=int, default=400)
  parser.add_argument("--pclip", type=float, default=0.02)
  parser.add_argument("--sjump", type=int, default=10)
  return parser


if __name__ == "__main__":
  main(attach_args().parse_args())
