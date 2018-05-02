import numpy as np
import unittest
from matplotlib import pyplot as plt


class HopfieldModell():
    def __init__(self, size: "Shape of Matrix of the Pattern is (size, size)"):
        self.size = size
        self.node_number = size**2
        self.trainings_set = None
        self.H = None
        self.weights = np.zeros( (self.node_number, self.node_number) )

    def run(self,
            init_data: "Input data",
            number_of_iteration: "Number of random nodes which will be changed") -> "Reshaped Matrix result":
        """Evaluate the random choosen node evaluation algorithm."""
        assert init_data.shape == (self.size, self.size), "incompatible array size"
        init_data = init_data.flatten()
        H = np.zeros(number_of_iteration)
        for i in range(number_of_iteration):
            n = np.random.randint(self.node_number)
            init_data[n] = np.sign(np.dot(self.weights[n], init_data))
            H[i] = self.energy_function(init_data)
        self.H = H
        return init_data.reshape( (self.size, self.size) )

    def training(   self,
                    trainings_set: "array of shape (Int, Int)"):
        """Using the trainings_set to evaluate the weights of the Modell by using
        the Hebb superposition of all members of the set."""
        pattern_number, pattern_size = trainings_set.shape
        assert pattern_size == self.node_number, "incompatible array size"
        self.trainings_set = trainings_set
        for i in range(self.node_number):
            for j in range(self.node_number):
                s = 0
                for n in range(pattern_number):
                    s += trainings_set[n][i] * trainings_set[n][j]
                self.weights[i][j] = s / self.node_number

    def load_data(self, name="test"):
        self.trainings_set = np.load(name + ".npy")
        print("Load Data")


    def get_storage_capacity(self) -> "Storage capacity":
        """Compute the storage capacity of the trainings_set. if C > 1 the Modell
        is not stable"""
        assert type(self.trainings_set) != None, "No trainings_set given."
        number_of_pattern, pattern_size = self.trainings_set.shape
        C = np.zeros( (number_of_pattern, pattern_size) )
        for m in range(number_of_pattern):
            for i in range(pattern_size):
                s = 0
                for j in range(pattern_size):
                    for n in [x for x in range(number_of_pattern) if x != i]:
                        s += self.trainings_set[n][i] * self.trainings_set[n][j] * self.trainings_set[m][j]
                C[m][i] = -self.trainings_set[m][i] * s
        C = C / self.node_number
        if np.max(C) > 1:
            print("Modell may be not stable.")
        return C


    def energy_function(self, pattern):
        if pattern.shape != (self.size, self.size):
            S = pattern.flatten()
        H = np.dot(S, np.dot(self.weights, S))
        return -H / 2.0

    def plot_energy(self):
        plt.plot(range(len(self.H)), self.H)
        plt.show()


class HopfieldModellTestCase(unittest.TestCase):
    """Test class to test the HopfieldModell."""


    @unittest.expectedFailure
    def test_run_shap_fail(self):
        """Expect a fail in reason of the incompatible size of the Modell and
        input data."""
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
        self.assertTrue(np.sum( pattern - test_result ) < 10)

test = 0
if not test:
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









else:
    unittest.main()
