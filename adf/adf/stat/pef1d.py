import numpy as np
import matplotlib.pyplot as plt

import adf.stat.conv1d as cnvop
from ..gradopt.opr8tr import operator
from ..gradopt.combops import chainop
from ..gradopt.cd import cd


class pef1d(operator):
  """ PEFs in 1D """

  def __init__(self, n, nlag, lags=None, aux=None, verb=False):
    """
    pef1d constructor

    Parameters
      n    - length of data array
      nlag - number of lags for the filter (filter coefficients)
      lags - input int lag array (optional)
      aux  - input data array that will form the operator D
    """
    self.__n = n
    # Compute lags for filter
    self.__nlag = nlag
    if (lags is not None):
      self.lags = lags
      if (nlag != lags.shape[0]):
        raise Exception("nlag must be the same as the length of lags array")
    else:
      self.lags = np.arange(nlag, dtype='int32')
    # Set the auxiliary image
    if (aux is not None):
      self.__aux = aux

  def plotfilters(self, flt=None, show=True, **kwargs):
    """ Plots the filter shape for QC """
    # Make data array
    dtmp = np.zeros(self.__n)
    # Make random filters
    if (flt is not None):
      ftmp = flt
    else:
      ftmp = np.random.rand(self.__nlag)
    if (flt is not None):
      dtmp[0:self.__nlag] = ftmp[:]
    else:
      # Put a one at the block beginning
      dtmp[0] = 1.0
      # Fill with random numbers
      dtmp[0:+self.__nlag] = ftmp[:]
    # Plot the filters
    fig = plt.figure(figsize=(kwargs.get("wbox", 14), kwargs.get("hbox", 7)))
    ax = fig.gca()
    ax.stem(dtmp)
    ax.set_xlabel(kwargs.get('xlabel', ''),
                  fontsize=kwargs.get('labelsize', 18))
    ax.set_ylabel('Coefficient', fontsize=kwargs.get('labelsize', 18))
    ax.tick_params(labelsize=kwargs.get('labelsize', 18))
    if (show):
      plt.show()

  def set_aux(self, aux):
    """ Sets the auxilliary image """
    self.__aux = aux

  def create_data(self):
    """ Creates the data vector for the PEF estimation """
    # Create a temporary filter
    tflt = np.zeros(self.__nlag, dtype='float32')
    tflt[0] = 1.0
    # Create the data
    dat = np.zeros(self.__n, dtype='float32')
    self.forward(False, tflt, dat)

    return -dat

  def get_dims(self):
    """ Returns the dimensions of the PEF and mask operator """
    # PEF dims
    pdims = {}
    pdims['ncols'] = self.__nlag
    pdims['nrows'] = self.__n
    # Mask dims
    kdims = {}
    kdims['ncols'] = self.__nlag
    kdims['nrows'] = self.__nlag

    return [kdims, pdims]

  def forward(self, add, flt, dat):
    """
    Applies the operator D (constructed from the aux array) that
    will be convolved with the filter coefficients

    Parameters
      add - whether to add to the output [True/False]
      flt - the filter coefficients to be estimated
      dat - the result of the application of the data operator D to the PEF
    """
    # Check data size
    if (self.__n != dat.shape[0]):
      raise ValueError(
          "data shape (%d) must match n passed to constructor(%d)" %
          (dat.shape[0], self.__n))
    # Check filter size
    if (self.__nlag != flt.shape[0]):
      raise ValueError(
          "number of filter lags (%d) must match nlag passed to constructor (%d)"
          % (flt.shape[0], self.__nlag))

    if (not add):
      dat[:] = 0.0

    cnvop.conv1df_fwd(
        self.__nlag,
        self.lags,  # Lags
        self.__n,
        self.__aux,  # Data operator
        flt,
        dat,
    )

  def adjoint(self, add, flt, dat):
    """
    Correlates the data operator D with the dat array to give an estimate
    of the filter coefficients

    Parameters
      add - whether to add to the output filter coefficients [True/False]
      flt - the output filter coefficients
      dat - the input data to be correlated with D
    """
    # Check data size
    if (self.__n != dat.shape[0]):
      raise ValueError(
          "data shape (%d) must match n passed to constructor(%d)" %
          (dat.shape[0], self.__n))
    # Check filter size
    if (self.__nlag != flt.shape[0]):
      raise ValueError(
          "number of filter lags (%d) must match nlag passed to constructor (%d)"
          % (flt.shape[0], self.__nlag))

    if (not add):
      flt[:] = 0.0

    cnvop.conv1df_adj(
        self.__nlag,
        self.lags,  # Lags
        self.__n,
        self.__aux,  # Data operator
        flt,
        dat,
    )

  def dottest(self, add=False):
    """ Performs the dot product test of the operator """
    # Create model and data
    m = np.random.rand(self.__nlag).astype('float32')
    mh = np.zeros(m.shape, dtype='float32')
    d = np.random.rand(self.__n).astype('float32')
    dh = np.zeros(d.shape, dtype='float32')

    if (add):
      self.forward(True, m, dh)
      self.adjoint(True, mh, d)
      dotm = np.dot(m.flatten(), mh.flatten())
      dotd = np.dot(d, dh)
      print("Dot product test (add==True):")
      print("Dotm = %f Dotd = %f" % (dotm, dotd))
      print("Absolute error = %f" % (abs(dotm - dotd)))
      print("Relative error = %f" % (abs(dotm - dotd) / dotd))
    else:
      self.forward(False, m, dh)
      self.adjoint(False, mh, d)
      dotm = np.dot(m.flatten(), mh.flatten())
      dotd = np.dot(d, dh)
      print("Dot product test (add==False):")
      print("Dotm = %f Dotd = %f" % (dotm, dotd))
      print("Absolute error = %f" % (abs(dotm - dotd)))
      print("Relative error = %f" % (abs(dotm - dotd) / dotd))


class pef1dmask(operator):
  """ Mask operator for not updating the zero lag coefficient """

  def forward(self, add, flt, msk):
    """ Applies the mask to the filter """
    if (flt.shape != msk.shape):
      raise Exception("model and data must have same shape")
    # Set the zero lag to zero
    msk[:] = flt[:]
    msk[0] = 0.0

  def adjoint(self, add, flt, msk):
    """ Applies adjoint mask """
    if (flt.shape != msk.shape):
      raise Exception("model and data must have same shape")
    # Set the zero lag to zero
    flt[:] = msk[:]
    flt[0] = 0.0


def gapped_pef(dat, na, gap, niter=None, eps=0.0, qcres=False, verb=False):
  """
  Estimates a gapped PEF

  Parameters:
    na    - total length of filter
    gap   - number of samples distance between lag zero and lag one
    niter - number of iterations for which to run the CD inversion [na]
    eps   - regularization parameter
    qcres - flag to QC the prediction-error (residual) [False]
    verb  - verbosity information during inversion [False]

  Returns the lags and filter coefficients of the gapped PEF
  """
  if (na == 0):
    raise Exception("Input number of filter coefficients must be non-zero")
  # Build the lag array
  lags = np.arange(gap - 1, na, 1).astype('int32')
  lags[0] = 0
  nlag = len(lags)
  # Build the PEF
  pef = pef1d(len(dat), nlag, lags, aux=dat)
  idat = pef.create_data()
  # Build the chained PEF-mask operator
  mask = pef1dmask()
  zro = np.zeros(nlag, dtype='float32')
  dkop = chainop([mask, pef], pef.get_dims())
  # Run the inversion
  flt = np.zeros(nlag, dtype='float32')
  flt[0] = 1.0
  pefres = []
  if (niter is None):
    niter = na
  invflt = cd(dkop,
              idat,
              flt,
              niter=niter,
              rdat=zro,
              eps=eps,
              ress=pefres,
              verb=verb)

  if (qcres):
    return pefres[-1], lags, invflt
  else:
    return lags, invflt
