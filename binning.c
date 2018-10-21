
#include <stdio.h>

void binning(int* xidx, int* yidx, double* mass, int npart, double* vals, int nbins)
{
  int n, idx;

  for(n = 0; n < npart; n++)
    {
      idx = xidx[n] * nbins + yidx[n];

      vals[idx] += mass[n];
    }
}
