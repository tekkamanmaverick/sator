
from include import *
from settings import *
from snap import *
from fields import *
from image import *
from pspace import *
from lines import *
from plots import *
from utils import *

class sator:

    def __init__(self, par_file):

        # Initialize settings

        self.get_settings(par_file)

        if par_file:
            return

        # Initialize flags
        
        self.flag_types_frame = 0
        self.flag_plot_options_frame = 0
        self.flag_plot_sub_options_frame = 0
        self.flag_fig = 0
        self.flag_plot_first = 0

        # Create main window

        self.root = tk.Tk()

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.win_width = int(self.win_fac * self.screen_width)
        self.win_height = int(self.win_fac * self.screen_height)

        self.fig_size = self.win_height / float(self.fig_dpi)

        self.ratio = (self.win_width - self.win_height) / float(self.win_width)

        x = int((self.screen_width - self.win_width) / 2)
        y = int((self.screen_height - self.win_height) / 2)

        self.root.geometry('%dx%d+%d+%d' % (self.win_width, self.win_height, x, y))
        self.root.title("This is SATOR v1.0")

        # Create menu frame

        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.place(relx = 0, rely = 0, relwidth = self.ratio, relheight = 0.5)

        # Create snap frame

        self.snap_frame = tk.Frame(self.menu_frame)
        self.snap_frame.grid(row = 0, column = 0)

        label = tk.Label(self.snap_frame, text = 'Snapshot')
        label.grid(row = 0, column = 1)

        label = tk.Label(self.snap_frame, text = 'Base')
        label.grid(row = 1, column = 0, sticky = 'w')

        self.base_tk = tk.StringVar()
        self.base_tk.set('test')

        entry = tk.Entry(self.snap_frame, textvariable = self.base_tk)
        entry.grid(row = 1, column = 1, sticky = 'w')

        label = tk.Label(self.snap_frame, text = '#')
        label.grid(row = 2, column = 0, sticky = 'w')

        self.snapnum_tk = tk.StringVar()
        self.snapnum_tk.set('1')

        entry = tk.Entry(self.snap_frame, textvariable = self.snapnum_tk)
        entry.grid(row = 2, column = 1, sticky = 'w')

        btn = tk.Button(self.snap_frame, text = 'Open', command = lambda:self.open_snapshot())
        btn.grid(row = 3, column = 1)

        # Create output frame

        self.output_frame = tk.Frame(self.root)
        self.output_frame.place(relx = 0, rely = 0.5, relwidth = self.ratio, relheight = 0.5)

        self.stdout = ScrolledText.ScrolledText(self.output_frame)
        self.stdout.pack()

        redir = redirect(self.stdout)
        sys.stdout = redir

        # Create plot frame

        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.place(relx = self.ratio, rely = 0, relwidth = 1 - self.ratio, relheight = 1)

    def open_snapshot(self):

        # Destroy frames

        self.destroy_frames(1, 1, 1, 0)

        # Get header from snapshot

        self.get_header(self.base_tk.get(), self.snapnum_tk.get(), 0, 1)

        # Check for read error
        
        if self.flag_error == 1:
            self.error_message('Could not open snapshot file!')
        elif self.flag_error == 2:
            self.error_message('Type list is empty!')
        else:
            self.create_types_frame()

    def create_types_frame(self):

        # Destroy frames

        self.destroy_frames(1, 1, 1, 1)

        # Create types frame

        self.types_frame = tk.Frame(self.menu_frame)
        self.types_frame.grid(row = 1, column = 0, sticky = 'nw')

        label = tk.Label(self.types_frame, text = 'Type')
        label.grid(row = 0, column = 0, sticky = 'w')

        self.part_type_tk = tk.StringVar()
        self.part_type_tk.set(self.header.type_list[0])

        menu = tk.OptionMenu(self.types_frame, self.part_type_tk, *self.header.type_list)
        menu.grid(row = 0, column = 1, sticky = 'w')

        # Set types frame flag
        
        self.flag_types_frame = 1

        # Create plot options frame

        self.create_plot_options_frame()
        self.part_type_tk.trace('w', lambda *args: self.create_plot_options_frame())

    def create_plot_options_frame(self):

        # Destroy frames

        self.destroy_frames(0, 1, 1, 1)

        # Determine which snap fields and refined fields are available

        flag = self.init_fields(int(self.part_type_tk.get()))

        # Check for existence of refined fields

        if flag:

            self.error_message('No refined fields exist for this particle type!')

        else:

            # Determine plot options

            plot_options = ['Slice', 'Projection', 'Phase Space', 'Lines']

            # Create plot options frame

            self.plot_options_frame = tk.Frame(self.menu_frame)
            self.plot_options_frame.grid(row = 2, column = 0, sticky = 'nw')

            label = tk.Label(self.plot_options_frame, text = 'Plot')
            label.grid(row = 0, column = 0, sticky = 'w')

            self.plot_option = tk.StringVar(self.plot_options_frame)
            self.plot_option.set(plot_options[0])

            menu = tk.OptionMenu(self.plot_options_frame, self.plot_option, *plot_options)
            menu.grid(row = 0, column = 1, sticky = 'w')

            self.create_plot_sub_options_frame()
            self.plot_option.trace('w', lambda *args: self.create_plot_sub_options_frame())

            self.flag_plot_options_frame = 1

    def create_plot_sub_options_frame(self):

        # Destroy frames

        self.destroy_frames(0, 0, 1, 1)

        # Create sub options frame

        self.plot_sub_options_frame = tk.Frame(self.menu_frame)
        self.plot_sub_options_frame.grid(row = 3, column = 0, sticky = 'nw')

        # Set flag to indicate plot is created for the first time

        self.flag_plot_first = 1

        # Do plot option dependent routines

        plot_option = self.plot_option.get()

        self.plot_sub_options = []

        if plot_option == 'Slice' or plot_option == 'Projection':

            # Determine plottable fields

            self.get_plot_fields()

            # Create left sub options frame

            self.plot_left_sub_options_frame = tk.Frame(self.plot_sub_options_frame)
            self.plot_left_sub_options_frame.grid(row = 0, column = 0, sticky = 'nw')

            # Create menu for fields

            label = tk.Label(self.plot_left_sub_options_frame, text = 'Field')
            label.grid(row = 0, column = 0, sticky = 'w')

            self.plot_sub_options.append(self.plot_fields.keys())
            self.plot_sub_options.append(tk.StringVar())
            self.plot_sub_options[1].set(self.plot_sub_options[0][0])

            menu = tk.OptionMenu(self.plot_left_sub_options_frame, self.plot_sub_options[1], *self.plot_sub_options[0])
            menu.grid(row = 0, column = 1, sticky = 'w')

            # Create buttons for image width

            label = tk.Label(self.plot_left_sub_options_frame, text = 'Width')
            label.grid(row = 1, column = 0, sticky = 'w')

            self.plot_sub_options.append(tk.StringVar())
            self.plot_sub_options[2].set(self.length_units.keys()[0])

            menu = tk.OptionMenu(self.plot_left_sub_options_frame, self.plot_sub_options[2], *self.length_units.keys())
            menu.grid(row = 1, column = 2, sticky = 'w')

            length_unit = self.length_units[self.plot_sub_options[2].get()]
            width = self.header.BoxSize / self.header.HubbleParam * self.header.unit_length / length_unit

            self.plot_sub_options.append(tk.StringVar())
            self.plot_sub_options[3].set(str(width))

            entry = tk.Entry(self.plot_left_sub_options_frame, textvariable = self.plot_sub_options[3], width = self.entry_width)
            entry.grid(row = 1, column = 1, sticky = 'w')

            # Create entry for number of pixels

            label = tk.Label(self.plot_left_sub_options_frame, text = 'Pixels')
            label.grid(row = 2, column = 0, sticky = 'w')

            self.plot_sub_options.append(tk.StringVar())
            self.plot_sub_options[4].set(500)

            entry = tk.Entry(self.plot_left_sub_options_frame, textvariable = self.plot_sub_options[4], width = self.entry_width)
            entry.grid(row = 2, column = 1, sticky = 'w')

            # Create Go button

            btn = tk.Button(self.plot_left_sub_options_frame, text = 'Go', command = lambda:self.do_plot(plot_option, [0, 0, 0]))
            btn.grid(row = 3, column = 1)

            # Create right sub options frame

            self.plot_right_sub_options_frame = tk.Frame(self.plot_sub_options_frame)
            self.plot_right_sub_options_frame.grid(row = 0, column = 1, sticky = 'nw')

            # Create buttons for zooming

            label = tk.Label(self.plot_right_sub_options_frame, text = 'Zoom')
            label.grid(row = 0, column = 0, sticky = 'w')

            btn = tk.Button(self.plot_right_sub_options_frame, text = '+', command = lambda:self.do_plot(plot_option, [1, 0, 0]))
            btn.grid(row = 0, column = 1, sticky = 'w')

            btn = tk.Button(self.plot_right_sub_options_frame, text = '-', command = lambda:self.do_plot(plot_option, [2, 0, 0]))
            btn.grid(row = 0, column = 2, sticky = 'w')

            # Create buttons for movement

            label = tk.Label(self.plot_right_sub_options_frame, text = 'Move')
            label.grid(row = 1, column = 0, sticky = 'w')

            btn = tk.Button(self.plot_right_sub_options_frame, text = 'L', command = lambda:self.do_plot(plot_option, [0, 1, 0]))
            btn.grid(row = 1, column = 1, sticky = 'w')

            btn = tk.Button(self.plot_right_sub_options_frame, text = 'R', command = lambda:self.do_plot(plot_option, [0, 2, 0]))
            btn.grid(row = 1, column = 2, sticky = 'w')

            btn = tk.Button(self.plot_right_sub_options_frame, text = 'U', command = lambda:self.do_plot(plot_option, [0, 3, 0]))
            btn.grid(row = 1, column = 3, sticky = 'w')

            btn = tk.Button(self.plot_right_sub_options_frame, text = 'D', command = lambda:self.do_plot(plot_option, [0, 4, 0]))
            btn.grid(row = 1, column = 4, sticky = 'w')

            # Create buttons for rotation

            label = tk.Label(self.plot_right_sub_options_frame, text = 'Rotate')
            label.grid(row = 2, column = 0, sticky = 'w')

            btn = tk.Button(self.plot_right_sub_options_frame, text = 'L', command = lambda:self.do_plot(plot_option, [0, 0, 1]))
            btn.grid(row = 2, column = 1, sticky = 'w')

            btn = tk.Button(self.plot_right_sub_options_frame, text = 'R', command = lambda:self.do_plot(plot_option, [0, 0, 2]))
            btn.grid(row = 2, column = 2, sticky = 'w')

            btn = tk.Button(self.plot_right_sub_options_frame, text = 'U', command = lambda:self.do_plot(plot_option, [0, 0, 3]))
            btn.grid(row = 2, column = 3, sticky = 'w')

            btn = tk.Button(self.plot_right_sub_options_frame, text = 'D', command = lambda:self.do_plot(plot_option, [0, 0, 4]))
            btn.grid(row = 2, column = 4, sticky = 'w')

        elif plot_option == 'Phase Space':

            # Create menu for fields

            label = tk.Label(self.plot_sub_options_frame, text = 'X Field')
            label.grid(row = 0, column = 0, sticky = 'w')

            self.plot_sub_options.append(self.plot_fields.keys())
            self.plot_sub_options.append(tk.StringVar())
            self.plot_sub_options[1].set(self.plot_sub_options[0][0])

            menu = tk.OptionMenu(self.plot_sub_options_frame, self.plot_sub_options[1], *self.plot_sub_options[0])
            menu.grid(row = 0, column = 1, sticky = 'w')

            label = tk.Label(self.plot_sub_options_frame, text = 'Y Field')
            label.grid(row = 1, column = 0, sticky = 'w')

            self.plot_sub_options.append(self.plot_fields.keys())
            self.plot_sub_options.append(tk.StringVar())
            self.plot_sub_options[3].set(self.plot_sub_options[2][0])

            menu = tk.OptionMenu(self.plot_sub_options_frame, self.plot_sub_options[3], *self.plot_sub_options[2])
            menu.grid(row = 1, column = 1, sticky = 'w')

            # Create entry for number of pixels

            label = tk.Label(self.plot_sub_options_frame, text = 'Pixels')
            label.grid(row = 2, column = 0, sticky = 'w')

            self.plot_sub_options.append(tk.StringVar())
            self.plot_sub_options[4].set(500)

            entry = tk.Entry(self.plot_sub_options_frame, textvariable = self.plot_sub_options[4], width = self.entry_width)
            entry.grid(row = 2, column = 1, sticky = 'w')
            
            # Create Go button

            btn = tk.Button(self.plot_sub_options_frame, text = 'Go', command = lambda:self.do_plot(plot_option, 0))
            btn.grid(row = 3, column = 1)

        elif plot_option == 'Lines':

            # Create menu for fields

            label = tk.Label(self.plot_sub_options_frame, text = 'X Field')
            label.grid(row = 0, column = 0, sticky = 'w')

            self.plot_sub_options.append(self.plot_fields.keys())
            self.plot_sub_options.append(tk.StringVar())
            self.plot_sub_options[1].set(self.plot_sub_options[0][0])

            menu = tk.OptionMenu(self.plot_sub_options_frame, self.plot_sub_options[1], *self.plot_sub_options[0])
            menu.grid(row = 0, column = 1, sticky = 'w')

            label = tk.Label(self.plot_sub_options_frame, text = 'Y Field')
            label.grid(row = 1, column = 0, sticky = 'w')

            self.plot_sub_options.append(self.plot_fields.keys())
            self.plot_sub_options.append(tk.StringVar())
            self.plot_sub_options[3].set(self.plot_sub_options[2][0])

            menu = tk.OptionMenu(self.plot_sub_options_frame, self.plot_sub_options[3], *self.plot_sub_options[2])
            menu.grid(row = 1, column = 1, sticky = 'w')

            # Create entry for number of pixels

            label = tk.Label(self.plot_sub_options_frame, text = 'Pixels')
            label.grid(row = 2, column = 0, sticky = 'w')

            self.plot_sub_options.append(tk.StringVar())
            self.plot_sub_options[4].set(500)

            entry = tk.Entry(self.plot_sub_options_frame, textvariable = self.plot_sub_options[4], width = self.entry_width)
            entry.grid(row = 2, column = 1, sticky = 'w')
            
            # Create Go button

            btn = tk.Button(self.plot_sub_options_frame, text = 'Go', command = lambda:self.do_plot(plot_option, 0))
            btn.grid(row = 3, column = 1)

        # Set sub options frame flag

        self.flag_plot_sub_options_frame = 1

    def do_plot(self, plot_option, args):

        # Destroy frames

        self.destroy_frames(0, 0, 0, 1)

        # Initialize figure

        self.fig = mp.figure.Figure(figsize = (self.fig_size, self.fig_size))
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.plot_frame)
        self.canvas.get_tk_widget().grid()

        # Do plot option dependent routines

        if plot_option == 'Slice' or plot_option == 'Projection':

            opts = self.plot_sub_options

            refined_field = self.plot_sub_options[1].get()
            width = float(self.plot_sub_options[3].get())
            length_unit = self.plot_sub_options[2].get()
            npixels = int(self.plot_sub_options[4].get())

            width = self.get_image(plot_option, refined_field, width, length_unit, npixels, args)

            self.plot_sub_options[3].set(str(width))

        elif plot_option == 'Phase Space':

            xfield = self.plot_sub_options[1].get()
            yfield = self.plot_sub_options[3].get()
            npixels = int(self.plot_sub_options[4].get())

            vals, bds = self.get_pspace(xfield, yfield, npixels)

            self.plot_pspace(self.fig, vals, bds, xfield, yfield)
            
        elif plot_option == 'Lines':

            xfield = self.plot_sub_options[1].get()
            yfield = self.plot_sub_options[3].get()
            npixels = int(self.plot_sub_options[4].get())

            x, y = self.get_lines(self.fig, xfield, yfield, npixels)

            self.plot_lines(x, y, xfield, yfield)

        # Refresh and save figure

        self.canvas.draw_idle()
        self.fig.savefig('out.pdf')
        self.flag_fig = 1

    # Function for destroying frames

    def destroy_frames(self, flag1, flag2, flag3, flag4):

        if flag1:
            if self.flag_types_frame:
                self.types_frame.destroy()
                self.flag_types_frame = 0
        if flag2:
            if self.flag_plot_options_frame:
                self.plot_options_frame.destroy()
                self.flag_plot_options_frame = 0
        if flag3:
            if self.flag_plot_sub_options_frame:
                self.plot_sub_options_frame.destroy()
                self.flag_plot_sub_options_frame = 0
        if flag4:
            if self.flag_fig:
                self.fig.clf()
                self.canvas.get_tk_widget().destroy()
                self.flag_fig = 0

    # Pop-up for error messages

    def error_message(self, text):

        error = tk.Toplevel()
        error.title('Error')

        win_fac = 0.15

        win_width = int(win_fac * self.screen_width)
        win_height = int(win_fac * self.screen_height)

        x = int((self.screen_width - win_width) / 2)
        y = int((self.screen_height - win_height) / 2)

        error.geometry('%dx%d+%d+%d' % (win_width, win_height, x, y))

        msg = tk.Message(error, text = text, width = 0.95 * win_width)
        msg.pack()

# Redirect stdout to output frame

class redirect(object):

    def __init__(self, text_ctrl):
        self.output = text_ctrl

    def write(self, string):
        self.output.insert(tk.END, string)
        
# Import functions from other files

# From settings.py

sator.get_settings = get_settings

# From snap.py

sator.get_header = get_header
sator.get_snap_field = get_snap_field
sator.snap_field_error = snap_field_error

# From fields.py

sator.init_fields = init_fields
sator.get_plot_fields = get_plot_fields
sator.get_refined_field = get_refined_field

# From image.py

sator.get_image = get_image

# From pspace.py

sator.get_pspace = get_pspace

# From lines.py

sator.get_lines = get_lines

# From plots.py

sator.plot_pspace = plot_pspace
sator.plot_lines = plot_lines

# From utils.py

sator.get_center = get_center
sator.center_and_rotate = center_and_rotate
sator.init_figure = init_figure
sator.finish_figure = finish_figure
