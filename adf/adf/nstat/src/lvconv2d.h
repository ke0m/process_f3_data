/**
 * 2D Linearly-varying non-stationary convolution
 * of a prediction-error filter
 * @author: Joseph Jennings
 * @version: 2020.03.11
 */

#ifndef LVCONV2D_H_
#define LVCONV2D_H_

void lvconv2df_fwd(int nb, int *b1, int *e1, int *b2, int *e2, int nlag, int *lag1, int *lag2,
                   int n1, int n2, float *aux, int *nf, float *flt, float *dat);
void lvconv2df_adj(int nb, int *b1, int *e1, int *b2, int *e2, int nlag, int *lag1, int *lag2,
                   int n1, int n2, float *aux, int *nf, float *flt, float *dat);

#endif /* LVCONV2D_H_ */
