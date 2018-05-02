import numpy as np
from matplotlib import pyplot as plt
import MenuBar



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



        self._fig = plt.figure()
        self._fig.subplots_adjust(left=0.3)
        self._ax = plt.subplot()

        labels = ('add', 'save', 'quit')
        menu = MenuBar.make_menu(self._fig, labels, self.on_select)
        self._fig.canvas.mpl_connect('button_press_event', self.onPress)
        self.new_pattern = np.ones( (self.size, self.size) )
        self._img = plt.imshow(self.new_pattern)
        plt.show()




    def on_select(self, item):
        if item.labelstr == "quit":
            exit()
        if item.labelstr == "save":
            self.save_pattern()
        if item.labelstr == "add":
            self.add_pattern(self.new_pattern.copy())
            self.new_pattern = np.ones( (self.size, self.size) )
            self.update_plot()


    def add_pattern(self, pattern):
        """Add a pattern to the list and increase the number of patterns"""
        assert (len(pattern[:,0]) == self.size) and len(pattern[0]) == self.size, "Pattern has to be a (n x n) matrix with n = size."
        self.patterns.append(pattern)
        print("Add pattern.")
        self.number_of_pattern += 1

    def get_trainings_set(self):
        """Cast the list to an numpy array and returns it in shape
        (number_of_pattern, size_of_pattern) where size_of_pattern is the to
        one dimmension flattened vector of the quadratic matrix of the pattern."""
        ret = np.zeros( (self.number_of_pattern, self.size**2) )
        for i in range(self.number_of_pattern):
            ret[i] = self.patterns[i].flatten()
        return ret

    def onPress(self, event):
        mode = plt.get_current_fig_manager().toolbar.mode
        if event.button == 1 and event.inaxes and mode == '':
            self.update(int(event.xdata+0.5),int(event.ydata+0.5))

    def update(self, i, j):
        """Change the sign of the cell (i,j) and update the plot."""
        self.new_pattern[j][i] *= -1
        self.update_plot()

    def update_plot(self):
        self._img.set_data(self.new_pattern)
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
p = PatternCreator(15)
