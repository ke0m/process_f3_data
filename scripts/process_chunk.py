import os
import argparse
import numpy as np
import subprocess

from regio import seppy


def main(args):
  # Get the file names for this chunk
  files = os.listdir(args.chunk_dir)
  files = list(filter(lambda f: '.H' in f, files))
  files = list(
      filter(
          lambda f: 'mute' not in f and 'debubble' not in f and 'processed'
          not in f and 'gnc' not in f, files))

  keys = [
      'f3_shots', 'f3_srcx', 'f3_recx', 'f3_srcy', 'f3_recy', 'f3_nrec',
      'f3_strm'
  ]

  ddict = {
      key: os.path.join(args.chunk_dir, ifile)
      for key in keys for ifile in files if key in ifile
  }

  suffix = ddict['f3_shots'].split('f3_shots')[-1]

  # First mute the data
  mute_output = os.path.join(args.chunk_dir, 'f3_mute' + suffix)
  mute_cmd = """
  python ./scripts/mute_da.py --input-data=%s \
    --srcx=%s \
    --recx=%s \
    --srcy=%s \
    --recy=%s \
    --nrec-per-shot=%s \
    --streamer-header=%s \
    --output-data=%s \
    --water-vel=%f
  """ % (ddict['f3_shots'], ddict['f3_srcx'], ddict['f3_recx'],
         ddict['f3_srcy'], ddict['f3_recy'], ddict['f3_nrec'], ddict['f3_strm'],
         mute_output, args.water_vel)
  if args.verb:
    print(mute_cmd)
  subprocess.check_call(mute_cmd, shell=True)

  # Now debubble the data
  debubble_output = os.path.join(args.chunk_dir, 'f3_debubble' + suffix)
  debubble_cmd = """
  python ./scripts/debubble_shots.py --input-data=%s \
    --input-filter=%s \
    --input-lags=%s \
    --output-data=%s \
    --verb
  """ % (mute_output, args.input_filter, args.input_lags, debubble_output)
  if args.verb:
    print(debubble_cmd)
  subprocess.check_call(debubble_cmd, shell=True)

  if args.output_data is None:
    args.output_data = os.path.join(args.chunk_dir,
                                    'f3_processed' + suffix)
  # GNC Correction
  ftype = os.path.splitext(args.output_data)[-1]
  energy_qc = "--energy-qc" if args.energy_qc else ""
  base_gnc_cmd = """
  python ./scripts/gnc_correction.py --input-data=%s \
    --time-shift=%f \
    --max-time=%f \
    --energy-level=%f %s \
    --output-data=%s
  """
  if ftype == '.npy':
    sep = seppy.sep()
    gnc_output = os.path.join(args.chunk_dir, 'f3_processed' + suffix)
    gnc_cmd = base_gnc_cmd % (debubble_output, args.time_shift, args.max_time,
                              args.energy_level, energy_qc, gnc_output)
    if args.verb:
      print(gnc_cmd)
    subprocess.check_call(gnc_cmd, shell=True)
    # Now read in all files and write to .npz
    odict = {}
    for key, ifile in ddict.items():
      if key == 'f3_shots':
        daxes, data = sep.read_file(gnc_output)
        data = data.reshape(daxes.n, order='F').T
        odict['dt'] = daxes.d[0]
        odict[key] = np.ascontiguousarray(data).astype('float32')
      elif key == 'f3_nrec':
        daxes, data = sep.read_file(ifile)
        odict[key] = data.astype('int32')
      elif key != 'f3_strm':
        daxes, data = sep.read_file(ifile)
        odict[key] = data.astype('float32')
    np.save(args.output_data, odict)
  else:
    gnc_cmd = base_gnc_cmd % (debubble_output, args.time_shift, args.max_time,
                              args.energy_level, energy_qc, args.output_data)
    if args.verb:
      print(gnc_cmd)
    subprocess.check_call(gnc_cmd, shell=True)


def attach_args(parser=argparse.ArgumentParser()):
  parser.add_argument("--chunk-dir", type=str, default=None)
  parser.add_argument("--water-vel", type=float, default=1450)
  parser.add_argument("--qc", action='store_true', default=False)
  parser.add_argument(
      "--input-filter",
      type=str,
      default="./debubble_data/filter.H",
  )
  parser.add_argument(
      "--input-lags",
      type=str,
      default="./debubble_data/lags.H",
  )
  parser.add_argument("--time-shift", type=float, default=0.008)
  parser.add_argument("--max-time", type=float, default=6)
  parser.add_argument("--energy-level", type=float, default=-1)
  parser.add_argument("--energy-qc", action='store_true', default=False)
  parser.add_argument("--output-data", type=str, default=None)
  parser.add_argument("--verb", action='store_true', default=False)
  return parser


if __name__ == "__main__":
  main(attach_args().parse_args())
