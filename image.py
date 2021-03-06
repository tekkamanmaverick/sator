
from include import *
from utils import *

def get_image(self, plot_option, refined_field, width, length_unit, npixels, args):

    # Extract parameters

    if args:
        zoom = args[0]
        move = args[1]
        rotate = args[2]
    else:
        zoom = 0
        move = 0
        rotate = 0

    # Initialize some additional variables

    center_mode = 0
    npoints = npixels**2

    if refined_field == 'gamma':
        log_plot = 0
    else:
        log_plot = 1

    # Get particle positions

    flag, pos = self.get_refined_field('pos')

    if flag:
        return

    flag, vel = self.get_refined_field('vel')

    if flag:
        return

    flag, mass = self.get_refined_field('mass')

    if flag:
        return

    pos, vel = self.center_and_rotate(pos, vel, mass)

    # Do this the first time the plot is created

    if self.flag_plot_first:

        # Center box

        flag, nh = self.get_refined_field('nh')

        if flag:
            return

        flag = self.get_center(0)

        if flag:
            return

        self.norm_center = np.zeros(3)

        # Get normalized positions

        self.norm_pos = np.zeros([int(pos.size / 3), 3])

        for i in np.arange(3):
            self.norm_pos[:, i] = (pos[:, i] - self.center[i]) / self.header.boxsize_cgs

        # Create tree

        if plot_option == 'Slice':
            self.tree = spatial.cKDTree(self.norm_pos)

        # Initialize rotation angles

        self.rot_alpha = 0.
        self.rot_beta = 0.

        # It is no longer the first time the plot is created

        self.flag_plot_first = 0

    # Do zoom

    if zoom:

        if zoom == 1:
            width *= self.zoom_fac
        elif zoom == 2:
            width /= self.zoom_fac

    # Determine normalized width

    norm_width = width * self.length_units[length_unit] / self.header.boxsize_cgs

    # Do move

    if move:

        delta = self.move_fac * norm_width

        if move == 1:
            self.norm_center[0] -= delta
        elif move == 2:
            self.norm_center[0] += delta
        elif move == 3:
            self.norm_center[1] -= delta
        elif move == 4:
            self.norm_center[1] += delta

    # Get rotation angles

    if rotate:

        if rotate == 1:
            self.rot_beta += self.rot_delta
        elif rotate == 2:
            self.rot_beta -= self.rot_delta
        elif rotate == 3:
            self.rot_alpha += self.rot_delta
        elif rotate == 4:
            self.rot_alpha -= self.rot_delta

    # Do plot

    if plot_option == 'Slice':

        # Determine list of evenly spaced points

        x1 = -norm_width / 2. + self.norm_center[0]
        x2 = norm_width / 2. + self.norm_center[0]

        y1 = -norm_width / 2. + self.norm_center[1]
        y2 = norm_width / 2. + self.norm_center[1]

        px = np.linspace(x1, x2, npixels)
        py = np.linspace(y1, y2, npixels)

        xv, yv = np.meshgrid(px, py, indexing='ij')

        xv = xv.ravel()
        yv = yv.ravel()

        points = np.empty([npoints, 3])

        points[:, 0] = xv
        points[:, 1] = yv
        points[:, 2] = 0.

        # Do rotation

        points = do_rotation(points, self.rot_alpha, self.rot_beta, self.norm_center)

        # Walk tree

        dist, idx = self.tree.query(points)

        # Select nearest neigbours in target field

        flag, vals = self.get_refined_field(refined_field)

        if flag:
            return

        vals = vals[idx]

        if log_plot:
            vals = np.log10(vals)

    elif plot_option == 'Projection':

        # Get index list for particles within r = 2 * sub box (due to rotation)

        rel_pos = np.zeros([int(self.norm_pos.size / 3), 3])

        for i in np.arange(3):
            rel_pos[:, i] = (self.norm_pos[:, i] - self.norm_center[i]) / norm_width

        idx_list = []
        
        for i in np.arange(3):
            idx_list.append(np.abs(rel_pos[:, i]) < 1.)

        idx = np.logical_and(idx_list[0], idx_list[1])
        idx = np.logical_and(idx, idx_list[2])

        # Get positions of sub box

        sub_pos = np.zeros([rel_pos[idx, 0].size, 3])

        for i in np.arange(3):
            sub_pos[:, i] = rel_pos[idx, i]

        # Do rotation

        rot_pos = do_rotation(sub_pos, self.rot_alpha, self.rot_beta, np.zeros(3))
            
        # Get fields required for projection

        x = np.array(rot_pos[:, 0])
        y = np.array(rot_pos[:, 1])

        mass = mass[idx]

        flag, rho = self.get_refined_field('rho')

        if flag:
            return

        rho = rho[idx]

        flag, ref = self.get_refined_field(refined_field)

        if flag:
            return
        
        ref = ref[idx]

        if log_plot:
            ref = np.log10(ref)

        hsml = (3. / 4. / np.pi * mass / rho)**( 1. / 3.)
        hsml /= (self.header.boxsize_cgs * norm_width)

        # Initialize result arrays

        vals = np.zeros(npoints, dtype = np.dtype('float64'))
        sums = np.zeros(npoints, dtype = np.dtype('float64'))

        # Load projection library

        arr = npct.ndpointer(dtype = np.dtype('float64'), ndim = 1, flags = 'CONTIGUOUS')
        lib = npct.load_library("projection", ".")
        lib.restype = None
        lib.projection.argtypes = [arr, arr, arr, arr, arr, c_int, arr, arr, c_int]

        # Do projection

        lib.projection(x, y, rho, hsml, ref, x.size, vals, sums, npixels)

        # Get valid values

        idx = sums > 0.
        vals[idx] /= sums[idx]
        idx = sums == 0.
        vals[idx] = np.nan

    # Reshape

    vals = np.reshape(vals, (npixels, npixels))
    vals = np.swapaxes(vals, 0, 1)

    # Draw image

    bottom = 0.05
    top = 0.05
    frac_cbar = 0.03

    frac = 1. - bottom - top - frac_cbar
    left = (1. - frac) / 2.

    cmap = get_color_map(refined_field)

    ax = self.fig.add_axes([left, bottom, frac, frac])

    ax.set_xticks([])
    ax.set_yticks([])

    im = ax.imshow(vals, cmap = cmap)

    # Add labels

    offset_x = 0.01
    offset_y = 0.05

    self.fig.text(left + frac + offset_x, bottom + frac + offset_y, get_label(refined_field), rotation = 270)

    offset = 0.02

    text = 'Width: ' + str(width) + ' ' + length_unit

    self.fig.text(0.5, offset, text, horizontalalignment = 'center')

    # Add color bar
    
    cax = self.fig.add_axes([left, bottom + frac, frac, frac_cbar])

    self.fig.colorbar(im, cax = cax, orientation = 'horizontal')

    cax.xaxis.set_ticks_position('top')
    cax.yaxis.set_label_position('right')

    # Return width (used for zooming)

    return width
