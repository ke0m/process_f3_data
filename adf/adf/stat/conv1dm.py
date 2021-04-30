import numpy as np
import matplotlib.pyplot as plt

import adf.stat.conv1d as cnvop
from ..gradopt.opr8tr import operator


class conv1dm(operator):
  """ Convolution in 1D (adjoint returns the model) """

  def __init__(self, n, nlag, lags=None, flt=None, verb=False):
    """
    conv1dm constructor

    Parameters
      n    - length of data array
      nlag - number of lags for the filter (filter coefficients)
      lags - input int lag array (optional)
      flt  - input filter array that will form the filter operator
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
    # Set the filter
    if (flt is not None):
      self.__flt = flt
      if (len(self.__flt) != nlag):
        raise Exception("Length of input filter (%d_ must = nlag" %
                        (len(self.__flt)))

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
      for il in range(len(self.lags)):
        dtmp[self.lags[il]] = ftmp[il]
    else:
      # Put a one at the block beginning
      dtmp[0] = 1.0
      for il in range(len(self.lags)):
        dtmp[self.lags[il]] = ftmp[il]
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

  def set_flt(self, aux):
    """ Sets the filter """
    self.__flt = aux

  def get_dims(self):
    """ Returns the dimensions of the convolution operator """
    # Conv dims
    cdims = {}
    cdims['ncols'] = self.__n
    cdims['nrows'] = self.__n

    return cdims

  def forward(self, add, mod, dat):
    """
    Applies the operator F (constructed from the flt array) to
    the input model

    Parameters
      add - whether to add to the output [True/False]
      mod - input model to be convolved with filter [n]
      dat - the result of the application of the filter with the model [n]
    """
    # Check data size
    if (self.__n != dat.shape[0]):
      raise Exception("data shape (%d) must match n passed to constructor(%d)" %
                      (dat.shape[0], self.__n))
    # Check filter size
    if (self.__n != mod.shape[0]):
      raise Exception(
          "model shape (%d) must match n passed to constructor(%d)" %
          (mod.shape[0], self.__n))

    if (not add):
      dat[:] = 0.0

    cnvop.conv1dm_fwd(
        self.__nlag,
        self.lags,  # Lags
        self.__n,
        self.__flt,  # Data operator
        mod,
        dat,
    )

  def adjoint(self, add, mod, dat):
    """
    Correlates the filter operator with the dat array to give an estimate
    of the model

    Parameters
      add - whether to add to the output filter coefficients [True/False]
      flt - the output model [n]
      dat - the input data to be correlated with the filter [n]
    """
    # Check data size
    if (self.__n != dat.shape[0]):
      raise ValueError(
          "data shape (%d) must match n passed to constructor(%d)" %
          (dat.shape[0], self.__n))
    # Check filter size
    if (self.__n != mod.shape[0]):
      raise ValueError(
          "model shape (%d) must match n passed to constructor(%d)" %
          (mod.shape[0], self.__n))

    if (not add):
      mod[:] = 0.0

    cnvop.conv1dm_adj(
        self.__nlag,
        self.lags,  # Lags
        self.__n,
        self.__flt,  # Data operator
        mod,
        dat,
    )

  def dottest(self, add=False):
    """ Performs the dot product test of the operator """
    # Create model and data
    m = np.random.rand(self.__n).astype('float32')
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
