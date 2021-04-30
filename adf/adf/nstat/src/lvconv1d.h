/**
 * Linearly-varying non-stationary convolution
 * of a prediction-error filter
 * @author: Joseph Jennings
 * @version: 2020.03.08
 */

#ifndef LVCONV1D_H_
#define LVCONV1D_H_

void lvconv1df_fwd(int nb, int *b, int *e, int nlag, int *lag, int n, float *aux, float *flt, float *dat);
void lvconv1df_adj(int nb, int *b, int *e, int nlag, int *lag, int n, float *aux, float *flt, float *dat);


#endif /* LVCONV1D_H_ */
