import argparse
import numpy as np
import time
import matplotlib.pyplot as plt

from regio import seppy


def main(args):
  sep = seppy.sep()
  saxes, srcs = sep.read_file(args.src_coords)
  srcs = srcs.reshape(saxes.n, order='F')
  srcy = srcs[:, 0]
  srcx = srcs[:, 1]

  beg = time.time()
  usrcs = np.unique(srcs, axis=0)
  usrcy = usrcs[:, 0]
  usrcx = usrcs[:, 1]
  if args.verb:
    print("Computed unique src coordinates in %f s" % (time.time() - beg),
          flush=True)

  raxes, recs = sep.read_file(args.rec_coords)
  recs = recs.reshape(raxes.n, order='F')
  recy = recs[:, 0]
  recx = recs[:, 1]

  beg = time.time()
  urecs = np.unique(recs, axis=0)
  urecy = urecs[:, 0]
  urecx = urecs[:, 1]
  if args.verb:
    print("Computed unique rec coordinates in %f s" % (time.time() - beg),
          flush=True)

  # Calculate midpoints
  mptx = (srcx + recx) / 2.0
  mpty = (srcy + recy) / 2.0

  beg = time.time()
  mpts = np.zeros(recs.shape, dtype='float32')
  mpts[:, 0] = mpty
  mpts[:, 1] = mptx
  umpts = np.unique(mpts, axis=0)
  umpty = umpts[:, 0]
  umptx = umpts[:, 1]
  if args.verb:
    print("Computed unique mpt coordinates in %f s" % (time.time() - beg),
          flush=True)

  # Read in migration cube
  maxes, mig = sep.read_file(args.img)
  nz, nx, ny = maxes.n
  oz, ox, oy = maxes.o
  dz, dx, dy = maxes.d
  dx *= 1000
  dy *= 1000
  mig = mig.reshape(maxes.n, order='F')
  ox = 469800.0
  oy = 6072350.0

  if args.verb:
    print("Src extent: Min_Y=%d Min_X=%d Max_Y=%d Max_X=%d" %
          (np.min(srcy), np.min(srcx), np.max(srcy), np.max(srcx)))
    print("Rec extent: Min_Y=%d Min_X=%d Max_Y=%d Max_X=%d" %
          (np.min(recy), np.min(recx), np.max(recy), np.max(recx)))
    print("Mpt extent: Min_Y=%.2f Min_X=%.2f Max_Y=%.2f Max_X=%.2f" %
          (np.min(mpty), np.min(mptx), np.max(mpty), np.max(mptx)))

  fig = plt.figure(figsize=(15, 10))
  ax = fig.gca()
  ax.imshow(
      np.flipud(seppy.bytes2float(mig[args.slc_idx].T)),
      cmap='gray',
      extent=[ox, ox + nx * dx, oy, oy + ny * dy],
  )
  ax.scatter(
      usrcx[::args.skip],
      usrcy[::args.skip],
      marker='*',
      color='tab:red',
  )
  ax.set_xlabel('X (km)', fontsize=15)
  ax.set_ylabel('Y (km)', fontsize=15)
  ax.set_title('Source locations: OriginX=%.1f OriginY=%.1f' % (ox, oy),
               fontsize=15)
  ax.tick_params(labelsize=15)
  if args.show:
    plt.show()
  plt.savefig(
      args.output_src_fig,
      dpi=150,
      transparent=False,
      bbox_inches='tight',
  )
  plt.close()

  # Remove receiver below bottom boundary
  # this cannot be used in imaging as we do not
  # have the velocity here
  idx = np.where(urecy < oy)
  purecy = np.delete(urecy, idx)
  purecx = np.delete(urecx, idx)
  fig = plt.figure(figsize=(15, 10))
  ax = fig.gca()
  ax.imshow(
      np.flipud(seppy.bytes2float(mig[args.slc_idx].T)),
      cmap='gray',
      extent=[ox, ox + nx * dx, oy, oy + ny * dy],
  )
  ax.scatter(
      purecx[::args.skip],
      purecy[::args.skip],
      marker='v',
      color='tab:green',
      s=20,
  )
  ax.set_xlabel('X (km)', fontsize=15)
  ax.set_ylabel('Y (km)', fontsize=15)
  ax.tick_params(labelsize=15)
  ax.set_title('Receiver locations: OriginX=%.1f OriginY=%.1f' % (ox, oy),
               fontsize=15)
  if args.show:
    plt.show()
  plt.savefig(
      args.output_rec_fig,
      dpi=150,
      transparent=False,
      bbox_inches='tight',
  )
  plt.close()

  fig = plt.figure(figsize=(15, 10))
  ax = fig.gca()
  ax.imshow(
      np.flipud(seppy.bytes2float(mig[args.slc_idx].T)),
      cmap='gray',
      extent=[ox, ox + nx * dx, oy, oy + ny * dy],
  )
  ax.scatter(umptx[::args.skip], umpty[::args.skip], color='tab:orange', s=20)
  ax.set_xlabel('X (km)', fontsize=15)
  ax.set_ylabel('Y (km)', fontsize=15)
  ax.set_title('Midpoint locations: OriginX=%.1f OriginY=%.1f' % (ox, oy),
               fontsize=15)
  ax.tick_params(labelsize=15)
  if args.show:
    plt.show()
  plt.savefig(
      args.output_mpt_fig,
      dpi=150,
      transparent=False,
      bbox_inches='tight',
  )
  plt.close()


def attach_args(parser=argparse.ArgumentParser()):
  parser.add_argument("--src-coords", type=str, default="./all_src_coords.H")
  parser.add_argument("--rec-coords", type=str, default="./all_rec_coords.H")
  parser.add_argument(
      "--img",
      type=str,
      default="/net/brick5/data3/northsea_dutch_f3/mig/mig.T",
  )
  parser.add_argument("--slc-idx", type=int, default=400)
  parser.add_argument(
      "--output-src-fig",
      type=str,
      default="./fig/src_coords.png",
  )
  parser.add_argument(
      "--output-rec-fig",
      type=str,
      default="./fig/rec_coords.png",
  )
  parser.add_argument(
      "--output-mpt-fig",
      type=str,
      default="./fig/mpt_coords.png",
  )
  parser.add_argument("--skip", type=int, default=1)
  parser.add_argument("--verb", action='store_true', default=False)
  parser.add_argument("--show", action='store_true', default=False)
  return parser


if __name__ == "__main__":
  main(attach_args().parse_args())
