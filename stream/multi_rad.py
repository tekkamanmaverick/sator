
import os, sys

sys.path.append(os.getenv('SATORDIR'))

from sator import *

mp.rcParams.update({'font.size': 18})

nfiles = 1
nrows = 1
ncols = 1

xfield = 'nh'
yfield = 'temp'

xsize = 17.
ysize = 20.

bottom = 0.04
left = 0.05
right = 0.02
top = 0.02

fig = mp.figure.Figure(figsize = (xsize, ysize))

canvas = FigureCanvasTkAgg(fig)

grid = AxesGrid(fig, [left, bottom, 1. - left - right, 1. - bottom - top], nrows_ncols = (nrows, ncols), axes_pad = 0., aspect = False)

objs = list()

for i in np.arange(nfiles):

    objs.append(sator('par.txt'))

    if i == 1:
        objs[i].get_header('test', 1)
    else:
        objs[i].get_header('test', 0)

    objs[i].init_fields(0)

    x, y = objs[i].get_lines('r', 'temp', 100)

    x = 10.**x
    x /= au_in_cm
    x = np.log10(x)
    
    xmin = np.min(x)
    xmax = np.max(x)

    idx = np.invert(np.isnan(y))

    ymin = np.min(y[idx])
    ymax = np.max(y[idx])
    
    grid[i].plot(x, y)

    grid[i].set_xlim(xmin = xmin, xmax = xmax)
    grid[i].set_ylim(ymin = ymin, ymax = ymax)

    #grid[i].xaxis.set_ticks_position('both')
    
    if i >= nrows * ncols - ncols:
        grid[i].set_xlabel(get_label(xfield))

    if i % ncols == 0:
        grid[i].set_ylabel(get_label(yfield))

canvas.print_figure('out.pdf')
