import argparse
import segyio
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

from regio import seppy


def main(args):
  sep = seppy.sep()

  # Read in the source hash map and the source coordinates
  hmap = np.load(args.src_hash_map, allow_pickle=True)[()]
  crds = np.load(args.src_coords, allow_pickle=True)[()]

  # Grid origin and sampling of the original grid
  ox, oy = 469800, 6072350
  dx, dy = 25, 25

  # Grid origin of the velocity grid
  oxv, oyv = 200, 5
  nxv, nyv = 1000, 500

  # Data sampling
  dt = 0.002

  # Windowed grid
  # Consistent with the windowing of the velocity model
  oxw = ox + oxv * dx
  oyw = oy + oyv * dy

  if args.qc:
    # Read in the migration cube
    maxes, mig = sep.read_file(args.img)
    mig = mig.reshape(maxes.n, order='F')
    # Window the migration cube
    migw = mig[:, oxv:oxv + nxv, oyv:oyv + nyv]
    # Plotting axes
    oxp, oyp = oxw * 0.001, oyw * 0.001
    dxp, dyp = dx * 0.001, dy * 0.001

  # Make a 100X100m grid and loop over each point
  oyw += dy * args.offset_y
  oxw += dx * args.offset_x  # Change coefficients of dy and dx to shift box
  sxs = np.arange(oxw, oxw + (args.nxg - 1) * dx, args.dsx)
  sys = np.arange(oyw, oyw + (args.nyg - 1) * dy, args.dsy)
  nsx = len(sxs)
  nsy = len(sys)

  fcrds = []
  # Remove the shots outside of the region
  for icrd in range(len(crds)):
    if (crds[icrd, 0] >= oyw and crds[icrd, 1] >= oxw):
      fcrds.append(crds[icrd])
  fcrds = np.asarray(fcrds)

  ctr = 0
  dmap = {}
  srcs = set()
  rsxs, rsys = [], []
  with tqdm(total=nsy * nsx, desc='nshots') as pbar:
    for isy in range(nsy):
      gsy = sys[isy]
      for isx in range(nsx):
        pbar.update(1)
        gsx = sxs[isx]
        # Compute the distance between this point and
        # all of the source coordinates
        dists = np.sqrt((gsy - fcrds[:, 0])**2 + (gsx - fcrds[:, 1])**2)
        # Find this coordinate
        idx = np.argmin(dists)
        rsy, rsx = fcrds[idx]
        # If we have seen these source before, keep going
        if ((rsy, rsx) in srcs):
          print("Saw %d %d before, not writing" % (rsy, rsx))
          ctr += 1
          continue
        else:
          srcs.add((rsy, rsx))
        rsys.append(rsy)
        rsxs.append(rsx)
        # Get the key that tells us which files contain the data
        key = str(int(rsy)) + ' ' + str(int(rsx))
        recxinfo, recyinfo = [], []
        strminfo, tidcinfo = [], []
        srcdat = []
        for ifile in hmap[key]:
          if (ifile not in dmap):
            dmap[ifile] = segyio.open(ifile, ignore_geometry=True)
          # Get the source coordinates
          srcxf = np.asarray(
              dmap[ifile].attributes(segyio.TraceField.SourceX),
              dtype='int32',
          )
          srcyf = np.asarray(
              dmap[ifile].attributes(segyio.TraceField.SourceY),
              dtype='int32',
          )
          # Get the receiver coordinates
          recxf = np.asarray(
              dmap[ifile].attributes(segyio.TraceField.GroupX),
              dtype='int32',
          )
          recyf = np.asarray(
              dmap[ifile].attributes(segyio.TraceField.GroupY),
              dtype='int32',
          )
          # Get the streamer header
          strmr = np.asarray(
              dmap[ifile].attributes(segyio.TraceField.CDP_TRACE),
              dtype='int32',
          )
          # Get the trace identification code
          tidcd = np.asarray(
              dmap[ifile].attributes(segyio.TraceField.TraceIdentificationCode),
              dtype='int32',
          )
          # Find the traces with that source coordinate
          scoordsf = np.zeros([len(srcxf), 2], dtype='int32')
          scoordsf[:, 0] = srcyf
          scoordsf[:, 1] = srcxf
          idx1 = scoordsf == fcrds[idx]
          s = np.sum(idx1, axis=1)
          nidx1 = s == 2
          # Get receiver coordinates for this shot
          recxinfo.append(recxf[nidx1])
          recyinfo.append(recyf[nidx1])
          # Get the streamer header for this shot
          strminfo.append(strmr[nidx1])
          # Get the trace identification codes for this shot
          tidcinfo.append(tidcd[nidx1])
          # Get the data for this shot
          data = dmap[ifile].trace.raw[:]
          srcdat.append(data[nidx1, :])
        # Concatenate data from different files
        recxinfo = np.concatenate(recxinfo, axis=0)
        recyinfo = np.concatenate(recyinfo, axis=0)
        strminfo = np.concatenate(strminfo, axis=0)
        tidcinfo = np.concatenate(tidcinfo, axis=0)
        srcdat = np.concatenate(srcdat, axis=0)
        ntr, nt = srcdat.shape
        nrec = len(recxinfo)
        # Skip writing if dead traces
        if (np.all(tidcinfo == 2)):
          print("Bad shot, not writing shot %d %d %d" % (ctr, rsy, rsx))
          ctr += 1
          continue
        # Add the tuple to the set and make sure we have not used it
        if (nrec != len(recyinfo)):
          print("Warning nrecx != nrecy for shot %f %f" % (rsy, rsx))
        if (isy == 0 and isx == 0):
          sep.write_file(args.output_srcx_coords, np.asarray([rsx]))
          sep.write_file(args.output_srcy_coords, np.asarray([rsy]))
          sep.write_file(
              args.output_recx_coords,
              recxinfo.astype('float32'),
          )
          sep.write_file(
              args.output_recy_coords,
              recyinfo.astype('float32'),
          )
          sep.write_file(
              args.output_nrec_per_shot,
              np.asarray([nrec], dtype='float32'),
          )
          sep.write_file(
              args.output_streamer_hdr,
              strminfo.astype('float32'),
          )
          sep.write_file(
              args.output_shots,
              srcdat.T,
              ds=[dt, 1.0],
          )
        else:
          sep.append_file(args.output_srcx_coords, np.asarray([rsx]))
          sep.append_file(args.output_srcy_coords, np.asarray([rsy]))
          sep.append_file(
              args.output_recx_coords,
              recxinfo.astype('float32'),
          )
          sep.append_file(
              args.output_recy_coords,
              recyinfo.astype('float32'),
          )
          sep.append_file(
              args.output_nrec_per_shot,
              np.asarray([nrec], dtype='float32'),
          )
          sep.append_file(
              args.output_streamer_hdr,
              strminfo.astype('float32'),
          )
          sep.append_file(args.output_shots, srcdat.T)
        if args.qc:
          # Plot the source receiver geometry for this shot
          fig = plt.figure(figsize=(10, 5))
          ax = fig.gca()
          ax.imshow(
              np.flipud(migw[args.slc_idx].T),
              extent=[oxp, oxp + nxv * dxp, oyp, oyp + nyv * dyp],
              interpolation='bilinear',
              cmap='gray',
          )
          ax.scatter(
              np.asarray(rsxs) / 1000.0,
              np.asarray(rsys) / 1000.0,
              marker='*',
              color='tab:red',
          )
          ax.scatter(
              recxinfo / 1000.0,
              recyinfo / 1000.0,
              marker='v',
              color='tab:green',
          )
          # Plot the data
          fig = plt.figure()
          ax = fig.gca()
          pclip = 0.05
          dmin = pclip * np.min(srcdat)
          dmax = pclip * np.max(srcdat)
          ax.imshow(
              srcdat.T,
              cmap='gray',
              extent=[0, ntr, nt * dt, 0],
              aspect='auto',
              vmin=dmin,
              vmax=dmax,
          )
          ax.set_xlabel('Receiver no', fontsize=15)
          ax.set_ylabel('Time (s)', fontsize=15)
          ax.tick_params(labelsize=15)
          plt.show()
        ctr += 1

  # Close all of the opened files
  for kvp in dmap.items():
    kvp[1].close()


def attach_args(parser=argparse.ArgumentParser()):
  root_dir = "/net/brick5/data3/northsea_dutch_f3/"
  parser.add_argument(
      "--src-hash-map",
      type=str,
      default=root_dir + "segy/info_new/src_hmap.npy",
  )
  parser.add_argument(
      "--src-coords",
      type=str,
      default=root_dir + "segy/info_new/scoords.npy",
  )
  parser.add_argument("--dsx", type=float, default=100)
  parser.add_argument("--dsy", type=float, default=100)
  parser.add_argument("--nxg", type=int, default=500)
  parser.add_argument("--nyg", type=int, default=500)
  parser.add_argument("--offset-x", type=int, default=0)
  parser.add_argument("--offset-y", type=int, default=0)
  parser.add_argument("--qc", action='store_true', default=False)
  parser.add_argument(
      "--img",
      type=str,
      default=root_dir + "/mig/mig.T",
  )
  parser.add_argument("--slc-idx", type=int, default=400)
  parser.add_argument(
      "--output-srcx-coords",
      type=str,
      default=root_dir + "process_f3_data/windowed_data/f3_srcx_new.H",
  )
  parser.add_argument(
      "--output-srcy-coords",
      type=str,
      default=root_dir + "process_f3_data/windowed_data/f3_srcy_new.H",
  )
  parser.add_argument(
      "--output-recx-coords",
      type=str,
      default=root_dir + "process_f3_data/windowed_data/f3_recx_new.H",
  )
  parser.add_argument(
      "--output-recy-coords",
      type=str,
      default=root_dir + "process_f3_data/windowed_data/f3_recy_new.H",
  )
  parser.add_argument(
      "--output-nrec-per-shot",
      type=str,
      default=root_dir + "process_f3_data/windowed_data/f3_nrec_new.H",
  )
  parser.add_argument(
      "--output-streamer-hdr",
      type=str,
      default=root_dir + "process_f3_data/windowed_data/f3_streamer_new.H",
  )
  parser.add_argument(
      "--output-shots",
      type=str,
      default=root_dir + "/process_f3_data/windowed_data/f3_shots_new.H",
  )
  return parser


if __name__ == "__main__":
  main(attach_args().parse_args())
