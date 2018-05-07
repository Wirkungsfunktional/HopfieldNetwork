import numpy as np



class Pattern():
    def __init__(self, size):
        self.size = size
        self.pattern = np.ones( (self.size, self.size) )

    def get_quadratic_rep(self):
        return self.pattern

    def get_column_rep(self):
        return self.pattern.flatten()

    def make_random_pattern(self):
        self.pattern = np.ones( (self.size, self.size) ) - \
                2*np.random.randint(2, size = (self.size, self.size))

    def set_point(self, i, j, value):
        self.pattern[i][j] = value

    def set_pattern_from_matrix(self, a):
        shape = a.shape
        self.size = shape[0]
        self.pattern = a
