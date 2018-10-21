
from include import *
from utils import *

def get_pspace(self):

    # This is required at the beginning of each plot routine

    self.init_fig()

    # Extract parameters

    opts = self.plot_sub_options

    xfield = opts[1].get()
    yfield = opts[3].get()
    nbins = int(opts[4].get())

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
    
    # Take logarithm
    
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

    xidx = (x - xmin) * nbins / (xmax - xmin)
    yidx = (y - ymin) * nbins / (ymax - ymin)

    # Convert to integer

    xidx = xidx.astype(dtype = np.dtype('int32'))
    yidx = yidx.astype(dtype = np.dtype('int32'))

    # Limit inteegers

    xidx = np.minimum(xidx, nbins - 1)
    yidx = np.minimum(yidx, nbins - 1)

    # Intitialize results array

    vals = np.zeros(nbins**2)

    # Load pspace library

    arr_i = npct.ndpointer(dtype = np.dtype('int32'), ndim = 1, flags = 'CONTIGUOUS')
    arr_d = npct.ndpointer(dtype = np.dtype('float64'), ndim = 1, flags = 'CONTIGUOUS')
    lib = npct.load_library("binning", ".")
    lib.restype = None
    lib.binning.argtypes = [arr_i, arr_i, arr_d, c_int, arr_d, c_int]

    # Bin particles into vals array

    lib.binning(xidx, yidx, mass, mass.size, vals, nbins)

    # Divide by total mass

    tot_mass = np.sum(vals)
    idx = vals > 0.
    vals[idx] /= tot_mass

    # Take logarithm of fractional mass

    vals[idx] = np.log10(vals[idx])

    # Set empty bins to nan
    idx = vals == 0.
    vals[idx] = np.nan

    # Reshape

    vals = np.reshape(vals, (nbins, nbins))
    vals = np.swapaxes(vals, 0, 1)

    # Draw image

    bottom = 0.05
    top = 0.05
    frac_cbar = 0.03

    frac = 1. - bottom - top - frac_cbar
    left = (1. - frac) / 2.

    ax = self.fig.add_axes([left, bottom, frac, frac])

    im = ax.imshow(vals, origin = 'lower')
    
    # This is needed at the end of each plot routine

    self.finish_fig()
