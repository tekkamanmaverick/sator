
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

bottom = 0.1
left = 0.05
right = 0.02
top = 0.02

fig = mp.figure.Figure(figsize = (xsize, ysize))

canvas = FigureCanvasTkAgg(fig)

grid = AxesGrid(fig, [left, bottom, 1. - left - right, 1. - bottom - top], nrows_ncols = (nrows, ncols), axes_pad = 0., aspect = False)

objs = list()

for i in np.arange(nfiles):

    objs.append(sator('par.txt'))

    if i == 0:
        base = 'test'
        num = 1
    elif i == 1:
        base = 'mh1w2r1'
        num = 0
    elif i == 2:
        base = 'mh2w1r1'
        num = 48
    elif i == 3:
        base = 'mh2w1r1'
        num = 0
    elif i == 3:
        base = 'mh3w1r1'
        num = 73
    elif i == 4:
        base = 'mh3w2r1'
        num = 73
    elif i == 5:
        base = 'mh5w1r1'
        num = 273
    elif i == 6:
        base = 'mh5w2r1'
        num = 90

    objs[i].get_header(base, num)

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

cax = fig.add_axes([0.5 - width / 2., 0.04, width, height])

fig.colorbar(im, cax = cax, orientation = 'horizontal')

cax.set_xlabel(r'${\rm log}\,M/M_{\rm tot}$')
    
canvas.print_figure('out.pdf')
