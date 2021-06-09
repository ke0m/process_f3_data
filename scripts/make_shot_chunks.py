import os
import argparse
import numpy as np
from tqdm import tqdm

from regio import seppy
from adf.gradopt.utils import create_inttag


def main(args):
  sep = seppy.sep()

  # First read in srcx, srcy, nrec
  _, all_srcx = sep.read_file(args.all_srcx)
  _, all_srcy = sep.read_file(args.all_srcy)
  _, all_nrec = sep.read_file(args.all_nrec)
  all_nrec = all_nrec.astype('int32')

  _, all_recx = sep.read_file(args.all_recx)
  _, all_recy = sep.read_file(args.all_recy)
  _, all_strm = sep.read_file(args.all_strm)

  total_shots = len(all_srcx)
  nchunks = int(total_shots / args.chunk_size + 0.5)

  begsht, endsht = 0, args.chunk_size
  begtr, endtr = 0, 0
  for ichunk in tqdm(range(nchunks), desc='nchunks'):
    # Window the headers
    srcx_chunk = all_srcx[begsht:endsht]
    srcy_chunk = all_srcy[begsht:endsht]
    nrec_chunk = all_nrec[begsht:endsht]
    endtr += np.sum(nrec_chunk)
    recx_chunk = all_recx[begtr:endtr]
    recy_chunk = all_recy[begtr:endtr]
    strm_chunk = all_strm[begtr:endtr]
    # Read in a data chunk
    daxes, dat = sep.read_wind(args.all_shots, fw=begtr, nw=len(recx_chunk))
    dat = dat.reshape(daxes.n, order='F')
    # Write chunks to file
    tag = create_inttag(ichunk, nchunks)
    chunk_dir = os.path.join(args.output_dir, 'chunk_' + tag)
    if not os.path.isdir(chunk_dir):
      os.mkdir(chunk_dir)
    if not args.to_npy:
      sep.write_file(
          os.path.join(chunk_dir, 'f3_srcx_' + args.string_id + tag + '.H'),
          srcx_chunk.astype('float32'),
      )
      sep.write_file(
          os.path.join(chunk_dir, 'f3_srcy_' + args.string_id + tag + '.H'),
          srcy_chunk.astype('float32'),
      )
      sep.write_file(
          os.path.join(chunk_dir, 'f3_nrec_' + args.string_id + tag + '.H'),
          nrec_chunk.astype('float32'),
      )
      sep.write_file(
          os.path.join(chunk_dir, 'f3_recx_' + args.string_id + tag + '.H'),
          recx_chunk.astype('float32'),
      )
      sep.write_file(
          os.path.join(chunk_dir, 'f3_recy_' + args.string_id + tag + '.H'),
          recy_chunk.astype('float32'),
      )
      sep.write_file(
          os.path.join(chunk_dir, 'f3_strm_' + args.string_id + tag + '.H'),
          strm_chunk.astype('float32'),
      )
      sep.write_file(
          os.path.join(chunk_dir, 'f3_shots_' + args.string_id + tag + '.H'),
          dat.astype('float32'),
          os=daxes.o,
          ds=daxes.d,
      )
    else:
      odict = {}
      odict['dt'] = daxes.d[0]
      odict['f3_shots'] = np.ascontiguousarray(dat.T).astype('float32')
      odict['f3_nrec'] = nrec_chunk.astype('int32')
      odict['f3_srcx'] = srcx_chunk.astype('float32')
      odict['f3_srcy'] = srcy_chunk.astype('float32')
      odict['f3_recx'] = recx_chunk.astype('float32')
      odict['f3_recy'] = recy_chunk.astype('float32')
      np.save(
          os.path.join(chunk_dir, 'chunk_' + args.string_id + tag + '.npy'),
          odict,
      )
    # Update counters
    begsht = endsht
    endsht += args.chunk_size
    begtr = endtr


def attach_args(parser=argparse.ArgumentParser()):
  path = "/net/brick5/data3/northsea_dutch_f3/process_f3_data/windowed_data"
  parser.add_argument(
      "--all-shots",
      type=str,
      default=os.path.join(path, 'all/f3_shots_all_combined_interp.H'),
  )
  parser.add_argument(
      "--all-srcx",
      type=str,
      default=os.path.join(path, 'all/f3_srcx_all_combined.H'),
  )
  parser.add_argument(
      "--all-srcy",
      type=str,
      default=os.path.join(path, 'all/f3_srcy_all_combined.H'),
  )
  parser.add_argument(
      "--all-recx",
      type=str,
      default=os.path.join(path, 'all/f3_recx_all_combined.H'),
  )
  parser.add_argument(
      "--all-recy",
      type=str,
      default=os.path.join(path, 'all/f3_recy_all_combined.H'),
  )
  parser.add_argument(
      "--all-nrec",
      type=str,
      default=os.path.join(path, 'all/f3_nrec_all_combined.H'),
  )
  parser.add_argument(
      "--all-strm",
      type=str,
      default=os.path.join(path, 'all/f3_strm_all_combined.H'),
  )
  parser.add_argument("--string-id", type=str, default=None)
  parser.add_argument("--to-npy", action='store_true', default=False)
  parser.add_argument("--chunk-size", type=int, default=100)
  parser.add_argument(
      "--output-dir",
      type=str,
      default=os.path.join(path, 'all/chunks/'),
  )
  return parser


if __name__ == "__main__":
  main(attach_args().parse_args())
