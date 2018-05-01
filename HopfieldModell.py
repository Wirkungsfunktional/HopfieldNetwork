import numpy as np
import unittest


class HopfieldModell():
    def __init__(self, size):
        self.size = size
        self.node_number = size**2

        self.weights = np.zeros( (self.node_number, self.node_number) )

    def run(self, init_data, number_of_iteration):
        assert init_data.shape == (self.size, self.size), "incompatible array size"
        init_data = init_data.flatten()
        for i in range(number_of_iteration):
            n = np.random.randint(self.node_number)
            init_data[n] = np.sign(np.dot(self.weights[n], init_data))
        return init_data.reshape( (self.size, self.size) )

    def training(self, trainings_set):
        pattern_number, pattern_size = trainings_set.shape
        assert pattern_size == self.node_number, "incompatible array size"
        for i in range(self.node_number):
            for j in range(self.node_number):
                s = 0
                for n in range(pattern_number):
                    s += trainings_set[n][i] * trainings_set[n][j]
                self.weights[i][j] = s



class HopfieldModellTestCase(unittest.TestCase):
    @unittest.expectedFailure
    def test_run_shap_fail(self):
        h = HopfieldModell(15)
        h.run(np.array([2, 3, 5]), 10)

    def test_run_of_single_pattern(self):
        n = 15
        h = HopfieldModell(n)
        pattern = np.ones( (n, n) ) - 2*np.diag(np.ones(n))
        trainings_set = np.zeros( (1, n**2) )
        trainings_set[0] = pattern.flatten()
        h.training(trainings_set)
        test_pattern = pattern
        for i in range(int(n/2)):
            index1 = np.random.randint(n)
            index2 = np.random.randint(n)
            test_pattern[index1][index2] = np.random.randint(3) - 1
        test_result = h.run(test_pattern, 1000)
        assert np.sum( pattern - test_result ) < 10





unittest.main()
