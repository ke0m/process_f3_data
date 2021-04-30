#include <stdio.h>
#include <cstring>
#include "conv1d.h"

void conv1df_fwd(int nlag, int *lag, int n, float *aux, float *flt, float *dat) {

  /* Loop over the data */
  for(int id = 0; id <= n-lag[nlag-1]-1; ++id) {
    /* Loop over the coefficients */
    for(int il = 0; il < nlag; ++il) {
      dat[id + lag[il]] += flt[il]*aux[id];
    }
  }
}

void conv1df_adj(int nlag, int *lag, int n, float *aux, float *flt, float *dat) {

  /* Loop over the data */
  for(int id = n-lag[nlag-1]-1; id >= 0; --id) {
    /* Loop over the coefficients */
    for(int il = 0; il < nlag; ++il) {
      flt[il] += aux[id]*dat[id + lag[il]];
    }
  }
}

void conv1dm_fwd(int nlag, int *lag, int n, float *flt, float *mod, float *dat) {

  /* Loop over the data */
  for(int id = 0; id <= n-lag[nlag-1]-1; ++id) {
    /* Loop over the coefficients */
    for(int il = 0; il < nlag; ++il) {
      dat[id + lag[il]] += flt[il]*mod[id];
    }
  }

}

void conv1dm_adj(int nlag, int *lag, int n, float *flt, float *mod, float *dat) {

  /* Loop over the data */
  for(int id = 0; id <= n-lag[nlag-1]-1; ++id) {
    /* Loop over the coefficients */
    for(int il = 0; il < nlag; ++il) {
      mod[id] += flt[il]*dat[id + lag[il]];
    }
  }

}
