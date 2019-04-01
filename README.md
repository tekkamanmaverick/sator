**Installation**

Note: Since I have left astrophysics, Volker Springel has assumed ownership of the code. Please contact him for any questions. Under dire circumstances, you may contact me at *tgreif81@gmail.com* :).

1. If not already present, install Python 3. Sator requires the following modules: tkinter, numpy, scipy, matplotlib, mpl_toolkits, h5py, ctypes. Depending on the version of Python you have installed, you might need to install some of these modules. I had to perform the following steps:
	* `sudo apt-get install python3-pip`
	* `sudo apt-get install python3-tk`
	* `pip3 install numpy`
	* `pip3 install scipy`
	* `pip3 install matplotlib`
	* `pip3 install h5py`
2. Git clone the repository to your favorite location
3. Set the environment variable *DATA_DIR* to point to the folder with the snapshot data. For example, the snapshot files of a simulation named *test* must be located in *$DATA_DIR/test/*, and the files must be named e.g. *test_000* in that directory.
4. Copy `par_template.txt` to your own parameter file (e.g. *par.txt*) and set the parameters
5. Copy `snap_fields_template.txt` to your own snapshot fields file (e.g. *snap_fields.txt*) and define the fields in the snapshot for format 1 (Note: this is only necessary for snapshot format 1)
6. Start sator with `./sator.sh`. In this case the parameter file name defaults to *par.txt*. If you are starting Sator for the first time, the C libraries will be compiled. If you want to use a different name for the parameter file, you can manually invoke sator with the command `python3 main.py par_alt.txt`, where *par_alt.txt* is the alternative name of the parameter file. You can also run sator in script mode. An example is given in the file *script.py*. You can run the script with `python3 script.py`.

Please report any bugs to the Issues site, email Volker Springel at *vspringel@mpa-garching.mpg.de*, or simply fix it yourself :).

**Fields in Sator**

In Sator there are two different kinds of fields: snapshot fields and refined fields. The former are fields as they exist in the snapshots, e.g. *Coordinates* in an HDF5 file. The refined fields are computed from the snapshot fields and are typically used for plots, for example the temperature (refined field *temp*). The temperature is computed from the snapshot fields *InternalEnergy*, *Gamma* and *ChemicalAbundances*, if the latter two are present in the snapshot. A new refined field, together with its dimensionality and data type, can be specified in settings.py. Its calculation from the snapshot fields is defined in fields.py in the routine *get_refined_field*.

For snapshot format 1, the snapshot fields, their properties and their order in the snapshot must be defined in a file specified by the parameter `SnapFieldsFile` in the paramater file.