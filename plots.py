
from include import *
from utils import *

def plot_lines(self, fig, x, y):

    xmin = np.min(x)
    xmax = np.max(x)

    idx = np.invert(np.isnan(y))

    ymin = np.min(y[idx])
    ymax = np.max(y[idx])

    bottom = 0.1
    left = 0.11
    right = 0.02
    
    frac = 1. - left - right
    top = 1. - bottom - frac

    axes = fig.add_axes([left, bottom, frac, frac])

    axes.plot(x, y)

    axes.set_xlim(xmin = xmin, xmax = xmax)
    axes.set_ylim(ymin = ymin, ymax = ymax)

    return axes

def plot_pspace(self, fig, vals, bds, xfield, yfield):

    # Draw image

    bottom = 0.1
    left = 0.11
    right = 0.08
    frac_cbar = 0.03

    frac = 1. - left - right
    top = 1. - bottom - frac_cbar - frac

    ax = fig.add_axes([left, bottom, frac, frac])

    im = ax.imshow(vals, cmap = mp.cm.jet, extent = bds, origin = 'lower', aspect = 'auto')

    # Add labels

    ax.set_xlabel(get_label(xfield))
    ax.set_ylabel(get_label(yfield))

    offset_x = 0.01
    offset_y = 0.05

    text = r'${\rm log}\,M/M_{\rm tot}$'
    
    fig.text(left + frac + offset_x, bottom + frac + offset_y, text, rotation = 270)

    # Add color bar
    
    cax = fig.add_axes([left, bottom + frac, frac, frac_cbar])

    fig.colorbar(im, cax = cax, orientation = 'horizontal')

    cax.xaxis.set_ticks_position('top')
    cax.yaxis.set_label_position('right')
