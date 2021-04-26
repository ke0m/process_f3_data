import argparse
import os
import segyio
from mpi4py import MPI
import numpy as np
from tqdm import tqdm

from regio import seppy
from utils import chunks


def _get_src_rec_coords(rank, segys):
  allscoords, allrcoords = [], []
  with tqdm(total=len(segys), desc='%d nsegy' % (rank),
            position=rank + 1) as pbar:
    for isegy in segys:
      # Read in the SEGY
      datsgy = segyio.open(isegy, ignore_geometry=True)

      # Get the coordinates
      srcx = np.asarray(datsgy.attributes(segyio.TraceField.SourceX),
                        dtype='int32')
      srcy = np.asarray(datsgy.attributes(segyio.TraceField.SourceY),
                        dtype='int32')
      recx = np.asarray(datsgy.attributes(segyio.TraceField.GroupX),
                        dtype='int32')
      recy = np.asarray(datsgy.attributes(segyio.TraceField.GroupY),
                        dtype='int32')

      srccoords = np.zeros([len(srcx), 2], dtype='int')
      reccoords = np.zeros([len(recx), 2], dtype='int')

      srccoords[:, 0] = srcy
      srccoords[:, 1] = srcx

      reccoords[:, 0] = recy
      reccoords[:, 1] = recx

      allscoords.append(srccoords)
      allrcoords.append(reccoords)

      pbar.update(1)

  allscoords = np.concatenate(allscoords, axis=0).astype('float32')
  allrcoords = np.concatenate(allrcoords, axis=0).astype('float32')
  return {'src': allscoords, 'rec': allrcoords, 'rank': rank}


def main(args):
  comm = MPI.COMM_WORLD

  rank = comm.Get_rank()
  size = comm.Get_size()

  if rank == 0:
    segys = [
        os.path.join(args.segy, isegy)
        for isegy in os.listdir(args.segy)
        if '.segy' in isegy
    ]
    segy_chunks = chunks(segys, size)
  else:
    segy_chunks = None

  segy_chunk = comm.scatter(segy_chunks, root=0)

  srcoords = _get_src_rec_coords(rank, segy_chunk)

  all_srcoords = comm.gather(srcoords, root=0)

  if rank == 0:
    all_scoords, all_rcoords = [], []
    for srcoord in all_srcoords:
      all_scoords.append(srcoord['src'])
      all_rcoords.append(srcoord['rec'])

    all_scoords = np.concatenate(all_scoords, axis=0).astype('float32')
    all_rcoords = np.concatenate(all_rcoords, axis=0).astype('float32')

  if rank == 0:
    sep = seppy.sep()
    sep.write_file(args.src_coords, all_scoords)
    sep.write_file(args.rec_coords, all_rcoords)

    if args.unique_src_coords is not None:
      uscoords = np.unique(all_scoords, axis=0)
      sep.write_file(args.unique_src_coords, uscoords)


def attach_args(parser=argparse.ArgumentParser()):
  parser.add_argument(
      "--segy",
      type=str,
      default="/net/brick5/data3/northsea_dutch_f3/segy",
      help="Path to segy files",
  )
  parser.add_argument(
      "--src-coords",
      type=str,
      default=None,
      required=True,
      help="Output source coordinates",
  )
  parser.add_argument(
      "--unique-src-coords",
      type=str,
      default=None,
      required=False,
      help="Output unique source coordinates",
  )
  parser.add_argument(
      "--rec-coords",
      type=str,
      default=None,
      required=True,
      help="Output receiver coordinates",
  )

  return parser


if __name__ == "__main__":
  main(attach_args().parse_args())
