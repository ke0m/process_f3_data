import segyio
import glob
import inpout.seppy as seppy
import numpy as np
from genutils.ptyprint import progressbar
import matplotlib.pyplot as plt

sep = seppy.sep()

# Read in the SEGY file
sgys = glob.glob("./segy/*.segy")

allscoords = []; allrcoords = []
for isgy in progressbar(range(len(sgys)),"nsgy:"):
  # Read in the SEGY
  datsgy = segyio.open(sgys[isgy],ignore_geometry=True)

  # Get the coordinates
  srcx = np.asarray(datsgy.attributes(segyio.TraceField.SourceX),dtype='int32')
  srcy = np.asarray(datsgy.attributes(segyio.TraceField.SourceY),dtype='int32')
  recx = np.asarray(datsgy.attributes(segyio.TraceField.GroupX),dtype='int32')
  recy = np.asarray(datsgy.attributes(segyio.TraceField.GroupY),dtype='int32')

  srccoords = np.zeros([len(srcx),2],dtype='int')
  reccoords = np.zeros([len(recx),2],dtype='int')

  srccoords[:,0] = srcy
  srccoords[:,1] = srcx

  reccoords[:,0] = recy
  reccoords[:,1] = recx

  allscoords.append(srccoords)
  allrcoords.append(reccoords)

allscoords = np.concatenate(allscoords,axis=0).astype('float32')
allrcoords = np.concatenate(allrcoords,axis=0).astype('float32')

sep.write_file("srccoordsall.H",allscoords)
sep.write_file("reccoordsall.H",allrcoords)

