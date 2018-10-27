
from include import *
from utils import *

# Initialize settings

def get_settings(self, par_file):

    # Relative size of main window

    self.win_fac = 0.5

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

    self.length_units = {'kpc': kpc_in_cm,
                         'Mpc': mpc_in_cm,
                         'pc': pc_in_cm,
                         'au': au_in_cm,
                         'solar radii': rsun_in_cm}

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

    # Read parameter file

    snap_fields_file = get_parameters(par_file)

    # Get snap fields (only relevant for snapshot format 1)

    self.snap_fields_exist = read_snap_fields(snap_fields_file)

    self.snap_fields_nfields = len(self.snap_fields_exist)
    self.snap_fields_rank = len(self.snap_fields_exist[0])

# Read parameter file

def get_parameters(par_file):

    if not par_file:

        nargs = len(sys.argv)

        if nargs < 2:
            endrun('Not enough arguments specified on command line! Exiting...')

        par_file = sys.argv[1]

    f = open(par_file, 'r')

    for line in f:

        columns = line.split()

        if columns:
            if columns[0] == 'SnapFieldsFile':
                snap_fields_file = columns[1]

    f.close()

    return snap_fields_file

# Read snap fields file specified in paramater file

def read_snap_fields(snap_fields_file):

    # Read file
    
    f = open(snap_fields_file, 'r')

    n = 0
    refined_fields_exist = []

    for line in f:

        columns = line.split()

        if columns:
            refined_fields_exist.append([])

            for i in np.arange(len(columns)):
                refined_fields_exist[n].append(columns[i])
            n += 1

    # Replace dimensionality string with an integer

    idx = 1

    for entry in refined_fields_exist:
        entry[idx] = int(entry[idx])

    # Replace data type with the corresponding data type

    idx = 2

    for entry in refined_fields_exist:

        if entry[idx] == 'i':
            entry[idx] = np.dtype('int32')
        elif entry[idx] == 'l':
            entry[idx] = np.dtype('int64')
        elif entry[idx] == 'f':
            entry[idx] = np.dtype('float32')
        else:
            entry[idx] = np.dtype('float64')

    f.close()

    return refined_fields_exist
