
from sator import *

sator = sator('par.txt')

sator.get_header('test', '1')

sator.init_fields(0)

fig = mp.figure.Figure()

canvas = FigureCanvasAgg(fig)

vals, bds = sator.get_pspace('nh', 'temp', 500)

sator.plot_pspace(fig, vals, bds, 'nh', 'temp')

canvas.print_figure('out.pdf')
