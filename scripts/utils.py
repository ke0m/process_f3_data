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


def qc_f3data(
    dat,
    srcx,
    recx,
    srcy,
    recy,
    nrec,
    migslc,
    bidx=0,
    ntw=1500,
    dt=0.002,
    dx=25,
    dy=25,
    ox=469800,
    oy=6072350,
    show=True,
    **kwargs,
):
  """
  QCs the F3 data

  Parameters:
    dat  - the input f3 data [ntr,nt]
    srcx - the source x coordinates [nsht]
    recx - the receiver x coordinates [ntr]
    srcy - the source y coordinates [nsht]
    recy - the receiver x coordinates [ntr]
    nrec - the number of receivers [nsht]
  """
  nsht = len(nrec)
  if (nsht != len(srcx) and nsht != len(srcy)):
    raise ValueError("Source X/Y coordinates must be same length as nrec")

  ntr = len(recx)
  if (dat.shape[0] != ntr):
    raise ValueError(
        "Data must have same number of traces as receiver coordinates")

  pclip = kwargs.get('pclip', 1.0)
  dmin = kwargs.get('dmin', np.min(dat)) * pclip
  dmax = kwargs.get('dmax', np.max(dat)) * pclip

  # Windowed grid
  oxw = ox + 200 * dx
  oyw = oy + 5 * dy
  nxw1, nyw1 = migslc.shape

  # Plotting axes
  oxp, oyp = oxw * 0.001, oyw * 0.001
  dxp, dyp = dx * 0.001, dy * 0.001

  # Scale the source and receiver coordinates
  srcx *= 0.001
  recx *= 0.001
  srcy *= 0.001
  recy *= 0.001

  curr_pos, beg, end = 0, nrec[0], nrec[1]

  def key_event(e):
    nonlocal curr_pos, beg, end

    if e.key == "n":
      curr_pos = curr_pos + 1
      curr_pos = curr_pos % nsht
      if (curr_pos == 0):
        beg = 0
        end = beg
      beg = end
      end += nrec[curr_pos]
    elif e.key == 'y':
      curr_pos = curr_pos + kwargs.get('sjump', 125)
      curr_pos = curr_pos % nsht
      if (curr_pos == 0):
        beg = 0
        end = beg
      beg += sum(nrec[curr_pos - kwargs.get('sjump', 125):curr_pos])
      end = beg + nrec[curr_pos]
    elif e.key == "m":
      curr_pos = curr_pos - 1
      curr_pos = curr_pos % nsht
      if (curr_pos == nsht - 1):
        end = ntr
        beg = end
      end = beg
      beg -= nrec[curr_pos]
    elif e.key == 'u':
      curr_pos = curr_pos - kwargs.get('sjump', 125)
      curr_pos = curr_pos % nsht
      if (curr_pos == nsht - 1):
        end = ntr
        beg = end
      #print(curr_pos,curr_pos+kwargs.get('sjump',125),nrec[curr_pos:curr_pos+kwargs.get('sjump',125)])
      end -= (sum(nrec[curr_pos + 1:curr_pos + 1 + kwargs.get('sjump', 125)]))
      beg = end - nrec[curr_pos]
    else:
      return
    #print(beg,end,curr_pos,nrec[curr_pos])

    # Update the data
    ax[0].set_title('Srcx=%.3f Srcy=%.3f Num=%d/%d' %
                    (srcx[curr_pos], srcy[curr_pos], curr_pos, nsht),
                    fontsize=kwargs.get('labelsize', 14))
    ax[0].set_xlabel(kwargs.get('xlabel', 'X (km)'),
                     fontsize=kwargs.get('labelsize', 14))
    ax[0].set_ylabel(kwargs.get('ylabel', 'Y (km)'),
                     fontsize=kwargs.get('labelsize', 14))
    ax[0].tick_params(labelsize=kwargs.get('ticksize', 14))
    # Update sources
    srcs = np.zeros([1, 2])
    srcs[:, 0] = srcx[curr_pos]
    srcs[:, 1] = srcy[curr_pos]
    scats.set_offsets(srcs)
    # Update receivers
    recs = np.zeros([nrec[curr_pos], 2])
    recs[:, 0] = recx[beg:end]
    recs[:, 1] = recy[beg:end]
    scatr.set_offsets(recs)
    # Update the shot gathers
    l.set_data(dat[beg:end, 0:ntw].T)
    fig.canvas.draw()

  fig, ax = plt.subplots(
      2,
      1,
      figsize=(kwargs.get("wbox", 12), kwargs.get("hbox", 8)),
  )
  fig.canvas.mpl_connect('key_press_event', key_event)
  # Show the first frame
  ax[0].imshow(np.flipud(migslc.T),
               extent=[oxp, oxp + nxw1 * dxp, oyp, oyp + nyw1 * dyp],
               interpolation='none',
               cmap='gray')
  scats = ax[0].scatter(srcx[0], srcy[0], marker='*', color='tab:red')
  scatr = ax[0].scatter(
      recx[0:nrec[0]],
      recy[0:nrec[0]],
      marker='v',
      color='tab:green',
  )
  ax[0].set_xlabel(kwargs.get('xlabel', 'X (km)'),
                   fontsize=kwargs.get('labelsize', 14))
  ax[0].set_ylabel(kwargs.get('ylabel', 'Y (km)'),
                   fontsize=kwargs.get('labelsize', 14))
  ax[0].tick_params(labelsize=kwargs.get('ticksize', 14))
  l = ax[1].imshow(
      dat[0:nrec[0], 0:ntw].T,
      vmin=dmin,
      vmax=dmax,
      extent=[0, nrec[0], ntw * dt, 0],
      interpolation='bilinear',
      cmap='gray',
      aspect=kwargs.get('aspect', 50),
  )
  ax[1].set_xlabel('Receiver number', fontsize=kwargs.get('labelsize', 14))
  ax[1].set_ylabel('Time (s)', fontsize=kwargs.get('labelsize', 14))
  if (show):
    plt.show()
