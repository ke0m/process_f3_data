import numpy as np


def create_inttag(numin, totnum):
  """ Creates a tag that is appended with zeros for friendly Unix sorting """
  nzeroso = int(np.log10(totnum))
  nzeros = nzeroso
  tagout = None
  for izro in range(1, nzeroso + 1):
    if ((numin >= 10**(izro - 1) and numin < 10**(izro))):
      tagout = '0' * (nzeros) + str(numin)
    nzeros -= 1
  if (tagout is not None):
    return tagout
  elif (numin == 0):
    return '0' * (nzeroso) + str(numin)
  else:
    return str(numin)
