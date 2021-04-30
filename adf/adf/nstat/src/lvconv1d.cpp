#include <stdio.h>
#include <cstring>
#include "lvconv1d.h"

void lvconv1df_fwd(int nb, int *b, int *e, int nlag, int *lag, int n, float *aux, float *flt, float *dat) {

  /* Temporary arrays */
  float *b0 = new float[nlag]; float *d0 = new float[nlag];

  /* Loop over each block */
  for(int ib = 0; ib < nb; ++ib) {
    /* Get the filter coefficients at block corners */
    memcpy(b0,&flt[(ib+0)*nlag],sizeof(float)*nlag);
    memcpy(d0,&flt[(ib+1)*nlag],sizeof(float)*nlag);
    /* Compute interpolating factor to be added */
    double dist = e[ib] - b[ib] + 1.0;
    for(int il = 0; il < nlag; ++il) { d0[il] = (d0[il]-b0[il])/dist; };
    /* Loop over each point in the block */
    for(int id = b[ib]; id <= e[ib]; ++id) {
      /* Convolve with interpolated filter */
      for(int il = 0; il < nlag; ++il) {
        dat[id + lag[il]] += b0[il]*aux[id];
      }
      for(int il = 0; il < nlag; ++il) { b0[il] += d0[il]; };
    }
  }

  /* Free memory */
  delete[] b0; delete[] d0;
}

void lvconv1df_adj(int nb, int *b, int *e, int nlag, int *lag, int n, float *aux, float *flt, float *dat) {

  /* Temporary arrays */
  float *b0 = new float[nlag]; float *d0 = new float[nlag];

  /* Loop over each block */
  for(int ib = 0; ib < nb; ++ib) {
    /* Loop over each point in the block */
    memset(b0, 0, sizeof(float)*nlag); memset(d0, 0, sizeof(float)*nlag);
    for(int id = e[ib]; id >= b[ib]; --id) {
      /* Loop over the coefficients */
      for(int il = 0; il < nlag; ++il) {
        double x = aux[id] * dat[id + lag[il]];
        d0[il] += b0[il];
        b0[il] += x;
      }
    }
    /* Adjoint linear interpolation */
    double dist = e[ib] - b[ib] + 1.0;
    for(int il = 0; il < nlag; ++il) {
      flt[(ib+0)*nlag + il] += -d0[il]/dist + b0[il];
      flt[(ib+1)*nlag + il] +=  d0[il]/dist;
    }
  }

  /* Free memory */
  delete[] b0; delete[] d0;
}
