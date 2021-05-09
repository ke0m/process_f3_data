import os
import argparse
import numpy as np
import matplotlib.pyplot as plt

from regio import seppy
from sivu.movie import qc_f3data


def main(args):
  files = os.listdir(args.chunk_dir)
  files = list(filter(lambda f: '.H' in f, files))

  keys = [
      'f3_shots', 'f3_srcx', 'f3_recx', 'f3_srcy', 'f3_recy', 'f3_nrec',
      'f3_strm', 'f3_mute', 'f3_debubble', 'f3_processed'
  ]

  ddict = {
      key: os.path.join(args.chunk_dir, ifile)
      for key in keys for ifile in files if key in ifile
  }

  # Read in the geometry
  sep = seppy.sep()
  _, srcx = sep.read_file(ddict['f3_srcx'])
  _, srcy = sep.read_file(ddict['f3_srcy'])
  _, recx = sep.read_file(ddict['f3_recx'])
  _, recy = sep.read_file(ddict['f3_recy'])
  _, nrec = sep.read_file(ddict['f3_nrec'])
  nrec = nrec.astype('int32')
  # Read in the different stages of processing
  daxes, raw = sep.read_file(ddict['f3_shots'])
  raw = raw.reshape(daxes.n, order='F').T
  daxes, mute = sep.read_file(ddict['f3_mute'])
  mute = mute.reshape(daxes.n, order='F').T
  daxes, deb = sep.read_file(ddict['f3_debubble'])
  deb = deb.reshape(daxes.n, order='F').T
  paxes, prc = sep.read_file(ddict['f3_processed'])
  prc = prc.reshape(paxes.n, order='F').T
  dt, _ = daxes.d

  # Read in the image slice
  saxes, slc = sep.read_file(args.img)
  slc = slc.reshape(saxes.n, order='F')
  slcw = slc[args.slc_idx, 200:1200, 5:505]

  print("Press 'n' to move forward, 'm' to move back one shot")
  print("Press 'y' to move forward, 'u' to move back %d shots" % (args.sjump))
  qc_f3data(
      raw,
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
      show=False,
  )

  qc_f3data(
      mute,
      srcx,
      recx,
      srcy,
      recy,
      nrec,
      slcw,
      dt=dt,
      ntw=args.ntw,
      pclip=args.pclip,
      sjump=args.sjump,
      show=False,
  )

  qc_f3data(
      deb,
      srcx,
      recx,
      srcy,
      recy,
      nrec,
      slcw,
      dt=dt,
      ntw=args.ntw,
      pclip=args.pclip,
      sjump=args.sjump,
      show=False
  )

  qc_f3data(
      prc,
      srcx,
      recx,
      srcy,
      recy,
      nrec,
      slcw,
      dt=dt,
      ntw=args.ntw,
      pclip=args.pclip,
      sjump=args.sjump,
      show=True,
  )

  #trace_energy = np.sum(prc * prc, axis=1)
  #fig = plt.figure(figsize=(8, 8))
  #ax = fig.gca()
  #ax.plot(trace_energy)
  #ax.set_xlabel("Trace No", fontsize=15)
  #ax.set_ylabel("Energy", fontsize=15)
  #plt.show()


def attach_args(parser=argparse.ArgumentParser()):
  parser.add_argument("--chunk-dir", type=str, default=None)
  parser.add_argument(
      "--img",
      type=str,
      default="/net/brick5/data3/northsea_dutch_f3/mig/mig.T",
  )
  parser.add_argument("--slc-idx", type=int, default=400)
  parser.add_argument("--pclip", type=float, default=0.05)
  parser.add_argument("--sjump", type=int, default=10)
  parser.add_argument("--ntw", type=int, default=750)
  return parser


if __name__ == "__main__":
  main(attach_args().parse_args())
