
import numpy as np
import numpy.ctypeslib as npct
import matplotlib as mp
from matplotlib.backends.backend_tkagg import FigureCanvasAgg, FigureCanvasTkAgg
from mpl_toolkits.axes_grid1 import AxesGrid
import os
import h5py
import struct
import sys
import ScrolledText
import Tkinter as tk
from ctypes import c_int, c_double
from scipy import spatial
from scipy.spatial import cKDTree

pi = 3.1415927
gamma_adb = 5. / 3.
hydrogen_massfrac = 0.76
abhe = (1. / hydrogen_massfrac - 1.) / 4.
abde = 2.6e-5
mu_prim = 4. / (1. + 3. * hydrogen_massfrac)
protonmass = 1.67262178e-24
boltzmann = 1.38065e-16
electron_volt = 1.60219e-12
gravity = 6.672e-8
solar_mass = 1.989e33
hubble = 3.2407789e-18
sec_per_year = 3.155e7
pc_in_cm = 3.085678e18
kpc_in_cm = 1e3 * pc_in_cm
mpc_in_cm = 1e3 * kpc_in_cm
au_in_cm = 1.49598e13
rsun_in_cm = 6.955e10

NPARTTYPES = 6

class header:

    def __init__(self):

        header = 0

data_dir = os.environ['DATADIR']
