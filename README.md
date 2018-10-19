The installation is very simple:

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
3. Set the environment variable DATADIR to point at the folder with the snapshot data. For example, the snapshot files of a simulation named 'test' must be located in $DATADIR/test/, and the files must be named e.g. test_000 in that directory.
4. Start the program with 'python sator.py'. If all goes well you should see the main menu.

Please report any bugs to the Issues site, email me, or simply fix it yourself. Have fun!