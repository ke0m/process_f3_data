import argparse
import numpy as np

from regio import seppy


def main(args):
  sep = seppy.sep()
  daxes, data = sep.read_file(args.input_data)
  data = data.reshape(daxes.n, order='F').T
  data = np.ascontiguousarray(data).astype('float32')
  ntr, nt = data.shape
  dt, _ = daxes.d

  samples = int(args.time_shift / dt)
  data_pad = np.pad(data, ((0, 0), (0, samples)))

  data_shift = np.roll(data_pad, samples, axis=1)

  # Window to max time
  max_samples = int(args.max_time / dt)
  data_shift = data_shift[:, :max_samples]

  sep.write_file(args.output_data, data_shift.T, os=daxes.o, ds=daxes.d)


def attach_args(parser=argparse.ArgumentParser()):
  parser.add_argument("--input-data", type=str, default=None)
  parser.add_argument("--output-data", type=str, default=None)
  parser.add_argument("--time-shift", type=float, default=0.008)
  parser.add_argument("--max-time", type=float, default=6)
  return parser


if __name__ == "__main__":
  main(attach_args().parse_args())
