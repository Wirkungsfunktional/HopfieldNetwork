import numpy as np



class Pattern():
    def __init__(self, size):
        self.size = size
        self.pattern = np.ones( (self.size, self.size) )

    def get_quadratic_rep(self):
        return self.pattern

    def get_column_rep(self):
        return self.pattern.flatten()

    @staticmethod
    def make_random_pattern(size):
        p = Pattern(size)
        p.set_pattern_from_matrix(np.ones( (size, size) ) - \
                2*np.random.randint(2, size = (size, size)))
        return p

    def set_point(self, i, j, value):
        self.pattern[i][j] = value

    def set_pattern_from_matrix(self, a):
        shape = a.shape
        self.size = shape[0]
        self.pattern = a

    def apply_mask(self, mask):
        self.pattern *= mask.pattern
