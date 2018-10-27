
from sator import *

sator = sator('par.txt')

sator.get_header('test', '1')

sator.init_fields(0)

sator.fig = mp.figure.Figure()

canvas = FigureCanvasAgg(sator.fig)

sator.get_pspace('nh', 'temp', 500)

canvas.print_figure('out.pdf')
