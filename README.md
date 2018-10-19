The installation is very simple:

1. If not already done so, install Python. Usually default installations of Python already include the required modules, so no additional steps should be necessary. Sator uses these modules:
	* numpy
	* scipy
	* matplotlib
	* mpl_toolkits
	* h5py
	* ctypes
	* struct, sys, os
	* ScrolledText, Tkinter
2. Git clone the repository to your favorite location
3. Set the environment variable DATADIR to point at the folder with the snapshot data. For example, the snapshot files of a simulation named 'mh1w1f1' must be located in $DATADIR/mh1w1f1/, and the files must be named e.g. mh1w1f1_000 in that directory.
4. Start the program with 'python sator.py'. If all goes well you should see the main menu.

Please report any bugs to the Issues site, email me, or simply fix it yourself. Have fun!