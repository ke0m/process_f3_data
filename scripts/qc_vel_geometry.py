import argparse
import numpy as np
import matplotlib.pyplot as plt

from regio import seppy
from sivu.movie import viewcube3d


def main(args):
  sep = seppy.sep()
  # Read in geometry
  _, srcx = sep.read_file(args.srcx)
  srcx *= 0.001
  _, srcy = sep.read_file(args.srcy)
  srcy *= 0.001
  _, recx = sep.read_file(args.recx)
  recx *= 0.001
  _, recy = sep.read_file(args.recy)
  recy *= 0.001
  # Velocity model
  vaxes, vel = sep.read_file(args.vel_model)
  vel = vel.reshape(vaxes.n, order='F').T
  ny, nx, nz = vel.shape
  dz, dx, dy = vaxes.d
  oz, ox, oy = vaxes.o
  velw = vel[args.beg_inline_idx:args.end_inline_idx, :args.
             max_xline_idx, :args.max_depth_idx]
  nyw, nxw, nzw = velw.shape
  oyw = oy + args.beg_inline_idx * dy
  # [ny,nx,nz] -> [nz,ny,nx]
  velwt = np.ascontiguousarray(np.transpose(velw, (2, 0, 1)))

  # Image cube for context
  iaxes, img = sep.read_file(args.img_cube)
  img = img.reshape(iaxes.n, order='F').T
  img = img[:, 200:1200, 5:505]
  imgw = img[
      args.beg_inline_idx:args.end_inline_idx, :args.max_xline_idx, :1000]
  imgwt = np.ascontiguousarray(np.transpose(imgw, (2, 0, 1)))

  fig = plt.figure(figsize=(14, 7))
  ax = fig.gca()
  im = ax.imshow(
      np.flipud(velwt[args.vel_slice_idx]),
      cmap='jet',
      interpolation='bilinear',
      extent=[ox, ox + nxw * dx, oyw, oyw + nyw * dy],
      vmin=np.min(velwt),
      vmax=np.max(velwt),
  )
  ax.scatter(srcx[:4], srcy[:4], c='tab:red', marker='*')
  ax.set_xlabel('X (km)', fontsize=15)
  ax.set_ylabel('Y (km)', fontsize=15)
  ax.tick_params(labelsize=15)
  cbar_ax = fig.add_axes()
  cbar = fig.colorbar(im, cbar_ax, format='%.2f')
  cbar.ax.tick_params(labelsize=15)
  cbar.set_label('Velocity (km/s)', fontsize=15)

  fig = plt.figure(figsize=(14, 7))
  ax = fig.gca()
  im = ax.imshow(
      np.flipud(imgwt[400]),
      cmap='gray',
      interpolation='bilinear',
      extent=[ox, ox + nxw * dx, oyw, oyw + nyw * dy],
  )
  ax.scatter(srcx[:4], srcy[:4], c='tab:red', marker='*')
  ax.set_xlabel('X (km)', fontsize=15)
  ax.set_ylabel('Y (km)', fontsize=15)
  ax.tick_params(labelsize=15)

  viewcube3d(
      velwt,
      os=[0.0, ox, oyw],
      ds=[dz, dx, dy],
      cmap='jet',
      cbar=True,
      show=False,
  )
  viewcube3d(imgwt, os=[0.0, ox, oyw], ds=[dz, dx, dy])


def attach_args(parser=argparse.ArgumentParser()):
  parser.add_argument("--srcx", type=str, default=None)
  parser.add_argument("--srcy", type=str, default=None)
  parser.add_argument("--recx", type=str, default=None)
  parser.add_argument("--recy", type=str, default=None)
  parser.add_argument("--vel-model", type=str, default=None)
  parser.add_argument("--img-cube", type=str, default=None)
  parser.add_argument("--beg-inline-idx", type=int, default=0)
  parser.add_argument("--end-inline-idx", type=int, default=500)
  parser.add_argument("--max-xline-idx", type=int, default=500)
  parser.add_argument("--max-depth-idx", type=int, default=1000)
  parser.add_argument("--vel-slice-idx", type=int, default=500)
  return parser


if __name__ == "__main__":
  main(attach_args().parse_args())
