import os
import argparse
import segyio
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from regio import seppy


def main(args):
  segys = sorted([
      os.path.join(args.segy, isegy)
      for isegy in os.listdir(args.segy)
      if '.segy' in isegy
  ])
  if not os.path.isdir(args.output_info_dir):
    os.mkdir(args.output_info_dir)

  if args.qc:
    sep = seppy.sep()
    maxes, mig = sep.read_file(args.img)
    nt, nx, ny = maxes.n
    dt, dx, dy = maxes.d
    dx *= 1000
    dy *= 1000
    mig = mig.reshape(maxes.n, order='F')
    # Imaging origin
    ox = 469800.0
    oy = 6072350.0

  for segy in tqdm(segys, desc="nsegy"):
    datsgy = segyio.open(segy, ignore_geometry=True)

    # Get the coordinates
    srcx = np.asarray(datsgy.attributes(segyio.TraceField.SourceX),
                      dtype='int32')
    srcy = np.asarray(datsgy.attributes(segyio.TraceField.SourceY),
                      dtype='int32')
    srccoords = np.zeros([len(srcx), 2], dtype='int')
    srccoords[:, 0] = srcy
    srccoords[:, 1] = srcx

    ucoords, cts = np.unique(srccoords, axis=0, return_counts=True)
    nsht = ucoords.shape[0]

    if args.qc:
      # Plot the source coordinates
      fig = plt.figure(figsize=(10, 10))
      ax = fig.gca()
      ax.imshow(
          np.flipud(seppy.bytes2float(mig[args.slc_idx].T)),
          cmap='gray',
          extent=[ox, ox + nx * dx, oy, oy + ny * dy],
      )
      ax.scatter(ucoords[:, 1], ucoords[:, 0], marker='*', color='tab:red')
      ax.set_xlabel('X (km)', fontsize=15)
      ax.set_ylabel('Y (km)', fontsize=15)
      ax.tick_params(labelsize=15)
      plt.show()

    # Loop over unique coordinates and write to file
    bname = os.path.basename(segy)
    fname = os.path.splitext(bname)[0]
    ofile = os.path.join(args.output_info_dir, fname + '.txt')
    with open(ofile, 'w') as f:
      for icrd in range(nsht):
        f.write('%d %d %d\n' % (ucoords[icrd, 0], ucoords[icrd, 1], cts[icrd]))


def attach_args(parser=argparse.ArgumentParser()):
  parser.add_argument(
      "--segy",
      type=str,
      default="/net/brick5/data3/northsea_dutch_f3/segy",
      help="Path to segy files",
  )
  parser.add_argument(
      "--output-info-dir",
      type=str,
      default="/net/brick5/data3/northsea_dutch_f3/segy/info_new",
  )
  parser.add_argument("--qc", action="store_true", default=False)
  parser.add_argument(
      "--img",
      type=str,
      default="/net/brick5/data3/northsea_dutch_f3/mig/mig.T",
  )
  parser.add_argument("--slc-idx", type=int, default=400)
  return parser


if __name__ == "__main__":
  main(attach_args().parse_args())
