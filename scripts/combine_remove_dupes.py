import argparse
import os
import numpy as np
from tqdm import tqdm

from regio import seppy


def _find_duplicates(all_srcx, all_srcy):
  scoords = np.zeros([len(all_srcx), 2], dtype='float32')
  scoords[:, 0], scoords[:, 1] = all_srcx, all_srcy

  uscoords, idx = np.unique(scoords, axis=0, return_index=True)

  # Compute mask to get indices of duplicates
  m = np.zeros(len(all_srcx), dtype=bool)
  m[idx] = True

  dupes = scoords[~m].tolist()

  return {'(%d, %d)' % (icrd[0], icrd[1]): 0 for icrd in dupes}


def _read_data(data_dir, suffix, bases, sep):
  odict = {}
  for base in bases:
    file_base = os.path.join(data_dir, base)
    daxes, dat = sep.read_file(file_base + suffix)
    if base == 'f3_shots':
      dat = dat.reshape(daxes.n, order='F').T
    elif base == 'f3_nrec':
      dat = dat.astype('int32')
    odict[base] = dat

  return odict


def main(args):
  suffixes = sorted([
      ifile.split('f3_shots')[-1]
      for ifile in os.listdir(args.data_dir)
      if 'f3_shots' in ifile
  ])

  sep = seppy.sep()
  keys = [
      'f3_shots', 'f3_srcx', 'f3_srcy', 'f3_recx', 'f3_recy', 'f3_nrec',
      'f3_strm'
  ]

  # Load in all of the source coordinates
  all_srcx, all_srcy = [], []
  for k, suffix in enumerate(tqdm(suffixes, desc='rank')):
    srcx_base = os.path.join(args.data_dir, 'f3_srcx')
    _, srcx = sep.read_file(srcx_base + suffix)
    srcy_base = os.path.join(args.data_dir, 'f3_srcy')
    _, srcy = sep.read_file(srcy_base + suffix)
    all_srcx.append(srcx)
    all_srcy.append(srcy)

  # Find all duplicate coordinates
  all_srcx = np.concatenate(all_srcx, axis=0)
  all_srcy = np.concatenate(all_srcy, axis=0)
  dup_dict = _find_duplicates(all_srcx, all_srcy)

  # Loop over all data
  ddict = {key: [] for key in keys}
  for k, suffix in tqdm(enumerate(suffixes), desc='rank', total=len(suffixes)):
    alldat = _read_data(args.data_dir, suffix, keys, sep)

    ctr = 0
    odict = {key: [] for key in keys}
    srcxs, srcys = alldat['f3_srcx'].tolist(), alldat['f3_srcy'].tolist()
    for k, (sidx, sidy) in enumerate(zip(srcxs, srcys)):
      crd = '(%d, %d)' % (sidx, sidy)
      if crd in dup_dict.keys():
        if dup_dict[crd] == 0:
          nrec = alldat['f3_nrec'][k]
          odict['f3_srcx'].append(alldat['f3_srcx'][k])
          odict['f3_srcy'].append(alldat['f3_srcy'][k])
          odict['f3_nrec'].append(nrec)
          odict['f3_shots'].append(alldat['f3_shots'][ctr:ctr + nrec])
          odict['f3_recx'].append(alldat['f3_recx'][ctr:ctr + nrec])
          odict['f3_recy'].append(alldat['f3_recy'][ctr:ctr + nrec])
          dup_dict[crd] += 1
        else:
          ddict['f3_srcx'].append(alldat['f3_srcx'][k])
          ddict['f3_srcy'].append(alldat['f3_srcy'][k])
          ddict['f3_nrec'].append(nrec)
          ddict['f3_shots'].append(alldat['f3_shots'][ctr:ctr + nrec])
          ddict['f3_recx'].append(alldat['f3_recx'][ctr:ctr + nrec])
          ddict['f3_recy'].append(alldat['f3_recy'][ctr:ctr + nrec])
      else:
        nrec = alldat['f3_nrec'][k]
        odict['f3_srcx'].append(alldat['f3_srcx'][k])
        odict['f3_srcy'].append(alldat['f3_srcy'][k])
        odict['f3_nrec'].append(nrec)
        odict['f3_shots'].append(alldat['f3_shots'][ctr:ctr + nrec])
        odict['f3_recx'].append(alldat['f3_recx'][ctr:ctr + nrec])
        odict['f3_recy'].append(alldat['f3_recy'][ctr:ctr + nrec])
      ctr += alldat['f3_nrec'][k]

    # Srcx coordinates
    usrcx = np.asarray(odict['f3_srcx'], dtype='float32')
    name = os.path.join(args.output_dir, 'f3_srcx') + args.output_prefix + suffix
    sep.write_file(name, usrcx)
    # Srcy coordinates
    usrcy = np.asarray(odict['f3_srcy'], dtype='float32')
    name = os.path.join(args.output_dir, 'f3_srcy') + args.output_prefix + suffix
    sep.write_file(name, usrcy)
    # Num receivers per shot
    unrec = np.asarray(odict['f3_nrec'], dtype='float32')
    name = os.path.join(args.output_dir, 'f3_nrec') + args.output_prefix + suffix
    sep.write_file(name, unrec)
    # Shots
    udata = np.concatenate(odict['f3_shots'], axis=0)
    name = os.path.join(args.output_dir, 'f3_shots') + args.output_prefix + suffix
    sep.write_file(name, udata.T, ds=[0.002, 1.0], os=[0.0, 0.0])
    # Recx coordinates
    urecx = np.concatenate(odict['f3_recx'], axis=0)
    name = os.path.join(args.output_dir, 'f3_recx') + args.output_prefix + suffix
    sep.write_file(name, urecx)
    # Recy coordinates
    urecy = np.concatenate(odict['f3_recy'], axis=0)
    name = os.path.join(args.output_dir, 'f3_recy') + args.output_prefix + suffix
    sep.write_file(name, urecy)


def attach_args(parser=argparse.ArgumentParser()):
  parser.add_argument("--data-dir", type=str, default=None)
  parser.add_argument("--output-prefix", type=str, default='_clean')
  parser.add_argument("--output-dir", type=str, default=None)
  return parser


if __name__ == "__main__":
  main(attach_args().parse_args())
