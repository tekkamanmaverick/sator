**Installation**

1. If not already present, install Python. Usually default installations of Python already include the required modules, so no additional steps should be necessary. These modules are required:
	* numpy
	* scipy
	* matplotlib
	* mpl_toolkits
	* h5py
	* ctypes
	* struct, sys, os
	* ScrolledText, Tkinter
2. Git clone the repository to your favorite location
3. Set the environment variable DATADIR to point to the folder with the snapshot data. For example, the snapshot files of a simulation named *test* must be located in *$DATADIR/test/*, and the files must be named e.g. *test_000* in that directory.
4. Type `make` in the sator directory to compile the C libraries
5. Copy `par_template.txt` to your own parameter file (e.g. `par.txt`) and set the parameters
4. Start the program with `python sator.py par.txt`. If all goes well you should see the main menu.

Please report any bugs to the Issues site, email me at *tgreif@uni-heidelberg.de*, or simply fix it yourself.

**Fields in Sator**

In Sator there are two different kinds of fields: *snap fields* and *refined fields*. The former are fields as they exist in the snapshots, e.g. *Coordinates* in an HDF5 file. The *refined fields* are computed from the *snap fields* and are typically used for plots, e.g. the temperature (refined field *temp*) is computed from the *InternalEnergy*, as well as *Gamma* and *ChemicalAbundances*, if the latter two are present in the snapshot. A new refined field, together with its dimensionality and data type, can be specified in settings.py. Its calculation from the *snap fields* is defined in fields.py in the routine *get_refined_field*.

For snapshot format 1, the snap fields, their properties and their order in the snapshot must be defined in a file specified by the parameter `SnapFieldsFile` in the paramater file.