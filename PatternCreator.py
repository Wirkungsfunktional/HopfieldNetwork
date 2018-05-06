import numpy as np
from matplotlib import pyplot as plt
import MenuBar
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
        self._fill_option = 0
        self._line_option = 0
        self._start_point = None
        self._end_point = None




        self._fig = plt.figure()
        self._fig.subplots_adjust(left=0.5)
        self._ax = plt.subplot()
        self.is_clicked = False
        self.set_element = -1 # -1 draw and 1 delete cell

        self.labels = ('add', 'save', 'quit', 'draw/delete', 'random pattern', 'fill', 'line')
        menu = MenuBar.make_menu(self._fig, self.labels, self.on_select)
        self._fig.canvas.mpl_connect('button_press_event', self.on_click)
        self._fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self._fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.new_pattern = Pattern.Pattern(self.size)

        self._img = plt.imshow(self.new_pattern.get_quadratic_rep())
        plt.show()




    def on_select(self, item):
        # Add a pattern to the patterns - list
        if item.labelstr == self.labels[0]:
            self.add_pattern(self.new_pattern)
            self.new_pattern = Pattern.Pattern(self.size)
            self.update_plot()
        # Save the patterns - list to a file
        if item.labelstr == self.labels[1]:
            self.save_pattern()
        # Exit the Program
        if item.labelstr == self.labels[2]:
            exit()
        # Change Draw to delete option
        if item.labelstr == self.labels[3]:
            self.set_element *= -1
        # Create a random pattern and add it to the patterns list
        if item.labelstr == self.labels[4]:
            self.add_random_pattern()
        # Activate the fill option of closed curves
        if item.labelstr == self.labels[5]:
            self._fill_option ^= 1
            print(self._fill_option)
        # Activate the line option to draw a straight line
        if item.labelstr == self.labels[6]:
            self._line_option ^= 1


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
        self.new_pattern.make_random_pattern()
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
