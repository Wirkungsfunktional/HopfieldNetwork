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
        self.hopfield.set_run_mode("stochastic")
        self.iteration_number = 1000
        self.steps = range(self.iteration_number)
        self.energy_function = [0]*self.iteration_number
        self.new_pattern = Pattern.Pattern(self.size)



        self._fig = plt.figure()
        self._fig.subplots_adjust(left=0.5)
        self._ax  = plt.subplot(221)
        self._ax2 = plt.subplot(222)
        self._ax3 = plt.subplot(223)
        self._ax4 = plt.subplot(224)
        self.is_clicked = False
        self.set_element = -1 # -1 draw and 1 delete cell
        self._fill_option = 0
        self._line_option = 0
        self._start_point = None
        self._end_point = None



        observer = Observer.Observer()
        observer.add_action('add', self.action_add)
        observer.add_action('save', self.action_save)
        observer.add_action('quit', self.action_quit)
        observer.add_action('draw/delete', self.action_draw_delete)
        observer.add_action('random pattern', self.add_random_pattern)
        observer.add_action('fill', self.action_fill)
        observer.add_action('line', self.action_line)
        observer.add_action('train', self.action_training)
        observer.add_action('run', self.action_pattern_run)



        menu = MenuBar.make_menu(self._fig, observer)
        self._fig.canvas.mpl_connect('button_press_event', self.on_click)
        self._fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self._fig.canvas.mpl_connect('button_release_event', self.on_release)

        self._img   = self._ax.imshow(self.new_pattern.get_quadratic_rep())
        self._img2  = self._ax2.imshow(self.hopfield.weights)
        self._img3  = self._ax3.imshow(self.hopfield.storage_capacity)
        self._img4, = self._ax4.plot(self.steps, self.energy_function)

        plt.show()


    def action_add(self):
        """Add the pattern to the list."""
        self.add_pattern(self.new_pattern)
        self.new_pattern = Pattern.Pattern(self.size)
        self.update_plot()

    def action_save(self):
        """Save the pattern to a file of type .npy"""
        self.save_pattern()

    def action_quit(self):
        """Close the Program."""
        exit()

    def action_draw_delete(self):
        """Change the option from draw to erase pixel and backwards after new
        click."""
        self.set_element *= -1

    def action_random_pattern(self):
        """Add a ramdom generated Pattern to the pattern list."""
        self.add_random_pattern()

    def action_fill(self):
        """Achtivate the option to fill the pixel of a bounded region after
        clicking into this region."""
        self._fill_option ^= 1
        print(self._fill_option)

    def action_line(self):
        """Activate the option to draw a line"""
        self._line_option ^= 1

    def action_training(self):
        """Use the set of pattern to train the Hopfield model and plot the
        weights und storage_capacity into to additional plots."""
        self.hopfield.training(self.get_trainings_set())
        self._img2.set_data(self.hopfield.weights)
        self._img3.set_data(self.hopfield.storage_capacity)
        self._img2.autoscale()
        self._img3.autoscale()
        self._fig.canvas.draw()

    def action_pattern_run(self):
        """Perform the storage retrival on the pattern and plot the Energy of
        this operation."""
        p = Pattern.Pattern(0)
        p.set_pattern_from_matrix(
            self.hopfield.run(  self.new_pattern.get_quadratic_rep(),
                                self.iteration_number) )
        self._img4.set_ydata(self.hopfield.H)
        self._ax4.relim()
        self._ax4.autoscale_view()
        self.new_pattern = p
        self.update_plot()


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
        self.add_pattern(self.new_pattern)

    def get_trainings_set(self):
        """Cast the list to an numpy array and returns it in shape
        (number_of_pattern, size_of_pattern) where size_of_pattern is the to
        one dimmension flattened vector of the quadratic matrix of the pattern."""
        ret = np.zeros( (self.number_of_pattern, self.size**2) )
        for i in range(self.number_of_pattern):
            ret[i] = self.patterns[i].get_column_rep()
        return ret

    def on_click(self, event):
        """For _fill_option active the function fixes the starting point for the
        line. For the _fill_option, it fill the closed curve. For non activated
        options it draw the pixel."""
        mode = plt.get_current_fig_manager().toolbar.mode
        if event.button == 1 and event.inaxes and mode == '':

            if self._fill_option == 1:
                GA.flood_fill(  self.new_pattern.get_quadratic_rep(),
                                int(event.xdata+0.5),
                                int(event.ydata+0.5))
                self.update_plot()
            elif self._line_option == 1:
                self._start_point = (int(event.xdata+0.5),int(event.ydata+0.5))
            else:
                self.is_clicked = True
                self.update(int(event.xdata+0.5),int(event.ydata+0.5))

    def on_motion(self, event):
        if event.inaxes != self._ax: return
        if self.is_clicked:
            self.update(int(event.xdata+0.5),int(event.ydata+0.5))

    def on_release(self, event):
        self.is_clicked = False
        if self._line_option == 1:
            self._end_point = (int(event.xdata+0.5),int(event.ydata+0.5))
            GA.line_draw(   self.new_pattern.get_quadratic_rep(),
                            self._start_point[0],
                            self._start_point[1],
                            self._end_point[0],
                            self._end_point[1])
            self.update_plot()

    def update(self, i, j):
        """Change the sign of the cell (i,j) and update the plot."""
        self.new_pattern.set_point(j, i, self.set_element)
        self.update_plot()

    def update_plot(self):
        self._img.set_data(self.new_pattern.get_quadratic_rep())
        self._img.autoscale()
        self._fig.canvas.draw()


    def save_pattern(self):
        np.save("test", self.get_trainings_set())
        print("Saved Pattern.")


    def decode_to_orthogonal_code(self):
        """TODO: Find some way to convert a set of pattern such that the
        Correlation \sum x_j^n x_j^m = 0 for m != n is at most satisfied.
        Therefore the patterns are orthogonal and the capacity of the neural
        network should increase."""
        pass

print(__doc__)
p = PatternCreator(20)
