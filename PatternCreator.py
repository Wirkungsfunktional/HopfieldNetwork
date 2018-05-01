import numpy as np
from matplotlib import pyplot as plt


class PatternCreator:
    def __init__(self, size):
        self.size = size
        self.patterns = []
        self.number_of_pattern = 0



        self._fig = plt.figure()        # erstellt Fenster
        self._ax = plt.subplot()        # erstellt Plot
        self._fig.canvas.mpl_connect('button_press_event', self.onPress)

        self.new_pattern = np.ones( (self.size, self.size) )
        self.img = plt.imshow(self.new_pattern)
        plt.show()

    def add_pattern(self, pattern):
        assert (len(pattern[:,0]) == self.size) and len(pattern[0]) == self.size, "Pattern has to be a (n x n) matrix with n = size."
        self.patterns.append(pattern)
        self.number_of_pattern += 1

    def get_trainings_set(self):
        ret = np.zeros( (self.number_of_pattern, self.size**2) )
        for i in range(self.number_of_pattern):
            ret[i] = self.patterns[i].flatten()
        return ret

    def onPress(self, event):
        """Festlegung der Startwerte und Berechung"""
        mode = plt.get_current_fig_manager().toolbar.mode
        # Button: 1 == rechts, mode: Normal oder zoom, pan, etc.
        if event.button == 1 and event.inaxes and mode == '': # Fehler abfangen
            self.update(int(event.xdata+0.5),int(event.ydata+0.5))

    def update(self, i, j):
        self.new_pattern[j][i] = -1
        self.img.set_data(self.new_pattern)
        self.img.autoscale()
        print(self.new_pattern)
        self._fig.canvas.draw()




p = PatternCreator(15)
