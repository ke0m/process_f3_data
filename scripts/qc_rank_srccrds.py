import argparse
import os
import numpy as np
import matplotlib.pyplot as plt

from regio import seppy


def main(args):
  srcx_files = sorted([
      os.path.join(args.data_dir, ifile)
      for ifile in os.listdir(args.data_dir)
      if 'srcx' in ifile
  ])
  srcy_files = sorted([
      os.path.join(args.data_dir, ifile)
      for ifile in os.listdir(args.data_dir)
      if 'srcy' in ifile
  ])

  sep = seppy.sep()
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
  ny, nx = slcw.shape

  all_srcys, all_srcxs = [], []
  fig = plt.figure(figsize=(14, 7))
  for srcx_file, srcy_file in zip(srcx_files, srcy_files):
    saxes, srcx = sep.read_file(srcx_file)
    saxes, srcy = sep.read_file(srcy_file)
    srcx *= 0.001
    srcy *= 0.001
    all_srcxs.append(srcx)
    all_srcys.append(srcy)

    ax = fig.gca()
    ax.imshow(
        np.flipud(slcw),
        cmap='gray',
        extent=[oxw, oxw + nx * dx, oyw, oyw + ny * dy],
    )
    ax.scatter(srcx, srcy, marker='*', c='tab:red')
    ax.set_xlabel('X (km)', fontsize=15)
    ax.set_ylabel('Y (km)', fontsize=15)
    ax.tick_params(labelsize=15)
  plt.show()

  all_srcxs = np.concatenate(all_srcxs, axis=0)
  all_srcys = np.concatenate(all_srcys, axis=0)

  scoords = np.zeros([len(all_srcxs), 2], dtype='float32')
  scoords[:, 0] = all_srcxs
  scoords[:, 1] = all_srcys
  uscoords, counts = np.unique(scoords, axis=0, return_counts=True)

  print(scoords.shape)
  print(uscoords.shape)


def attach_args(parser=argparse.ArgumentParser()):
  parser.add_argument("--data-dir", type=str, default=None)
  parser.add_argument(
      "--img",
      type=str,
      default="/net/brick5/data3/northsea_dutch_f3/mig/mig.T",
  )
  parser.add_argument("--slc-idx", type=int, default=400)
  return parser


if __name__ == "__main__":
  main(attach_args().parse_args())
