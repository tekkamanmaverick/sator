
from include import *
from snap import *
from utils import *

def init_fields(self):

    self.flag_error = 0

    # These fields exist in the snapshot in this order (for format 1)

    self.snap_fields_exist = [['Coordinates', 3, np.dtype('float64')],
                              ['Velocities', 3, np.dtype('float64')],
                              ['ParticleIDs', 1, np.dtype('int32')],
                              ['Masses', 1, np.dtype('float64')],
                              ['InternalEnergy', 1, np.dtype('float64')],
                              ['Density', 1, np.dtype('float64')],
                              ['Volume', 1, np.dtype('float64')],
                              ['Acceleration', 3, np.dtype('float64')],
                              ['PressureGradient', 3, np.dtype('float64')],
                              ['ChemicalAbundances', 3, np.dtype('float64')],
                              ['Gamma', 1, np.dtype('float64')], 
                              ['AllowRefinement', 1, np.dtype('int32')],
                              ['VelocityDivergence', 1, np.dtype('float64')]]

    self.snap_fields_nfields = len(self.snap_fields_exist)
    self.snap_fields_rank = len(self.snap_fields_exist[0])

    # For a given particle type, these fields are present

    if self.flag_hdf5:
        
        self.snap_file = h5py.File(self.snap_name, 'r')

        str_part_type = 'PartType' + self.part_type.get()

        part = self.snap_file.get(str_part_type)
        
        keys = part.keys()

        self.snap_fields = dict.fromkeys(keys, np.empty(0))
        self.snap_fields_dims = {}
        self.snap_fields_dtypes = {}

        for field in self.snap_fields:

            ds = part.get(field)

            if len(ds.shape) == 1:
                self.snap_fields_dims[field] = 1
            else:

                self.snap_fields_dims[field] = ds.shape[1]

            self.snap_fields_dtypes[field] = ds.dtype

        self.snap_file.close

    else:

        self.snap_fields = {}
        self.snap_fields_dims = {}
        self.snap_fields_dtypes = {}

        for i in np.arange(self.snap_fields_nfields):

            snap_field = self.snap_fields_exist[i][0]

            self.snap_fields[snap_field] = np.empty(0)
            self.snap_fields_dims[snap_field] = self.snap_fields_exist[i][1]
            self.snap_fields_dtypes[snap_field] = self.snap_fields_exist[i][2]

    # These refined fields are available

    refined_fields = [['pos', 3, np.dtype('float64')],
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

    self.refined_fields_nfields = len(refined_fields)
    self.refined_fields_rank = len(refined_fields[0])

    # Set which snapshot fields are required for each refined field

    fields_req = {}

    fields_req['pos'] = ['Coordinates']
    fields_req['vel'] = ['Velocities']
    fields_req['id'] = ['ParticleIDs']
    fields_req['mass'] = ['Masses']
    fields_req['rho'] = ['Density']
    fields_req['nh'] = ['Density']
    fields_req['temp'] = ['InternalEnergy', 'Gamma']
    fields_req['vol'] = ['Volume']
    fields_req['gravacc'] = ['Acceleration']
    fields_req['gradp'] = ['PressureGradient']
    fields_req['abhm'] = ['ChemicalAbundances']
    fields_req['abh2'] = ['ChemicalAbundances']
    fields_req['abhii'] = ['ChemicalAbundances']
    fields_req['gamma'] = ['Gamma']
    fields_req['allowref'] = ['AllowRefinement']
    fields_req['divvel'] = ['VelocityDivergence']

    # For a given particle type, these refined fields are available

    self.refined_fields = {}
    self.refined_fields_dims = {}
    self.refined_fields_dtypes = {}

    for i in np.arange(self.refined_fields_nfields):

        field = refined_fields[i][0]
        
        snap_field_list = fields_req[field]

        flag = 1

        if not snap_field_list:
            flag = 0

        for snap_sub_field in snap_field_list:
            if snap_sub_field not in list(self.snap_fields):
                flag = 0
        if flag:
            self.refined_fields[field] = np.empty(0)
            self.refined_fields_dims[field] = refined_fields[i][1]
            self.refined_fields_dtypes[field] = refined_fields[i][2]

    if not self.refined_fields:
        sator.flag_error = 1

def get_plot_fields(self):

    self.plot_fields = {}

    for field in self.refined_fields:
        if self.refined_fields_dims[field] == 1:
            if self.refined_fields_dtypes[field] == np.dtype('float64'):
                self.plot_fields[field] = self.refined_fields[field]

def get_refined_field(self, field):

    if self.refined_fields[field].size:

        return self.refined_fields[field]

    else:

        print 'Reading field', field, '..'

        header = self.header

        h = header.HubbleParam
        redshift = header.redshift
        unit_length = header.unit_length
        unit_mass = header.unit_mass
        unit_velocity = header.unit_velocity
        unit_time = header.unit_time
        unit_energy = header.unit_energy

        if field == 'pos':
            vals = self.get_snap_field('Coordinates')
            fac = 1. / h * unit_length
            vals *= fac
        elif field == 'vel':
            vals = self.get_snap_field('Velocities')
            fac = 1. / np.sqrt(1. + redshift) * unit_velocity
            vals *= fac
        elif field == 'id':
            vals = self.get_snap_field('ParticleIDs')
        elif field == 'mass':
            vals = self.get_snap_field('Masses')
            fac = 1. / h * unit_mass
            vals *= fac
        elif field == 'rho':
            vals = self.get_snap_field('Density')
            fac = h**2 * (1. + redshift)**3 * unit_mass / unit_length**3
            vals *= fac
        elif field == 'nh':
            vals = self.get_snap_field('Density')
            fac = h**2 * (1. + redshift)**3 * unit_mass / unit_length**3
            vals *= fac
            fac = hydrogen_massfrac / protonmass
            vals *= fac
        elif field == 'u':
            vals = self.get_snap_field('InternalEnergy')
            fac = unit_energy / unit_mass
            vals *= fac
        elif field == 'temp':
            u = self.get_snap_field('InternalEnergy')
            fac = unit_energy / unit_mass
            u *= fac
            gamma = self.get_snap_field('Gamma')
            chem = self.get_snap_field('ChemicalAbundances')
            abhm = chem[:, 0]
            abh2 = chem[:, 1]
            abhii = chem[:, 2]
            abe = abhii
            mu = (1. + 4. * abhe) / (1. + abhe - abh2 + abe)
            vals = mu * (gamma - 1.) * protonmass / boltzmann * u
        elif field == 'vol':
            vals = self.get_snap_field('Volume')
            fac = (1. / h)**3 * unit_length**3
            vals *= fac
        elif field == 'gravacc':
            vals = self.get_snap_field('Acceleration')
            fac = (1. + redshift)**2
            vals /= fac
        elif field == 'gradp':
            vals = self.get_snap_field('PressureGradient')
            fac = (1. + redshift)**4 * h**3
            vals *= fac
        elif field == 'abhm':
            vals = self.get_snap_field('ChemicalAbundances')
            vals = vals[:, 0]
        elif field == 'abh2':
            vals = self.get_snap_field('ChemicalAbundances')
            vals = vals[:, 1]
        elif field == 'abhii':
            vals = self.get_snap_field('ChemicalAbundances')
            vals = vals[:, 2]
        elif field == 'gamma':
            vals = self.get_snap_field('Gamma')
        elif field == 'allowref':
            vals = self.get_snap_field('AllowRefinement')
        elif field == 'divvel':
            vals = self.get_snap_field('VelocityDivergence')
            fac = (1. + redshift) * h * unit_velocity / unit_length
            vals *= fac
        else:
            endrun('Field not recognized!')

        self.refined_fields[field] = vals

        return vals
