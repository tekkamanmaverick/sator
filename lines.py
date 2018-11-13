
from include import *
from utils import *

def get_lines(self, xfield, yfield, npixels):

    # Some additional settings

    if xfield == 'gamma':
        log_plot_x = 0
    else:
        log_plot_x = 1

    if yfield == 'gamma':
        log_plot_y = 0
    else:
        log_plot_y = 1

    # Read selected fields

    flag, x = self.get_refined_field(xfield)

    if flag:
        return

    flag, y = self.get_refined_field(yfield)

    if flag:
        return

    # Read mass

    flag, mass = self.get_refined_field('mass')

    if flag:
        return

    # Select only valid entries

    if log_plot_x or log_plot_y:
        if log_plot_x and log_plot_y:
            idx = np.logical_and(x > 0., y > 0.)
        elif log_plot_x:
            idx = x > 0.
        else:
            idx = y > 0.

        x = x[idx]
        y = y[idx]

        mass = mass[idx]

    npart = mass.size

    # Take logarithm if required

    if log_plot_x:
        x = np.log10(x)

    if log_plot_x:
        y = np.log10(y)

    # Get minimum and maximum values

    xmin = np.min(x)
    xmax = np.max(x)

    # Get indices for all cells

    xidx = (x - xmin) * npixels / (xmax - xmin)

    # Convert to integer

    xidx = xidx.astype(dtype = np.dtype('int32'))

    # Limit integers

    xidx = np.minimum(xidx, npixels - 1)

    # Intitialize results arrays

    sums = np.zeros(npixels)
    yvals = np.zeros(npixels)

    # Load binning library

    arr_i = npct.ndpointer(dtype = np.dtype('int32'), ndim = 1, flags = 'CONTIGUOUS')
    arr_d = npct.ndpointer(dtype = np.dtype('float64'), ndim = 1, flags = 'CONTIGUOUS')
    lib = npct.load_library("binning", ".")
    lib.restype = None
    lib.binning_1d.argtypes = [arr_i, arr_d, arr_d, c_int, arr_d, arr_d, c_int]

    # Bin particles into yvals array

    lib.binning_1d(xidx, mass, y, npart, sums, yvals, npixels)

    # Divide by total mass

    idx = sums != 0
    yvals[idx] /= sums[idx]

    # Set empty pixels to nan

    idx = sums == 0.
    yvals[idx] = np.nan

    # Set x-axis range

    xvals = xmin + (xmax - xmin) * np.arange(npixels) / npixels

    return xvals, yvals
    
