
from include import *
from utils import *

def get_pspace(self, xfield, yfield, npixels):

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

    ymin = np.min(y)
    ymax = np.max(y)

    # Get indices for all cells

    xidx = (x - xmin) * npixels / (xmax - xmin)
    yidx = (y - ymin) * npixels / (ymax - ymin)

    # Convert to integer

    xidx = xidx.astype(dtype = np.dtype('int32'))
    yidx = yidx.astype(dtype = np.dtype('int32'))

    # Limit integers

    xidx = np.minimum(np.maximum(xidx, 0), npixels - 1)
    yidx = np.minimum(np.maximum(yidx, 0), npixels - 1)

    # Intitialize results array

    vals = np.zeros(npixels**2)

    # Load binning library

    arr_i = npct.ndpointer(dtype = np.dtype('int32'), ndim = 1, flags = 'CONTIGUOUS')
    arr_d = npct.ndpointer(dtype = np.dtype('float64'), ndim = 1, flags = 'CONTIGUOUS')
    lib = npct.load_library("binning", ".")
    lib.restype = None
    lib.binning_2d.argtypes = [arr_i, arr_i, arr_d, c_int, arr_d, c_int]

    # Bin particles into vals array

    lib.binning_2d(xidx, yidx, mass, npart, vals, npixels)

    # Divide by total mass

    tot_mass = np.sum(vals)
    idx = vals > 0.
    vals[idx] /= tot_mass

    # Take logarithm of fractional mass

    vals[idx] = np.log10(vals[idx])

    # Set empty pixels to nan

    idx = vals == 0.
    vals[idx] = np.nan

    # Reshape

    vals = np.reshape(vals, (npixels, npixels))
    vals = np.swapaxes(vals, 0, 1)

    # Get boundaries

    bds = [xmin, xmax, ymin, ymax]

    return vals, bds
