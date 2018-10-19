
from include import *

# Initialize settings

def init_settings(self):

    # Relative size of main window

    self.win_fac = 0.8

    # Default DPI of matplotlib

    self.fig_dpi = 100

    # Width of entry boxes in characters

    self.entry_width = 10

    # Factor by which image is zoomed

    self.zoom_fac = 0.5

    # Factor by which image is moved

    self.move_fac = 0.3

    # Angle by which image is rotated

    self.rot_delta = np.pi / 12.

    # Length units available for images

    self.length_units = {'kpc': kpc_in_cm, 'Mpc': mpc_in_cm, 'pc': pc_in_cm, 'au': au_in_cm, 'solar radii': rsun_in_cm}
