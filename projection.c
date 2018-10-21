
#include <math.h>

int imin(int a, int b)
{
  if(a < b)
    return a;
  else
    return b;
}

int imax(int a, int b)
{
  if(a > b)
    return a;
  else
    return b;
}

int ilimit(int a, int nbins)
{
  int b = imin(imax(a, 0), nbins - 1);

  return b;
}

void projection(double* x, double *y, double* rho, double* hsml, double* vals, int npart, double* proj, double* sums, int nbins)
{
  int n, i, j, idx;
  int min1, max1, min2, max2;
  double psum, pproj;

  for(n = 0; n < npart; n++)
    {
      min1 = (x[n] + 0.5 - hsml[n]) * nbins;
      min1 = ilimit(min1, nbins);

      max1 = (x[n] + 0.5 + hsml[n]) * nbins;
      max1 = ilimit(max1, nbins);

      min2 = (y[n] + 0.5 - hsml[n]) * nbins;
      min2 = ilimit(min2, nbins);

      max2 = (y[n] + 0.5 + hsml[n]) * nbins;
      max2 = ilimit(max2, nbins);

      psum = rho[n] * rho[n];
      pproj = psum * vals[n];

      for(i = min1; i <= max1; i++)
	for(j = min2; j <= max2; j++)
	  {
	    idx = i * nbins + j;

	    proj[idx] += pproj;
	    sums[idx] += psum;
	  }
    }
}
