
#include <stdio.h>

void binning_1d(int* xidx, double* mass, double* y, int npart, double* sums, double* vals, int npixels)
{
  int n, idx;

  for(n = 0; n < npart; n++)
    {
      idx = xidx[n];

      sums[idx] += mass[n];

      vals[idx] += mass[n] * y[n];
    }
}

void binning_2d(int* xidx, int* yidx, double* mass, int npart, double* vals, int npixels)
{
  int n, idx;

  for(n = 0; n < npart; n++)
    {
      idx = xidx[n] * npixels + yidx[n];

      vals[idx] += mass[n];
    }
}
