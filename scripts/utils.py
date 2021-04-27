import numpy as np
import matplotlib.pyplot as plt


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


def plot_acq(
    srcx,
    srcy,
    recx,
    recy,
    slc,
    ox,
    oy,
    dx=0.025,
    dy=0.025,
    srcs=True,
    recs=False,
    figname=None,
    **kwargs,
):
  ny, nx = slc.shape
  cmap = kwargs.get('cmap', 'gray')
  fig = plt.figure(figsize=(14, 7))
  ax = fig.gca()
  ax.imshow(np.flipud(slc),
            cmap=cmap,
            extent=[ox, ox + nx * dx, oy, oy + ny * dy])
  if (srcs):
    ax.scatter(srcx, srcy, marker='*', color='tab:red')
  if (recs):
    ax.scatter(recx, recy, marker='v', color='tab:green')
  ax.set_xlabel('X (km)', fontsize=kwargs.get('fsize', 15))
  ax.set_ylabel('Y (km)', fontsize=kwargs.get('fsize', 15))
  ax.tick_params(labelsize=kwargs.get('fsize', 15))
  if (figname is not None):
    plt.savefig(figname, dpi=150, transparent=True, bbox_inches='tight')
  if (kwargs.get('show', True)):
    plt.show()
