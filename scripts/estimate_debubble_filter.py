import argparse
import numpy as np

from regio import seppy
from adf.stat.pef1d import gapped_pef
from adf.stat.conv1dm import conv1dm


def main(args):
  sep = seppy.sep()

  daxes, data = sep.read_file(args.input_data)
  data = data.reshape(daxes.n, order='F').T
  data = np.ascontiguousarray(data).astype('float32')
  ntr, nt = data.shape
  dt, _ = daxes.d

  lags, invflt = gapped_pef(
      data[args.trace_idx],
      na=args.na,
      gap=args.gap,
      niter=args.niter,
      verb=args.verb,
  )

  sep.write_file(args.output_lags, lags.astype('float32'))
  sep.write_file(args.output_filter, invflt)

  if args.output_data_qc is not None:
    cop = conv1dm(nt, len(lags), lags, flt=invflt)
    deb = np.zeros(data.shape, dtype='float32')
    for itr in range(ntr):
      cop.forward(False, data[itr], deb[itr])

    sep.write_file(args.output_data_qc, deb.T, os=daxes.o, ds=daxes.d)


def attach_args(parser=argparse.ArgumentParser()):
  parser.add_argument(
      "--input-data",
      type=str,
      default="./debubble_data/shot_for_debubble.H",
  )
  parser.add_argument(
      "--trace-idx",
      type=int,
      default=20,
  )
  parser.add_argument("--na", type=int, default=30)
  parser.add_argument("--gap", type=int, default=10)
  parser.add_argument("--niter", type=int, default=300)
  parser.add_argument("--verb", action='store_true', default=False)
  parser.add_argument(
      "--output-lags",
      type=str,
      default="./debubble_data/lags.H",
  )
  parser.add_argument(
      "--output-filter",
      type=str,
      default="./debubble_data/filter.H",
  )
  parser.add_argument(
      "--output-data-qc",
      type=str,
      default="./debubble_data/debubbled_shot_qc.H",
  )
  return parser


if __name__ == "__main__":
  main(attach_args().parse_args())
