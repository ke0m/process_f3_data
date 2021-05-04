import argparse
import numpy as np
from tqdm import tqdm

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

  if args.input_filter is not None:
    faxes, invflt = sep.read_file(args.input_filter)
    laxes, lags = sep.read_file(args.input_lags)
    lags = lags.astype('int32')
  else:
    lags, invflt = gapped_pef(
        data[args.trace_idx],
        na=args.na,
        gap=args.gap,
        niter=args.niter,
        verb=args.verb,
    )

  cop = conv1dm(nt, len(lags), lags, flt=invflt)

  deb = np.zeros(data.shape, dtype='float32')
  for itr in tqdm(range(ntr), desc="ntr", disable=(not args.verb)):
    cop.forward(False, data[itr], deb[itr])

  sep.write_file(args.output_data, deb.T, os=daxes.o, ds=daxes.d)


def attach_args(parser=argparse.ArgumentParser()):
  parser.add_argument("--input-data", type=str, default=None)
  parser.add_argument("--input-filter", type=str, default=None)
  parser.add_argument("--input-lags", type=str, default=None)
  parser.add_argument("--output-data", type=str, default=None)
  parser.add_argument("--trace-idx", type=int, default=20)
  parser.add_argument("--na", type=int, default=30)
  parser.add_argument("--gap", type=int, default=10)
  parser.add_argument("--niter", type=int, default=300)
  parser.add_argument("--verb", action='store_true', default=False)
  return parser


if __name__ == "__main__":
  main(attach_args().parse_args())
