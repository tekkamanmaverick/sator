
from include import *
from utils import *

def get_header(self, base, snapnum, sub_num = 0, verbose = 1):

    # Initialize some variables

    self.base = base
    self.snapnum = snapnum

    self.header = header()

    if verbose:
        print 'Reading snapshot...'

    self.flag_error = 0

    # Determine whether a snapshot or an IC file is present

    if snapnum == 'ic':
        snap_string = snapnum
    else:
        snap_string = repr(int(snapnum)).zfill(3)

    # Check if snapshot is in a subdirectory

    self.snap_path = self.data_dir + '/' + base + '/' + 'snapdir_' + snap_string

    if os.path.isdir(self.snap_path):
        self.flag_subdir = 1
    else:
        self.flag_subdir = 0
        self.snap_path = self.data_dir + '/' + base

    # Check snapshot format and if it is distributed among multiple files

    self.snap_path += '/' + base + '_' + snap_string

    if os.path.exists(self.snap_path):
        self.flag_multiple = 0
        self.flag_hdf5 = 0
        self.snap_name = self.snap_path
    elif os.path.exists(self.snap_path + '.hdf5'):
        self.flag_multiple = 0
        self.flag_hdf5 = 1
        self.snap_name = self.snap_path + '.hdf5'
    elif os.path.exists(self.snap_path + '.' + str(sub_num)):
        self.flag_multiple = 1
        self.flag_hdf5 = 0
        self.snap_name = self.snap_path + '.' + str(sub_num)
    elif os.path.exists(self.snap_path + '.' + str(sub_num) + '.hdf5'):
        self.flag_multiple = 1
        self.flag_hdf5 = 1
        self.snap_name = self.snap_path + '.' + str(sub_num) + '.hdf5'
    else:
        self.flag_error = 1
        return

    if verbose:

        if self.flag_hdf5:
            print 'Snapshot is in HDF5 (format 3)'
        else:
            print 'Snapshot is in binary (format 1 or 2)'    

    # Read header

    if self.flag_hdf5:

        # Open file

        snap_file = h5py.File(self.snap_name, 'r')

        h5py_header = snap_file['Header'].attrs

        # Save header data

        self.header.npart = h5py_header['NumPart_ThisFile']
        self.header.mass = h5py_header['MassTable']
        self.header.time = h5py_header['Time']
        self.header.redshift = h5py_header['Redshift']
        self.header.flag_sfr = h5py_header['Flag_Sfr']
        self.header.flag_feedback = h5py_header['Flag_Feedback']
        self.header.npartTotal = h5py_header['NumPart_Total']
        self.header.flag_cooling = h5py_header['Flag_Cooling']
        self.header.numfiles = h5py_header['NumFilesPerSnapshot']
        self.header.BoxSize = h5py_header['BoxSize']
        self.header.Omega0 = h5py_header['Omega0']
        self.header.OmegaLambda = h5py_header['OmegaLambda']
        self.header.HubbleParam = h5py_header['HubbleParam']
        self.header.flag_stellarage = h5py_header['Flag_StellarAge']
        self.header.flag_metals = h5py_header['Flag_Metals']
        self.header.npartTotalHighWord = h5py_header['NumPart_Total_HighWord']
        self.header.flag_stellarage = h5py_header['Flag_StellarAge']
        self.header.flag_doubleprecision = h5py_header['Flag_DoublePrecision']
        self.header.composition_vector_length = h5py_header['Composition_vector_length']

        # Some additional variables for format 3

        self.header.numtypes = snap_file['Config'].attrs.get('NTYPES', default = 6)
        self.header.unit_length = h5py_header['UnitLength_in_cm']
        self.header.unit_mass = h5py_header['UnitMass_in_g']
        self.header.unit_velocity = h5py_header['UnitVelocity_in_cm_per_s']

        # Close file

        snap_file.close()

    else:

        # Open file

        snap_file = open(self.snap_name, 'rb')

        # Read header

        self.header_size = struct.unpack('i', snap_file.read(4))[0]
        binary = snap_file.read(self.header_size)
        self.header_size = struct.unpack('i', snap_file.read(4))[0]

        # Set header data types

        string = ''

        for i in np.arange(NPARTTYPES):
            string += 'i'

        for i in np.arange(NPARTTYPES):
            string += 'd'

        string += 'ddii'
    
        for i in np.arange(NPARTTYPES):
            string += 'i'

        string += 'iiddddii'

        for i in np.arange(NPARTTYPES):
            string += 'I'

        string += 'iiidii'

        # Set padding
            
        size_i = string.count('i') * struct.calcsize('i')
        size_u = string.count('I') * struct.calcsize('I')
        size_d = string.count('d') * struct.calcsize('d')

        size_tot = size_i + size_u + size_d

        diff = (self.header_size - size_tot) / 4

        for i in np.arange(diff - 1):
            string += 'i'

        # Save data in header

        data = struct.unpack(string, binary)

        p = 0
        self.header.npart = data[p : p + NPARTTYPES]
        p += NPARTTYPES
        self.header.mass = data[p : p + NPARTTYPES]
        p += NPARTTYPES
        self.header.time = data[p]
        p += 1
        self.header.redshift = data[p]
        p += 1
        self.header.flag_sfr = data[p]
        p += 1
        self.header.flag_feedback = data[p]
        p += 1
        self.header.npartTotal = data[p : p + NPARTTYPES]
        p += NPARTTYPES
        self.header.flag_cooling = data[p]
        p += 1
        self.header.numfiles = data[p]
        p += 1
        self.header.BoxSize = data[p]
        p += 1
        self.header.Omega0 = data[p]
        p += 1
        self.header.OmegaLambda = data[p]
        p += 1
        self.header.HubbleParam = data[p]
        p += 1
        self.header.flag_stellarage = data[p]
        p += 1
        self.header.flag_metals = data[p]
        p += 1
        self.header.npartTotalHighWord = data[p : p + NPARTTYPES]
        p += NPARTTYPES
        self.header.flag_entropy_instead_u = data[p]
        p += 1
        self.header.flag_doubleprecision = data[p]
        p += 1
        self.header.flag_lpt_ics = data[p]
        p += 1
        self.header.lpt_scalingfactor = data[p]
        p += 1
        self.header.flag_tracer_field = data[p]
        p += 1
        self.header.composition_vector_length = data[p]

        # Some additional variables for formats 1 and 2

        self.header.numtypes = NPARTTYPES
        self.header.unit_length = 3.085678e21
        self.header.unit_mass = 1.989e43
        self.header.unit_velocity = 1e5

        # Close file

        snap_file.close()

    # Some additional variables for all snapshot formats

    self.header.unit_time = self.header.unit_length / self.header.unit_velocity
    self.header.unit_energy = self.header.unit_mass * self.header.unit_length**2 / self.header.unit_time**2
    self.header.boxsize_cgs = self.header.BoxSize / self.header.HubbleParam * self.header.unit_length

    # Create list of particle types that have at least one particle

    self.header.type_list = []

    for i in np.arange(self.header.numtypes):
        if self.header.npartTotal[i]:
            self.header.type_list.append(i)

    if not self.header.type_list:
        self.flag_error = 2

# Reead desired snap field from snapshot

def get_snap_field(self, snap_field):

    flag = 0

    keys = self.snap_fields.keys()

    # Check if desired snap field exists
    
    if snap_field not in keys:
        return 1, 0

    # Check whether desired snap field has already been read

    if not self.snap_fields[snap_field]:

        # Get header

        header = self.header

        # Get particle type from selection in GUI

        part_type = int(self.part_type)

        # Get total particle number for selected particle type

        ntot = header.npartTotal[part_type]

        # Distinguish between snapshot formats

        if self.flag_hdf5:

            # Get dataset shape and type

            shape = [ntot]

            # Open file

            if self.flag_multiple:
                snap_name = self.snap_path + '.0.hdf5'
            else:
                snap_name = self.snap_path + '.hdf5'

            snap_file = h5py.File(snap_name, 'r')

            # Get string for particle type

            str_part_type = 'PartType' + str(part_type)

            # Get particle group for desired particle type

            part = snap_file.get(str_part_type)

            # Get dataset for desired snap field

            ds = part.get(snap_field)

            # Get dataset type and shape

            ds_type = ds.dtype
            ds_shape = ds.shape

            # Close snapshot

            snap_file.close()

            # Create dataset with corresponding shape

            if len(ds_shape) == 2:
                sub_vals = ds_shape[1]
                shape.append(sub_vals)

            vals = np.zeros(shape, dtype = ds_type)

            # Initialize offset

            offset = 0

            # Go through all files and read dataset

            for i in np.arange(self.header.numfiles):

                # Open file

                if self.flag_multiple:
                    snap_name = self.snap_path + '.' + str(i) + '.hdf5'
                else:
                    snap_name = self.snap_path + '.hdf5'

                snap_file = h5py.File(snap_name, 'r')

                # Get particle group for desired particle type

                part = snap_file.get(str_part_type)

                # Continue if desired type exists

                if part:

                    ds = part.get(snap_field)

                    # Continue if desired field exists

                    if ds:

                        # Get number of particles of desired type

                        npart = snap_file['Header'].attrs['NumPart_ThisFile'][part_type]

                        # Read data in existing array

                        ds.read_direct(vals, np.s_[0 : npart], np.s_[offset : offset + npart])

                        # Add number of particles read to offset

                        offset += npart

                    else:
                        return 1, 0

                else:
                    return 1, 0

                # Close file

                snap_file.close()

        else:

            tot_count = 0

            # Go through all files and read data

            for i in np.arange(self.header.numfiles):

                # Get header for this file to obtain the number of types and the number of particles for each type

                self.get_header(self.base, self.snapnum, i, 0)

                # Open file

                snap_file = open(self.snap_name, 'rb')

                # Add header and SKIP blocks to offset in bytes

                offset = self.header_size + 2 * np.dtype('int32').itemsize

                # Go through all fields present in the snapshot

                for j in np.arange(self.snap_fields_nfields):

                    field = self.snap_fields_exist[j][0]

                    # Go through particle types that are present for the selected field

                    for part_type in self.snap_fields_types[field]:

                        # Get particle number for selected type

                        npart = self.header.npart[part_type]

                        # Continue if particles of the specified type and field exist

                        if npart:

                            # Determine number of entries and bytes per entry

                            count = npart * self.snap_fields_nentries[field]

                            bytes_per_element = self.snap_fields_dtypes[field].itemsize

                            # Read data only for the desired field (and not any previous ones)

                            if field == snap_field:

                                # Read data only for the desired particle type

                                if part_type == self.part_type:

                                    # Go to position in file specified by offset

                                    snap_file.seek(offset)

                                    # Read SKIP block

                                    snap_file.read(np.dtype('int32').itemsize)

                                    # Determine data type

                                    dtype = self.snap_fields_dtypes[field]

                                    # Do actual reading of a field

                                    data = np.fromfile(snap_file, dtype = dtype, count = count)

                                    # If this is the first file, create data set, otherwise resize it

                                    if i == 0:
                                        vals = data
                                    else:
                                        vals.resize(vals.size + count)
                                        vals[tot_count : tot_count + count] = data

                                    # Read SKIP block

                                    snap_file.read(np.dtype('int32').itemsize)

                                    # Add particle number to the total count

                                    tot_count += count

                            # Add this field to the offset

                            offset += count * bytes_per_element

                    # Add SKIP blocks to offset

                    offset += 2 * np.dtype('int32').itemsize

                # Close file

                snap_file.close()

            # Reshape data set to represent the number of entries (e.g. 3 for coordinates)

            nentries = self.snap_fields_nentries[snap_field]

            if nentries > 1:
                vals = vals.reshape((tot_count / nentries, nentries))

        # return error flag and dataset
                
        return flag, vals

    else:

        # This snap field has already been read

        return flag, self.snap_fields[snap_field]

# Error message if a snap field can not be read

def snap_field_error(self, snap_field):

    string = 'Could not read snap field \'' + snap_field + '\''

    self.error_message(string)
