
from include import *

# Initialize settings

def get_settings(self):

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

    # These refined fields are available. Note: you should also set how they are calculated in fields.py

    self.refined_fields_exist = [['pos', 3, np.dtype('float64')],
                                 ['vel', 3, np.dtype('float64')],
                                 ['id', 1, np.dtype('int32')],
                                 ['mass', 1, np.dtype('float64')],
                                 ['rho', 1, np.dtype('float64')],
                                 ['nh', 1, np.dtype('float64')],
                                 ['temp', 1, np.dtype('float64')],
                                 ['vol', 1, np.dtype('float64')],
                                 ['gravacc', 3, np.dtype('float64')],
                                 ['gradp', 3, np.dtype('float64')],
                                 ['abhm', 1, np.dtype('float64')],
                                 ['abh2', 1, np.dtype('float64')],
                                 ['abhii', 1, np.dtype('float64')],
                                 ['gamma', 1, np.dtype('float64')],
                                 ['allowref', 1, np.dtype('int32')],
                                 ['divvel', 1, np.dtype('float64')]]
