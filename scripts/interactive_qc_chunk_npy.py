import os
import argparse
import numpy as np

from regio import seppy
from sivu.movie import qc_f3data
from sivu.plot import plot_acq


def main(args):
  # Read in the .npz files
  files = [
      os.path.join(args.chunk_dir, ifile)
      for ifile in os.listdir(args.chunk_dir)
      if '.npy' in ifile
  ]

  ddicts = [np.load(ifile, allow_pickle=True).item() for ifile in files]

  # Concatenate into arrays
  data, srcx, recx, srcy, recy, nrec = [], [], [], [], [], []
  for ddict in ddicts:
    data.append(ddict['f3_shots'])
    srcx.append(ddict['f3_srcx'])
    srcy.append(ddict['f3_srcy'])
    recx.append(ddict['f3_recx'])
    recy.append(ddict['f3_recy'])
    nrec.append(ddict['f3_nrec'])

  data = np.concatenate(data, axis=0)
  srcx = np.concatenate(srcx, axis=0)
  srcy = np.concatenate(srcy, axis=0)
  recx = np.concatenate(recx, axis=0)
  recy = np.concatenate(recy, axis=0)
  nrec = np.concatenate(nrec, axis=0)
  dt = ddict['dt']

  # Read in the image slice
  sep = seppy.sep()
  saxes, slc = sep.read_file(args.img)
  slc = slc.reshape(saxes.n, order='F')
  slcw = slc[args.slc_idx, 200:1200, 5:505]

  # Read in the velocity model slice
  vaxes, vel = sep.read_file(args.vel)
  vel = vel.reshape(vaxes.n, order='F')
  velw = vel[args.slc_idx]

  # Plot sources on velocity model and image
  plot_acq(srcx, srcy, recx, recy, slcw, recs=False, show=False)
  plot_acq(srcx, srcy, recx, recy, velw, recs=False, show=False)

  # Plot receivers on velocity model and image
  plot_acq(srcx, srcy, recx, recy, slcw, recs=True, show=False)
  plot_acq(srcx, srcy, recx, recy, velw, recs=True, show=False)

  # Interactive QC of geometry and data
  print("Press 'n' to move forward, 'm' to move back one shot")
  print("Press 'y' to move forward, 'u' to move back %d shots" % (args.sjump))
  qc_f3data(
      data,
      srcx,
      recx,
      srcy,
      recy,
      nrec,
      slcw,
      dt=dt,
      ntw=args.ntw,
      pclip=args.pclip / 2,
      sjump=args.sjump,
      show=True,
  )


def attach_args(parser=argparse.ArgumentParser()):
  parser.add_argument("--chunk-dir", type=str, default=None)
  parser.add_argument(
      "--img",
      type=str,
      default="/net/brick5/data3/northsea_dutch_f3/mig/mig.T",
  )
  parser.add_argument(
      "--vel",
      type=str,
      default="/homes/sep/joseph29/projects/resfoc/bench/f3/miglintz5m.H",
  )
  parser.add_argument("--slc-idx", type=int, default=400)
  parser.add_argument("--pclip", type=float, default=0.05)
  parser.add_argument("--sjump", type=int, default=10)
  parser.add_argument("--ntw", type=int, default=750)
  return parser


if __name__ == "__main__":
  main(attach_args().parse_args())
