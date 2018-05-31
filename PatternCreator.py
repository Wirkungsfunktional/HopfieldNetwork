import numpy as np
from matplotlib import pyplot as plt
import MenuBar
import Observer
import GraphicAlgorithms as GA
import HopfieldModell as HM
import Pattern



__doc__ = """Using a matplotlib imshow plot of an quadratic matrix of ones. By
clicking on particular cells, one can change the respective state of the cell to
its negative. Hence one can create a pattern. The Key activities are:
    n: add a pattern to a set and start an empty plot.
    b: save the set to a file.


    """
class PatternCreator:
    def __init__(self, size):
        self.size = size
        self.patterns = []
        self.number_of_pattern = 0
        self.hopfield = HM.HopfieldModell(self.size)
        self.iteration_number = 1000
        self.steps = range(self.iteration_number)
        self.energy_function = [0]*self.iteration_number
        self.new_pattern = Pattern.Pattern(self.size)


        self._fig = plt.figure()
        self._fig.subplots_adjust(left=0.5)
        self._ax  = plt.subplot(111)


        observer = Observer.Observer()
        observer.add_action('add', self.action_add)
        observer.add_action('save', self.action_save)
        observer.add_action('quit', self.action_quit)
        observer.add_action('Pen Tool', self.action_draw_delete)
        observer.add_action('Fill Tool', self.action_fill)
        observer.add_action('Line Tool', self.action_line)
        observer.add_action('Rectangle Tool', self.action_rectangle)
        observer.add_action('Circle Tool', self.action_circle)
        observer.add_action('Random Pattern', self.add_random_pattern)
        observer.add_action('Load Pattern', self.action_load)
        observer.add_action('Train', self.action_training)
        observer.add_action('Run', self.action_pattern_run)



        menu = MenuBar.make_menu(self._fig, observer)
        self._fig.canvas.mpl_connect('button_press_event', self.on_click)
        self._fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self._fig.canvas.mpl_connect('button_release_event', self.on_release)

        self.plot1 = GA.Canvas( self._fig,
                                self._ax.imshow(self.new_pattern.get_quadratic_rep()),
                                self.new_pattern)

        self.line_draw_tool = GA.LineDrawTool(self.plot1)
        self.fill_draw_tool = GA.FillDrawTool(self.plot1)
        self.pen_draw_tool = GA.PenDrawTool(self.plot1)
        self.rect_draw_tool = GA.RectangleDrawTool(self.plot1)
        self.circ_draw_tool = GA.CircleDrawTool(self.plot1)
        self.draw_tool = self.pen_draw_tool

        plt.show()

    def action_circle(self):
        self.draw_tool = self.circ_draw_tool

    def action_load(self):
        self.new_pattern = self.patterns[0]
        self.plot1.set_data(self.new_pattern)
        self.plot1.update()

    def action_rectangle(self):
        self.draw_tool = self.rect_draw_tool

    def action_add(self):
        """Add the pattern to the list."""
        self.add_pattern(self.new_pattern)
        self.new_pattern = Pattern.Pattern(self.size)
        self.plot1.set_data(self.new_pattern)
        self.plot1.update()

    def action_save(self):
        """Save the pattern to a file of type .npy"""
        self.save_pattern()

    def action_quit(self):
        """Close the Program."""
        exit()

    def action_draw_delete(self):
        """Change the option from draw to pen_draw_tool."""
        self.draw_tool = self.pen_draw_tool

    def action_random_pattern(self):
        """Creates a random pattern."""
        self.add_random_pattern()

    def action_fill(self):
        """Activate the option to fill the pixel of a bounded region after
        clicking into this region."""
        self.draw_tool = self.fill_draw_tool

    def action_line(self):
        """Activate the option to draw a line"""
        self.draw_tool = self.line_draw_tool

    def action_training(self):
        """Use the set of pattern to train the Hopfield model and plot the
        weights und storage_capacity into to additional plots."""
        self.hopfield.training(self.get_trainings_set())

    def action_pattern_run(self):
        """Perform the storage retrival on the pattern and plot the Energy of
        this operation."""
        p = Pattern.Pattern(0)
        p.set_pattern_from_matrix(
            self.hopfield.run(  self.new_pattern.get_quadratic_rep(),
                                self.iteration_number) )
        self.new_pattern = p
        self.plot1.set_data(self.new_pattern)
        self.plot1.update()


    def add_pattern(self, pattern):
        """Add a pattern to the list and increase the number of patterns"""
        #assert (len(pattern[:,0]) == self.size) and len(pattern[0]) == \
        #    self.size, "Pattern has to be a (n x n) matrix with n = size."
        self.patterns.append(pattern)
        print("Added pattern.")
        self.number_of_pattern += 1
        #HM.HopfieldModell.get_storage_capacity(self.get_trainings_set())


    def add_random_pattern(self):
        """Create an uniform random pattern and add it to the patterns list."""
        self.new_pattern = Pattern.Pattern.make_random_pattern(self.size)
        self.plot1.set_data(self.new_pattern)
        self.plot1.update()

    def get_trainings_set(self):
        """Cast the list to an numpy array and returns it in shape
        (number_of_pattern, size_of_pattern) where size_of_pattern is the to
        one dimmension flattened vector of the quadratic matrix of the pattern."""
        ret = np.zeros( (self.number_of_pattern, self.size**2) )
        for i in range(self.number_of_pattern):
            ret[i] = self.patterns[i].get_column_rep().copy()
        return ret

    def on_click(self, event):
        """For _fill_option active the function fixes the starting point for the
        line. For the _fill_option, it fill the closed curve. For non activated
        options it draw the pixel."""
        mode = plt.get_current_fig_manager().toolbar.mode
        if event.button == 1 and event.inaxes and mode == '':
            self.draw_tool.on_click(event)

    def on_motion(self, event):
        if event.inaxes != self._ax: return
        self.draw_tool.on_motion(event)

    def on_release(self, event):
        mode = plt.get_current_fig_manager().toolbar.mode
        if event.button == 1 and event.inaxes and mode == '':
            self.draw_tool.on_release(event)


    def save_pattern(self):
        np.save("test", self.get_trainings_set())
        print("Saved Pattern.")



print(__doc__)
p = PatternCreator(100)
