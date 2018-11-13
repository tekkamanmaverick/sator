
from sator import *

sator = sator('par.txt')

sator.init_figure(8.)

ax = sator.fig.add_subplot(111)

npart = np.log10([64**3, 128**3, 256**3, 512**3])
runtime_data = np.log10([1e-3, 8.4e-3, 0.07, 0.88])
runtime_slice = np.log10([0.56, 3., 38., 763.])
runtime_proj = np.log10([0.17, 0.78, 6.3, 80.])
runtime_pspace = np.log10([0.16, 0.31, 2.1, 16.])

ax.plot(npart, runtime_data, label = 'Read')
ax.plot(npart, runtime_slice, label = 'Slice')
ax.plot(npart, runtime_proj, label = 'Projection')
ax.plot(npart, runtime_pspace, label = 'Phase space')

ax.tick_params(labelsize = 20)

ax.set_xlabel(r'${\rm log}\,N$', fontsize = 20)
ax.set_ylabel(r'${\rm log}\,t\,[{\rm s}]$', fontsize = 20)

ax.legend(fontsize = 20)

sator.finish_figure()
