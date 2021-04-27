import argparse
import segyio
import numpy as np
from mpi4py import MPI
from tqdm import tqdm
import logging

from regio import seppy
from utils import chunks


def _process_inline(
    sychunk,
    sxs,
    fcrds,
    hmap,
    fnames,
    rank,
    dt=0.002,
    logdir='./log',
):

  # Create a logger
  logging.basicConfig(
      filename='%s/rank-%d.log' % (logdir, rank),
      level=logging.INFO,
      format='%(asctime)s - %(filename)s:%(lineno)d - %(message)s',
  )

  # Write SEP files
  sep = seppy.sep()

  dmap = {}
  srcs = set()
  rsxs, rsys = [], []
  nsy, nsx = len(sychunk), len(sxs)
  ymin, ymax = np.min(sychunk), np.max(sychunk)
  logging.info('Ymin: %d Ymax: %d' % (ymin, ymax))
  with tqdm(total=nsy * nsx,
            desc='rank %d nshots' % (rank),
            position=rank + 1,
            nrows=40) as pbar:
    # Loop over chunks
    for isy in range(nsy):
      gsy = sychunk[isy]
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
          logging.info("Saw %d %d before, not writing" % (rsy, rsx))
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
          logging.info("Bad shot, not writing shot %d %d" % (rsy, rsx))
          continue
        # Add the tuple to the set and make sure we have not used it
        if (nrec != len(recyinfo)):
          logging.warning("Warning nrecx != nrecy for shot %f %f" % (rsy, rsx))
        if (isy == 0 and isx == 0):
          sep.write_file(fnames['srcx'] % (ymin, ymax), np.asarray([rsx]))
          sep.write_file(fnames['srcy'] % (ymin, ymax), np.asarray([rsy]))
          sep.write_file(
              fnames['recx'] % (ymin, ymax),
              recxinfo.astype('float32'),
          )
          sep.write_file(
              fnames['recy'] % (ymin, ymax),
              recyinfo.astype('float32'),
          )
          sep.write_file(
              fnames['nrec'] % (ymin, ymax),
              np.asarray([nrec], dtype='float32'),
          )
          sep.write_file(
              fnames['streamer'] % (ymin, ymax),
              strminfo.astype('float32'),
          )
          sep.write_file(
              fnames['shots'] % (ymin, ymax),
              srcdat.T,
              ds=[dt, 1.0],
          )
        else:
          sep.append_file(fnames['srcx'] % (ymin, ymax), np.asarray([rsx]))
          sep.append_file(fnames['srcy'] % (ymin, ymax), np.asarray([rsy]))
          sep.append_file(
              fnames['recx'] % (ymin, ymax),
              recxinfo.astype('float32'),
          )
          sep.append_file(
              fnames['recy'] % (ymin, ymax),
              recyinfo.astype('float32'),
          )
          sep.append_file(
              fnames['nrec'] % (ymin, ymax),
              np.asarray([nrec], dtype='float32'),
          )
          sep.append_file(
              fnames['streamer'] % (ymin, ymax),
              strminfo.astype('float32'),
          )
          sep.append_file(fnames['shots'] % (ymin, ymax), srcdat.T)

  # Close all of the opened files
  for kvp in dmap.items():
    kvp[1].close()


def main(args):
  comm = MPI.COMM_WORLD

  rank = comm.Get_rank()
  size = comm.Get_size()

  if rank == 0:
    # Read in the source hash map and the source coordinates
    hmap = np.load(args.src_hash_map, allow_pickle=True)[()]
    crds = np.load(args.src_coords, allow_pickle=True)[()]

    # Grid origin and sampling of the original grid
    ox, oy = 469800, 6072350
    dx, dy = 25, 25

    # Grid origin of the velocity grid
    oxv, oyv = 200, 5

    # Data sampling
    dt = 0.002

    # Windowed grid
    # Consistent with the windowing of the velocity model
    oxw = ox + oxv * dx
    oyw = oy + oyv * dy

    # Make a 100X100m grid and loop over each point
    oyw += dy * args.offset_y
    oxw += dx * args.offset_x  # Change coefficients of dy and dx to shift box
    sxs = np.arange(oxw, oxw + (args.nxg - 1) * dx, args.dsx)
    sys = np.arange(oyw, oyw + (args.nyg - 1) * dy, args.dsy)

    fcrds = []
    # Remove the shots outside of the region
    for icrd in range(len(crds)):
      if (crds[icrd, 0] >= oyw and crds[icrd, 1] >= oxw):
        fcrds.append(crds[icrd])
    fcrds = np.asarray(fcrds)

    fnames = {
        'srcx': args.output_base_srcx_coords,
        'srcy': args.output_base_srcy_coords,
        'recx': args.output_base_recx_coords,
        'recy': args.output_base_recy_coords,
        'nrec': args.output_base_nrec_per_shot,
        'streamer': args.output_base_streamer_hdr,
        'shots': args.output_base_shots,
    }
    sychunks = chunks(sys, size)
    allchunks = [{
        'sychunk': icnk,
        'sxs': sxs,
        'fcrds': fcrds,
        'hmap': hmap,
        'fnames': fnames,
        'dt': dt,
    } for icnk in sychunks]
  else:
    allchunks = None

  local_chunk = comm.scatter(allchunks, root=0)

  _process_inline(
      local_chunk['sychunk'],
      local_chunk['sxs'],
      local_chunk['fcrds'],
      local_chunk['hmap'],
      local_chunk['fnames'],
      rank,
      local_chunk['dt'],
  )


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
      "--output-base-srcx-coords",
      type=str,
      default=root_dir + "process_f3_data/windowed_data/f3_srcx_new_%d.H",
  )
  parser.add_argument(
      "--output-base-srcy-coords",
      type=str,
      default=root_dir + "process_f3_data/windowed_data/f3_srcy_new_%d.H",
  )
  parser.add_argument(
      "--output-base-recx-coords",
      type=str,
      default=root_dir + "process_f3_data/windowed_data/f3_recx_new_%d.H",
  )
  parser.add_argument(
      "--output-base-recy-coords",
      type=str,
      default=root_dir + "process_f3_data/windowed_data/f3_recy_new_%d.H",
  )
  parser.add_argument(
      "--output-base-nrec-per-shot",
      type=str,
      default=root_dir + "process_f3_data/windowed_data/f3_nrec_new_%d.H",
  )
  parser.add_argument(
      "--output-base-streamer-hdr",
      type=str,
      default=root_dir + "process_f3_data/windowed_data/f3_streamer_%d.H",
  )
  parser.add_argument(
      "--output-base-shots",
      type=str,
      default=root_dir + "/process_f3_data/windowed_data/f3_shots_new_%d.H",
  )
  return parser


if __name__ == "__main__":
  main(attach_args().parse_args())
