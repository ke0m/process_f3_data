import argparse
import numpy as np
from tqdm import tqdm

from regio import seppy
from mdsuops.mute import mute
from sivu.plot import plot_dat2d


def mute_f3shot(
    dat,
    isrcx,
    isrcy,
    nrec,
    strm,
    recx,
    recy,
    tp=0.5,
    vel=1450.0,
    dt=0.004,
    dx=0.025,
    hyper=True,
) -> np.ndarray:
  """
  Mutes a shot from the F3 dataset

  Parameters:
    dat   - an input shot gather from the F3 dataset [ntr,nt]
    isrcx - x source coordinate of the shot [float]
    isrcy - y source coordinate of the shot [float]
    strm  - index within the streamer
    recx  - x receiver coordinates for this shot [ntr]
    recy  - y receiver coordinates for this shot [ntr]
    vel   - water velocity [1450.0]
    tp    - length of taper [0.5s]
    dy    - minimum distance between streamers [20 m]
    dt    - temporal sampling interval [0.002]
    dx    - spacing between receivers [25 m]

  Returns a muted shot gather
  """
  mut = np.zeros(dat.shape, dtype='float32')
  v0 = vel * 0.001
  # Find the beginning indices of the streamer
  idxs = list(np.where(strm[:nrec] == 1)[0])
  idxs.append(nrec)
  for istr in range(1, len(idxs)):
    irecx, irecy = recx[idxs[istr - 1]], recy[idxs[istr - 1]]
    dist = np.sqrt((isrcx - irecx)**2 + (isrcy - irecy)**2)
    t0 = dist / vel
    if (t0 > 0.15):
      t0 = dist / (vel)
      v0 = 1.5
    else:
      v0 = vel * 0.001
    mut[idxs[istr - 1]:idxs[istr]] = np.squeeze(
        mute(
            dat[idxs[istr - 1]:idxs[istr]],
            dt=dt,
            dx=dx,
            v0=v0,
            t0=t0,
            tp=tp,
            half=False,
            hyper=hyper,
        ))
  return mut


def main(args):
  sep = seppy.sep()
  # Read the headers
  _, srcx = sep.read_file(args.srcx)
  _, srcy = sep.read_file(args.srcy)
  _, recx = sep.read_file(args.recx)
  _, recy = sep.read_file(args.recy)
  _, strm = sep.read_file(args.streamer_header)
  _, nrec = sep.read_file(args.nrec_per_shot)
  nrec = nrec.astype('int32')
  nsht = len(nrec)
  # Read the data
  daxes, data = sep.read_file(args.input_data)
  data = data.reshape(daxes.n, order='F').T
  data = np.ascontiguousarray(data).astype('float32')
  nt, ntr = daxes.n
  dt, _ = daxes.d

  # Output data
  smute = np.zeros(data.shape, dtype='float32')

  if args.qc:
    dmin, dmax = np.min(data), np.max(data)

  ntrw = 0
  for isht in tqdm(range(nsht), desc="nsht"):
    smute[ntrw:] = mute_f3shot(
        data[ntrw:],
        srcx[isht],
        srcy[isht],
        nrec[isht],
        strm[ntrw:],
        recx[ntrw:],
        recy[ntrw:],
    )
    if args.qc:
      plot_dat2d(data[ntrw:ntrw + nrec[isht], :1500],
                 show=False,
                 dt=dt,
                 dmin=dmin,
                 dmax=dmax,
                 pclip=0.01,
                 aspect=50)
      plot_dat2d(smute[ntrw:ntrw + nrec[isht], :1500],
                 dt=dt,
                 dmin=dmin,
                 dmax=dmax,
                 pclip=0.01,
                 aspect=50)
    ntrw += nrec[isht]

  sep.write_file(args.output_data, smute.T, os=daxes.o, ds=daxes.d)


def attach_args(parser=argparse.ArgumentParser()):
  parser.add_argument("--input-data", type=str, default=None)
  parser.add_argument("--srcx", type=str, default=None)
  parser.add_argument("--recx", type=str, default=None)
  parser.add_argument("--srcy", type=str, default=None)
  parser.add_argument("--recy", type=str, default=None)
  parser.add_argument("--nrec-per-shot", type=str, default=None)
  parser.add_argument("--streamer-header", type=str, default=None)
  parser.add_argument("--output-data", type=str, default=None)
  parser.add_argument("--water-vel", type=float, default=1450)
  parser.add_argument("--qc", action='store_true', default=False)
  return parser


if __name__ == "__main__":
  main(attach_args().parse_args())
