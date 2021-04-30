import os
import argparse
import numpy as np

from regio import seppy


def main(args):
  sep = seppy.sep()

  output_suffix = args.suffix.split(".H")[0] + '-wind%d.H' % (args.nshots)

  # Window based on shots
  _, srcx = sep.read_file(
      os.path.join(args.data_dir, 'f3_srcx_all_' + args.suffix))
  srcxw = srcx[:args.nshots]
  sep.write_file(os.path.join(args.data_dir, 'f3_srcx_all_' + output_suffix),
                 srcxw)

  _, srcy = sep.read_file(
      os.path.join(args.data_dir, 'f3_srcy_all_' + args.suffix))
  srcyw = srcy[:args.nshots]
  sep.write_file(os.path.join(args.data_dir, 'f3_srcy_all_' + output_suffix),
                 srcyw)

  _, nrec = sep.read_file(
      os.path.join(args.data_dir, 'f3_nrec_all_' + args.suffix))
  nrecw = nrec[:args.nshots]
  sep.write_file(os.path.join(args.data_dir, 'f3_nrec_all_' + output_suffix),
                 nrecw)

  # Window based on traces
  ntrw = np.sum(nrec[:args.nshots].astype('int32'))

  daxes, data = sep.read_file(
      os.path.join(args.data_dir, 'f3_shots_all_' + args.suffix))
  data = data.reshape(daxes.n, order='F')
  dataw = data[:, :ntrw]
  sep.write_file(os.path.join(args.data_dir, 'f3_shots_all_' + output_suffix),
                 dataw, os=daxes.o, ds=daxes.d)

  _, recx = sep.read_file(
      os.path.join(args.data_dir, 'f3_recx_all_' + args.suffix))
  recxw = recx[:ntrw]
  sep.write_file(os.path.join(args.data_dir, 'f3_recx_all_' + output_suffix),
                 recxw)

  _, recy = sep.read_file(
      os.path.join(args.data_dir, 'f3_recy_all_' + args.suffix))
  recyw = recy[:ntrw]
  sep.write_file(os.path.join(args.data_dir, 'f3_recy_all_' + output_suffix),
                 recyw)

  _, strm = sep.read_file(
      os.path.join(args.data_dir, 'f3_strm_all_' + args.suffix))
  strmw = strm[:ntrw]
  sep.write_file(os.path.join(args.data_dir, 'f3_strm_all_' + output_suffix),
                 strmw)


def attach_args(parser=argparse.ArgumentParser()):
  root_dir = "/net/brick5/data3/northsea_dutch_f3/"
  parser.add_argument(
      "--data-dir",
      type=str,
      default=root_dir + "process_f3_data/windowed_data/all",
  )
  parser.add_argument("--suffix", type=str, default="6073483-487273.H")
  parser.add_argument("--nshots", type=str, default=100)
  return parser


if __name__ == "__main__":
  main(attach_args().parse_args())
