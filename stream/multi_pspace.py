
import os, sys

sys.path.append(os.getenv('SATORDIR'))

from mpl_toolkits.axes_grid1 import ImageGrid

from sator import *

nfiles = 4
nrows = 2
ncols = 2

xfield = 'nh'
yfield = 'temp'

xsize = 15.
ysize = 20.

bottom = 0.09
left = 0.05
right = 0.02
top = 0.02

fig = mp.figure.Figure(figsize = (xsize, ysize))

canvas = FigureCanvasTkAgg(fig)

grid = ImageGrid(fig, [left, bottom, 1. - left - right, 1. - bottom - top], nrows_ncols = (nrows, ncols), axes_pad = 0., aspect = False)

objs = list()

for i in np.arange(nfiles):

    objs.append(sator('par.txt'))

    if i == 1:
        objs[i].get_header('test', 1)
    else:
        objs[i].get_header('test', 0)

    objs[i].init_fields(0)

    #axes = fig.add

    #sator.get_image('Slice', 'temp', 30., 'au', 500, 0)
    #sator.get_image('Projection', 'temp', 10., 'au', 500, 0)
    vals, bds = objs[i].get_pspace(xfield, yfield, 500)
    #x, y = sator.get_lines('nh', 'temp', 100)
    im = grid[i].imshow(vals, cmap = mp.cm.jet, extent = bds, origin = 'lower', aspect = 'auto')

    if i >= nrows * ncols - ncols:
        grid[i].set_xlabel(get_label(xfield))

    if i % ncols == 0:
        grid[i].set_ylabel(get_label(yfield))
    #ax.set_ylabel(get_label(yfield))

    #ax = fig.add_axes([0, 0, 1., 1.])
    #im = ax.imshow(vals, cmap = mp.cm.jet, extent = bds, origin = 'lower', aspect = 'auto')
    #axes = sator.plot_pspace(fig, vals, bds)

    #axes = sator.plot_lines(sator.fig, x, y)

height = 0.015
width = 0.3

cax = fig.add_axes([0.5 - width / 2., 0.03, width, height])

fig.colorbar(im, cax = cax, orientation = 'horizontal')

cax.set_xlabel(r'${\rm log}\,M/M_{\rm tot}$')
    
canvas.print_figure('out.pdf')
