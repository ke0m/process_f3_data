/**
 * 1D Stationary convolution of a prediction-error filter
 * @author: Joseph Jennings
 * @version: 2020.11.19
 */

#ifndef CONV1D_H_
#define CONV1D_H_

void conv1df_fwd(int nlag, int *lag, int n, float *aux, float *flt, float *dat);
void conv1df_adj(int nlag, int *lag, int n, float *aux, float *flt, float *dat);
void conv1dm_fwd(int nlag, int *lag, int n, float *aux, float *flt, float *dat);
void conv1dm_adj(int nlag, int *lag, int n, float *aux, float *flt, float *dat);

#endif /* CONV1D_H_ */
