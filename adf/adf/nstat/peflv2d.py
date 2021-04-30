import math, numpy as np
from opt.linopt.opr8tr import operator
import pef.nstat.lvconv2d as lvop
from utils.ptyprint import create_inttag
import matplotlib.pyplot as plt

class peflv2d(operator):
  """ Linearly varying PEFs in 2D """

  def __init__(self,n,j,nlag,lags=None,aux=None,verb=False):
    """
    peflv1d constructor

    Parameters
      n    - length of data array
      j    - spacing (jump) between filter blocks
      nlag - number of lags for the filter (filter coefficients)
      lags - input int lag array (optional)
      aux  - input data array that will form the operator D 
    """
    self.__n = n
    # Compute number of filters
    self.nf = []
    self.nf.append(int(math.ceil((n[0]-2)/j[0]) + 1))
    self.nf.append(int(math.ceil((n[1]-2)/j[1]) + 1))
    # Compute lags for filter
    if(lags is not None):
      # Split the coordinates
      self.lag1 = lags[0,:]; self.lag2 = lags[:,0]
    else:
      self.lag1 = []; self.lag2 = []
      # Compute the minimum lag
      if(nlag[0]%2 == 0):
        lag1min = -nlag[0]/2
      else:
        lag1min = -(nlag[0] - 1)/2
      # Compute the lags as coordinates in the filter
      for k in range(nlag[1]):
        for i in range(nlag[0]):
          if(lag1min + i < 0 and k == 0):
            continue
          else:
            self.lag1.append(lag1min + i)
            self.lag2.append(k)
      self.nlag = len(self.lag1)
      # Convert to numpy arrays
      self.lag1 = np.asarray(self.lag1,dtype='int32')
      self.lag2 = np.asarray(self.lag2,dtype='int32')
    
    # Find the min and max lag along axis 1
    minlag1 = np.min(self.lag1); maxlag1 = np.max(self.lag1)

    # Find the min and max lag along axis 2
    minlag2 = np.min(self.lag2); maxlag2 = np.max(self.lag2)

    # Build the blocks
    self.b1,self.e1 = self.find_optimal_sizes(self.__n[0],j[0],self.nf[0])
    self.b2,self.e2 = self.find_optimal_sizes(self.__n[1],j[1],self.nf[1])
    self.bb1 = []; self.eb1 = []
    self.bb2 = []; self.eb2 = []
    self.nb = 0
    # Handle the endpoints
    for k in range(len(self.b2)):
      for i in range(len(self.b1)):
        if(self.e1[i] == self.__n[0]-1):
          self.e1[i] -= maxlag1
        if(self.e2[k] == self.__n[1]-1):
          self.e2[k] -= maxlag2
        if(self.b1[i] == 0):
          self.b1[i] -= minlag1
        if(self.b2[k] == 0):
          self.b2[k] -= minlag2
        # Accumulate the blocks
        self.bb1.append(self.b1[i]); self.eb1.append(self.e1[i])
        self.bb2.append(self.b2[k]); self.eb2.append(self.e2[k])
        self.nb += 1

    # Convert to numpy arrays
    self.bb1 = np.asarray(self.bb1,dtype='int32'); self.eb1 = np.asarray(self.eb1,dtype='int32')
    self.bb2 = np.asarray(self.bb2,dtype='int32'); self.eb2 = np.asarray(self.eb2,dtype='int32')
    if(verb):
      print("Total number of blocks: %d"%(self.nb))
      for ib in range(self.nb):
        print("Block %s [b1=%s e1=%s b2=%s e2=%s]"%(create_inttag(ib,self.nb), create_inttag(self.bb1[ib],np.max(self.bb1)),
              create_inttag(self.eb1[ib],np.max(self.eb1)),create_inttag(self.bb2[ib],np.max(self.bb2)),
              create_inttag(self.eb2[ib],np.max(self.eb2))))
      print(" ")
      print("Total number of lags: %d"%(self.nlag))
      for il in range(self.nlag):
        print("%d lag1=%d lag2=%d"%(il,self.lag1[il],self.lag2[il]))

    # Set the auxiliary image
    if(aux is not None):
      self.__aux = aux

  def find_optimal_sizes(self,n,j,nf):
    """
    Finds the optimal block sizes for linearly varying convolution

    Parameters
      n1 - length of input data array
      j  - spacing between blocks
      nf - total number of filters
    
    Returns
      b - int array containing beginning block indices
      e - int array containing ending block indices
    """
    b = []; e = []
    space = n
    b.append(0)
    for k in range(nf-1):
      sample = int(math.ceil(space/(nf-k-1)))
      e.append(sample + b[k] - 1)
      if(k != nf-2): b.append(e[k] + 1)
      space -= sample

    return np.asarray(b,dtype='int32'),np.asarray(e,dtype='int32')

  def plotfilters(self,flts=None,show=True,**kwargs):
    """ Plots the filters on the coarse grid on the image for QC """
    pass

  def set_aux(self,aux):
    """ Sets the auxilliary image """
    self.__aux = aux

  def create_data(self):
    """ Creates the data vector for the PEF estimation """
    # Create a temporary filter
    tflt = np.zeros([self.nf[1],self.nf[0],self.nlag],dtype='float32')
    tflt[:,:,0] = 1.0
    # Create the data
    dat = np.zeros(self.__n,dtype='float32')
    self.forward(False,tflt,dat)

    return -dat

  def get_dims(self):
    """ Returns the dimensions of the PEF and mask operator """
    fltshape = [self.nf[1],self.nf[0],self.nlag]
    # PEF dims
    pdims = {}
    pdims['ncols'] = fltshape; pdims['nrows'] = self.__n
    # Mask dims
    kdims = {}
    kdims['ncols'] = fltshape; kdims['nrows'] = fltshape

    return [kdims,pdims]

  def forward(self,add,flt,dat):
    """
    Applies the operator D (constructed from the aux array) that 
    will be convolved with the filter coefficients

    Parameters
      add - whether to add to the output [True/False]
      flt - the filter coefficients to be estimated
      dat - the result of the application of the data operator D to the PEF
    """
    # Check data size
    if(self.__n != dat.shape):
      raise Exception("data shape (%d %d) must match n passed to constructor(%d %d)"%(dat.shape[0],dat.shape[1],self.__n[0],self.__n[1]))
    # Check filter size
    if(self.nlag != flt.shape[-1]):
      raise Exception("number of filter lags (%d) must match nlag passed to constructor (%d)"%(flt.shape[-11],self.nlag))
    if(tuple(self.nf) != flt.shape[:-1]):
      raise Exception("number of filters (%d %d) must match nf passed to constructor (%d %d)"%(flt.shape[0],flt.shape[1],self.nf[0],self.nf[1]))

    if(not add):
      dat[:] = 0.0

    lvop.lvconv2df_fwd(self.nb, self.bb1, self.eb1, self.bb2, self.eb2, # Blocks
                       self.nlag, self.lag1, self.lag2,                 # Lags
                       self.__n[0], self.__n[1], self.__aux,            # Data operator
                       self.nf, flt, dat) 

  def adjoint(self,add,flt,dat):
    """
    Correlates the data operator D with the dat array to give an estimate
    of the filter coefficients

    Parameters
      add - whether to add to the output filter coefficients [True/False]
      flt - the output filter coefficients
      dat - the input data to be correlated with D
    """
    # Check data size
    if(self.__n != dat.shape):
      raise Exception("data shape (%d %d) must match n passed to constructor(%d %d)"%(dat.shape[0],dat.shape[1],self.__n[0],self.__n[1]))
    # Check filter size
    if(self.nlag != flt.shape[-1]):
      raise Exception("number of filter lags (%d) must match nlag passed to constructor (%d)"%(flt.shape[-11],self.nlag))
    if(tuple(self.nf) != flt.shape[:-1]):
      raise Exception("number of filters (%d %d) must match nf passed to constructor (%d %d)"%(flt.shape[0],flt.shape[1],self.nf[0],self.nf[1]))

    if(not add):
      flt[:] = 0.0

    lvop.lvconv2df_adj(self.nb, self.bb1, self.eb1, self.bb2, self.eb2, # Blocks
                       self.nlag ,self.lag1, self.lag2,                 # Lags
                       self.__n[0], self.__n[1], self.__aux,            # Data operator
                       self.nf, flt, dat)

  def dottest(self,add=False):
    """ Performs the dot product test of the operator """
    # Create model and data
    m  = np.random.rand(self.nf[1],self.nf[0],self.nlag).astype('float32')
    mh = np.zeros(m.shape,dtype='float32')
    d  = np.random.rand(*self.__n).astype('float32')
    dh = np.zeros(d.shape,dtype='float32')

    if(add):
      self.forward(True,m ,dh)
      self.adjoint(True,mh,d )
      dotm = np.dot(m.flatten(),mh.flatten()); dotd = np.dot(d.flatten(),dh.flatten())
      print("Dot product test (add==True):")
      print("Dotm = %f Dotd = %f"%(dotm,dotd))
      print("Absolute error = %f"%(abs(dotm-dotd)))
      print("Relative error = %f"%(abs(dotm-dotd)/dotd))
    else:
      self.forward(False,m ,dh)
      self.adjoint(False,mh,d )
      dotm = np.dot(m.flatten(),mh.flatten()); dotd = np.dot(d.flatten(),dh.flatten())
      print("Dot product test (add==False):")
      print("Dotm = %f Dotd = %f"%(dotm,dotd))
      print("Absolute error = %f"%(abs(dotm-dotd)))
      print("Relative error = %f"%(abs(dotm-dotd)/dotd))

class peflv2dmask(operator):
  """ Mask operator for not updating the zero lag coefficient """

  def forward(self,add,flt,msk):
    """ Applies the mask to the filter """
    if(flt.shape != msk.shape):
      raise Exception("model and data must have same shape")
    # Set the zero lag to zero
    msk[:] = flt[:]
    msk[:,:,0] = 0.0

  def adjoint(self,add,flt,msk):
    """ Applies adjoint mask """
    if(flt.shape != msk.shape):
      raise Exception("model and data must have same shape")
    # Set the zero lag to zero
    flt[:] = msk[:]
    flt[:,:,0] = 0.0

