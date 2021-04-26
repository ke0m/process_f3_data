def splitnum(num, div):
  """ Splits a number into nearly even parts """
  splits = []
  igr, rem = divmod(num, div)
  splits = [igr] * div
  return [splits[i] + 1 for i in range(rem)] + splits[rem:]


def chunks(lst, nchnks):
  nitem = len(lst)
  splits = splitnum(nitem, nchnks)
  beg, end = 0, splits[0]
  for isplit in splits:
    yield lst[beg:end]
    beg = end
    end += isplit
