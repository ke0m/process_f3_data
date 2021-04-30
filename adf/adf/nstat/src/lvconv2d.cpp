#include <stdio.h>
#include <cstring>
#include "lvconv2d.h"

void lvconv2df_fwd(int nb, int *b1, int *e1, int *b2, int *e2, int nlag, int *lag1, int *lag2,
    int nd1, int nd2, float *aux, int *nf, float *flt, float *dat) {

  /* Allocate temporary arrays */
  float* b00 = new float[nlag]();
  float* b01 = new float[nlag]();
  float* d02 = new float[nlag]();
  float* d12 = new float[nlag]();
  float *bin = new float[nlag]();
  float *d01 = new float[nlag]();

  /* Loop over each block */
  for(int ib = 0; ib < nb; ++ib) {
    /* Get the locations of the block corners */
    int k1 = ib%(nf[0]-1);
    int k2 = ib/(nf[0]-1);
    /* Get the filter coefficients at the block corners */
    memcpy(b00,&flt[((k2+0)*nf[0] + k1+0)*nlag],sizeof(float)*nlag);
    memcpy(b01,&flt[((k2+0)*nf[0] + k1+1)*nlag],sizeof(float)*nlag);
    memcpy(d02,&flt[((k2+1)*nf[0] + k1+0)*nlag],sizeof(float)*nlag);
    memcpy(d12,&flt[((k2+1)*nf[0] + k1+1)*nlag],sizeof(float)*nlag);
    /* Compute axis 2 interpolating factors to be added */
    double dist1 = e1[ib] - b1[ib] + 1; double dist2 = e2[ib] - b2[ib] + 1;
    for(int il = 0; il < nlag; ++il) {
      d02[il] = (d02[il] - b00[il])/dist2;
      d12[il] = (d12[il] - b01[il])/dist2;
    }
    /* Loop over each point in the block */
    for(int id2 = b2[ib]; id2 <= e2[ib]; ++id2) {
      memcpy(bin,b00,sizeof(float)*nlag);
      memcpy(d01,b01,sizeof(float)*nlag);
      /* Compute axis 1 interpolating factor to be added */
      for(int il = 0; il < nlag; ++il) { d01[il] = (d01[il] - b00[il])/dist1; };
      for(int id1 = b1[ib]; id1 <= e1[ib]; ++id1) {
        /* Perform the convolution with the interpolated filter */
        for(int il = 0; il < nlag; ++il) {
          dat[(id2+lag2[il])*nd1 + id1+lag1[il]] += bin[il]*aux[id2*nd1 + id1];
        }
        /* Interpolate along axis 1 */
        for(int il = 0; il < nlag; ++il) { bin[il] += d01[il]; };
      }
      /* Interpolate along axis 2 */
      for(int il = 0; il < nlag; ++il) {
        b00[il] += d02[il]; b01[il] += d12[il];
      }
    }
  }

  /* Free memory */
  delete[] b00; delete[] b01;
  delete[] d02; delete[] d12;
  delete[] bin; delete[] d01;

}

void lvconv2df_adj(int nb, int *b1, int *e1, int *b2, int *e2, int nlag, int *lag1, int *lag2,
    int nd1, int nd2, float *aux, int *nf, float *flt, float *dat) {

  /* Allocate temporary arrays */
  float* b00 = new float[nlag]();
  float* b01 = new float[nlag]();
  float* d02 = new float[nlag]();
  float* d12 = new float[nlag]();
  float *bin = new float[nlag]();
  float *d01 = new float[nlag]();

  /* Loop over blocks */
  for(int ib = 0; ib < nb; ++ib) {
    /* Loop over each point in the block */
    memset(d02, 0, sizeof(float)*nlag); memset(d12, 0, sizeof(float)*nlag);
    memset(b00, 0, sizeof(float)*nlag); memset(b01, 0, sizeof(float)*nlag);
    for(int id2 = e2[ib]; id2 >= b2[ib]; --id2) {
      memset(d01, 0, sizeof(float)*nlag); memset(bin, 0, sizeof(float)*nlag);
      for(int id1 = e1[ib]; id1 >= b1[ib]; --id1) {
        for(int il = 0; il < nlag; ++il) {
          double x = aux[id2*nd1 + id1] * dat[(id2+lag2[il])*nd1 + id1+lag1[il]];
          d01[il] += bin[il];
          bin[il] += x;
        }
      }
      /* Adjoint linear interpolation */
      double dist1 = e1[ib] - b1[ib] + 1.0;
      for(int il = 0; il < nlag; ++il) {
        d02[il] += b00[il];
        d12[il] += b01[il];
        b00[il] += bin[il] - d01[il]/dist1;
        b01[il] += d01[il]/dist1;
      }
    }
    double dist2 = e2[ib] - b2[ib] + 1.0;
    int k1 = ib%(nf[0]-1); int k2 = ib/(nf[0]-1);
    for(int il = 0; il < nlag; ++il) {
      flt[(k2+0)*nf[0]*nlag + (k1+0)*nlag + il] += -d02[il]/dist2 + b00[il];
      flt[(k2+0)*nf[0]*nlag + (k1+1)*nlag + il] += -d12[il]/dist2 + b01[il];
      flt[(k2+1)*nf[0]*nlag + (k1+0)*nlag + il] +=  d02[il]/dist2;
      flt[(k2+1)*nf[0]*nlag + (k1+1)*nlag + il] +=  d12[il]/dist2;
    }
  }

  /* Free memory */
  delete[] b00; delete[] b01;
  delete[] d02; delete[] d12;
  delete[] bin; delete[] d01;
}
