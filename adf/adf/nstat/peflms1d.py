import numpy as np

def peflms1d(x,nw,mu,w0=None):
  """
  Performs PEF estimation in 1D using the LMS algorithm

  Parameters:
    x     - the input signal
    nw    - the number of filter coefficients
    mu    - adaptation constant
    w0    - an initial guess for w [None]

  Returns an estimate for w
  """
  n = x.shape[0]

  # Create output arrays
  err = np.zeros(n); pred = np.zeros(n)
  ws  = np.zeros([n,nw])

  w = np.zeros(nw)
  if(w0 is not None): w[:] = w0

  # Loop over all samples
  for k in range(nw,n):
    xk = np.flip(x[k-nw:k],0)
    pred[k] = np.dot(xk,w)
    err[k]  = x[k] - pred[k]
    w = w + 2*mu*err[k]*xk
    # Save the ws
    ws[k,:] = w

  return w,ws,pred,err

def peflmsgap1d(x,nw,gap,mu,w0=None,prdqc=False,update=True) -> list:
  """
  Estimates a gapped PEF (useful for debubble/demultiple)

  Parameters:
    x   - input 1D signal [nt]
    nw  - length of output filter
    gap - gap for predicting the bubble or multiple period
    mu  - learning rate
    w0  - input initial guess at weights
    prdqc

  Returns the estimated weights as well as the
  prediction-error (debubbled/demultipled signal)
  """
  n = x.shape[0]

  if(gap >= n):
    raise Exception("gap must be <= length of input signal")

  # Create output residual (error) signal and prediction
  err = np.zeros(n)
  prd = np.zeros(n)

  # Output PEF
  w = np.zeros(nw)
  if(w0 is not None): w[:] = w0

  # Initialize running variances
  sumsq = np.sum(x**2)
  sigy = np.sqrt(sumsq*mu)
  sige = sigy/2

  for k in range(nw,n):
    # Make the prediction
    xk = np.flip(x[k-nw:k],0)
    prd[k] = np.dot(xk,w)
    err[k] = x[k] - prd[k]
    if(update):
      # Compute a running variance
      sige = (1.0-mu)*sige + mu*err[k]**2
      sigy = (1.0-mu)*sigy + mu*x[k]**2
      # Update the filter
      w[gap:] = w[gap:] + mu/(sige+sigy)*err[k]*xk[gap:]

  if(prdqc):
    return prd,err,w
  else:
    return err,w

