
from include import *

def get_center(pos, nh, center_mode):

    center = np.zeros(3)

    if center_mode == 0:

        idx = np.argmax(nh)

        for i in np.arange(3):
            center[i] = pos[idx, i]

    return center
            
def do_rotation(pos, alpha, beta, center):

    # Temporarily center positions

    for i in np.arange(3):
        pos[:, i] -= center[i]

    # First rotation matrix (up and down)

    rot_alpha = np.zeros([3, 3])

    rot_alpha[0, 0] = 1.;
    rot_alpha[1, 1] = np.cos(alpha);
    rot_alpha[1, 2] = np.sin(alpha);
    rot_alpha[2, 1] = -np.sin(alpha);
    rot_alpha[2, 2] = np.cos(alpha);

    # Second rotation matrix (left and right)
    
    rot_beta = np.zeros([3, 3])

    rot_beta[0, 0] = np.cos(beta);
    rot_beta[0, 2] = -np.sin(beta);
    rot_beta[1, 1] = 1.;
    rot_beta[2, 0] = np.sin(beta);
    rot_beta[2, 2] = np.cos(beta);

    # Concatenate both rotations

    rot = np.dot(rot_beta, rot_alpha)

    # Rotate positions

    rot_pos = np.zeros([pos.size / 3, 3])

    rot_pos[:, 0] = rot[0, 0] * pos[:, 0]
    rot_pos[:, 0] += rot[0, 1] * pos[:, 1]
    rot_pos[:, 0] += rot[0, 2] * pos[:, 2]
        
    rot_pos[:, 1] = rot[1, 0] * pos[:, 0]
    rot_pos[:, 1] += rot[1, 1] * pos[:, 1]
    rot_pos[:, 1] += rot[1, 2] * pos[:, 2]

    rot_pos[:, 2] = rot[2, 0] * pos[:, 0]
    rot_pos[:, 2] += rot[2, 1] * pos[:, 1]
    rot_pos[:, 2] += rot[2, 2] * pos[:, 2]

    # Move positions back again

    for i in np.arange(3):
        rot_pos[:, i] += center[i]

    return rot_pos

def get_label(field):

    if field == 'mass':
        label = r'${\rm log}\,M\,[{\rm g}]$'
    elif field == 'rho':
        label = r'${\rm log}\,\rho\,[{\rm g}\,{\rm cm}^{-3}]$'
    elif field == 'nh':
        label = r'${\rm log}\,n_{\rm H}\,[{\rm cm}^{-3}]$'
    elif field == 'temp':
        label = r'${\rm log}\,T\,[{\rm K}]$'
    elif field == 'vol':
        label = r'${\rm log}\,{\rm Volume}\,[{\rm cm}^3]$'
    elif field == 'gravacc':
        label = r'$a_{\rm grav}$'
    elif field == 'gradp':
        label = r'$\nabla P$'
    elif field == 'abhm':
        label = r'${\rm log}\,{\rm y}_{{\rm H}^-}$'
    elif field == 'abh2':
        label = r'${\rm log}\,{\rm y}_{{\rm H}_2}$'
    elif field == 'abhii':
        label = r'${\rm log}\,{\rm y}_{\rm HII}$'
    elif field == 'gamma':
        label = r'${\rm Adiabatic}\,{\rm index}$'
    elif field == 'allowref':
        label = r'${\rm AllowRef}$'
    elif field == 'divvel':
        label = r'$\nabla V$'
    else:
        label = ''

    return label
            
def get_color_map(field):

    if field == 'temp':
        cmap =  mp.cm.gist_heat
    elif field == 'abhm':
        cmap = mp.cm.gist_stern
    elif field == 'abh2':
        cmap =  mp.cm.gist_stern
    elif field == 'abhii':
        cmap = mp.cm.gist_stern
    else:
        cmap = mp.cm.jet

    return cmap
            
def endrun(msg):

    print msg

    sys.exit()
