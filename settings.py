
from include import *
from utils import *

# Initialize settings

def get_settings(self, par_file):

    # Directory of snapshot data

    self.data_dir = os.environ['DATA_DIR']

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

    self.length_units = {'kpc': kpc_in_cm,
                         'Mpc': mpc_in_cm,
                         'pc': pc_in_cm,
                         'au': au_in_cm,
                         'solar radii': rsun_in_cm}

    # These refined fields are available. Note: you should also set how they are calculated in fields.py

    self.refined_fields_exist = [['pos', 3, 'float64'],
                                 ['r', 1, 'float64'],
                                 ['vel', 3, 'float64'],
                                 ['id', 1, 'int32'],
                                 ['mass', 1, 'float64'],
                                 ['u', 1, 'float64'],
                                 ['rho', 1, 'float64'],
                                 ['nh', 1, 'float64'],
                                 ['temp', 1, 'float64'],
                                 ['vol', 1, 'float64'],
                                 ['h', 1, 'float64'],
                                 ['gravacc', 3, 'float64'],
                                 ['gradp', 3, 'float64'],
                                 ['abhm', 1, 'float64'],
                                 ['abh2', 1, 'float64'],
                                 ['abhii', 1, 'float64'],
                                 ['gamma', 1, 'float64'],
                                 ['allowref', 1, 'int32'],
                                 ['divvel', 1, 'float64']]

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
    snap_fields_exist = []

    for line in f:

        columns = line.split()

        if columns:
            snap_fields_exist.append([])

            for i in np.arange(len(columns)):
                snap_fields_exist[n].append(columns[i])
            n += 1

    # Save list of particle types for which the fields are present

    idx = 1

    for entry in snap_fields_exist:

        tl = entry[idx]

        tl = tl.split(',')

        tl = np.array(tl)

        tl = tl.astype(np.dtype('int32'))

        tl = np.sort(tl)

        entry[idx] = tl

    # Replace dimensionality string with an integer

    idx = 2

    for entry in snap_fields_exist:
        entry[idx] = int(entry[idx])

    # Replace data type string with numpy data type

    idx = 3

    for entry in snap_fields_exist:
        entry[idx] = np.dtype(entry[idx])

    f.close()

    return snap_fields_exist
