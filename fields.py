
from include import *
from snap import *
from utils import *

def init_fields(self, part_type):

    self.flag_error = 0

    # Set particle type

    self.part_type = part_type

    # For a given particle type, these snap fields are present

    if self.flag_hdf5:

        self.snap_file = h5py.File(self.snap_name, 'r')

        str_part_type = 'PartType' + str(part_type)

        part = self.snap_file.get(str_part_type)
        
        keys = part.keys()

        self.snap_fields = dict.fromkeys(keys, np.empty(0))
        self.snap_fields_nentries = {}
        self.snap_fields_dtypes = {}

        for field in self.snap_fields:

            ds = part.get(field)

            if len(ds.shape) == 1:
                self.snap_fields_nentries[field] = 1
            else:
                self.snap_fields_nentries[field] = ds.shape[1]

            self.snap_fields_dtypes[field] = ds.dtype

        self.snap_file.close

    else:

        self.snap_fields = {}
        self.snap_fields_nentries = {}
        self.snap_fields_dtypes = {}

        for i in np.arange(self.snap_fields_nfields):

            snap_field = self.snap_fields_exist[i][0]

            self.snap_fields[snap_field] = np.empty(0)
            self.snap_fields_nentries[snap_field] = self.snap_fields_exist[i][1]
            self.snap_fields_dtypes[snap_field] = self.snap_fields_exist[i][2]

    # Inititalize refined fields for selected particle type

    self.refined_fields_nfields = len(self.refined_fields_exist)
    self.refined_fields_rank = len(self.refined_fields_exist[0])
    self.refined_fields = {}
    self.refined_fields_nentries = {}
    self.refined_fields_dtypes = {}

    for i in np.arange(self.refined_fields_nfields):

        field = self.refined_fields_exist[i][0]
        
        self.refined_fields[field] = np.empty(0)
        self.refined_fields_nentries[field] = self.refined_fields_exist[i][1]
        self.refined_fields_dtypes[field] = self.refined_fields_exist[i][2]

    # If a new type is read, this will be the first time the plot is created
        
    self.flag_plot_first = 1

    # Return an error if no refined fields are present

    if not self.refined_fields:
        return 1
    else:
        return 0

def get_plot_fields(self):

    self.plot_fields = {}

    for field in self.refined_fields:
        if self.refined_fields_nentries[field] == 1:
            if self.refined_fields_dtypes[field] == np.dtype('float64'):
                self.plot_fields[field] = self.refined_fields[field]

def get_refined_field(self, refined_field):

    flag = 0

    if self.refined_fields[refined_field].size:

        return flag, self.refined_fields[refined_field]

    else:

        print 'Reading refined field \'' + refined_field + '\'..'

        header = self.header

        h = header.HubbleParam
        redshift = header.redshift
        unit_length = header.unit_length
        unit_mass = header.unit_mass
        unit_velocity = header.unit_velocity
        unit_time = header.unit_time
        unit_energy = header.unit_energy

        if refined_field == 'pos':

            snap_field = 'Coordinates'

            flag, vals = self.get_snap_field(snap_field)

            if flag:
                self.snap_field_error(snap_field)
            else:
                fac = 1. / h * unit_length
                vals *= fac

        elif refined_field == 'vel':

            snap_field = 'Velocities'

            flag, vals = self.get_snap_field(snap_field)

            if flag:
                self.snap_field_error(snap_field)
            else:
                fac = 1. / np.sqrt(1. + redshift) * unit_velocity
                vals *= fac

        elif refined_field == 'id':

            snap_field = 'ParticleIDs'

            flag, vals = self.get_snap_field('ParticleIDs')

            if flag:
                self.snap_field_error(snap_field)

        elif refined_field == 'mass':

            snap_field = 'Masses'

            flag, vals = self.get_snap_field(snap_field)

            if flag:
                self.snap_field_error(snap_field)
            else:
                fac = 1. / h * unit_mass
                vals *= fac

        elif refined_field == 'rho':

            snap_field = 'Density'

            flag, vals = self.get_snap_field(snap_field)

            if flag:
                self.snap_field_error(snap_field)
            else:
                fac = h**2 * (1. + redshift)**3 * unit_mass / unit_length**3
                vals *= fac

        elif refined_field == 'nh':

            snap_field = 'Density'

            flag, vals = self.get_snap_field(snap_field)

            if flag:
                self.snap_field_error(snap_field)
            else:
                fac = h**2 * (1. + redshift)**3 * unit_mass / unit_length**3
                vals *= fac
                fac = hydrogen_massfrac / protonmass
                vals *= fac

        elif refined_field == 'u':

            snap_field = 'InternalEnergy'

            flag, vals = self.get_snap_field(snap_field)

            if flag:
                self.snap_field_error(snap_field)
            else:
                fac = unit_energy / unit_mass
                vals *= fac

        elif refined_field == 'temp':

            snap_field = 'Gamma'

            flag, gamma = self.get_snap_field(snap_field)

            if flag:
                gamma = gamma_adb

            snap_field = 'ChemicalAbundances'

            flag, chem = self.get_snap_field(snap_field)

            if flag:
                mu = mu_prim
            else:
                abhm = chem[:, 0]
                abh2 = chem[:, 1]
                abhii = chem[:, 2]
                abe = abhii
                mu = (1. + 4. * abhe) / (1. + abhe - abh2 + abe)

            snap_field = 'InternalEnergy'

            flag, u = self.get_snap_field(snap_field)

            if flag:
                self.snap_field_error(snap_field)
            else:
                fac = unit_energy / unit_mass
                u *= fac
                vals = mu * (gamma - 1.) * protonmass / boltzmann * u

        elif refined_field == 'vol':

            snap_field = 'Volume'

            flag, vals = self.get_snap_field(snap_field)

            if flag:
                self.snap_field_error(snap_field)
            else:
                fac = (1. / h)**3 * unit_length**3
                vals *= fac

        elif refined_field == 'gravacc':

            snap_field = 'Acceleration'

            flag, vals = self.get_snap_field(snap_field)

            if flag:
                self.snap_field_error(snap_field)
            else:
                fac = (1. + redshift)**2
                vals /= fac

        elif refined_field == 'gradp':

            snap_field = 'PressureGradient'

            flag, vals = self.get_snap_field(snap_field)

            if flag:
                self.snap_field_error(snap_field)
            else:
                fac = (1. + redshift)**4 * h**3
                vals *= fac

        elif refined_field == 'abhm':

            snap_field = 'ChemicalAbundances'

            flag, vals = self.get_snap_field(snap_field)

            if flag:
                self.snap_field_error(snap_field)
            else:
                vals = vals[:, 0]

        elif refined_field == 'abh2':

            snap_field = 'ChemicalAbundances'

            flag, vals = self.get_snap_field(snap_field)

            if flag:
                self.snap_field_error(snap_field)
            else:
                vals = vals[:, 1]

        elif refined_field == 'abhii':

            snap_field = 'ChemicalAbundances'

            flag, vals = self.get_snap_field(snap_field)

            if flag:
                self.snap_field_error(snap_field)
            else:
                vals = vals[:, 2]

        elif refined_field == 'gamma':

            snap_field = 'Gamma'

            flag, vals = self.get_snap_field(snap_field)

            if flag:
                self.snap_field_error(snap_field)

        elif refined_field == 'allowref':

            snap_field = 'AllowRefinement'

            flag, vals = self.get_snap_field(snap_field)

            if flag:
                self.snap_field_error(snap_field)

        elif refined_field == 'divvel':

            snap_field = 'VelocityDivergence'

            flag, vals = self.get_snap_field(snap_field)

            if flag:
                self.snap_field_error(snap_field)
            else:
                fac = (1. + redshift) * h * unit_velocity / unit_length
                vals *= fac

        else:
            flag = 1

        if flag:
            self.refined_fields[refined_field] = np.empty(0)
        else:
            self.refined_fields[refined_field] = vals

        return flag, vals
