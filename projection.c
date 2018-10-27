
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

int ilimit(int a, int npixels)
{
  int b = imin(imax(a, 0), npixels - 1);

  return b;
}

void projection(double* x, double* y, double* rho, double* hsml, double* vals, int npart, double* proj, double* sums, int npixels)
{
  int n, i, j, idx;
  int min1, max1, min2, max2;
  double psum, pproj;

  for(n = 0; n < npart; n++)
    {
      min1 = (x[n] + 0.5 - hsml[n]) * npixels;
      min1 = ilimit(min1, npixels);

      max1 = (x[n] + 0.5 + hsml[n]) * npixels;
      max1 = ilimit(max1, npixels);

      min2 = (y[n] + 0.5 - hsml[n]) * npixels;
      min2 = ilimit(min2, npixels);

      max2 = (y[n] + 0.5 + hsml[n]) * npixels;
      max2 = ilimit(max2, npixels);

      psum = rho[n] * rho[n];
      pproj = psum * vals[n];

      for(i = min1; i <= max1; i++)
	for(j = min2; j <= max2; j++)
	  {
	    idx = i * npixels + j;

	    proj[idx] += pproj;
	    sums[idx] += psum;
	  }
    }
}
