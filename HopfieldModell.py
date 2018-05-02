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
                    trainings_set = "None"):
        """Using the trainings_set to evaluate the weights of the Modell by using
        the Hebb superposition of all members of the set."""
        if trainings_set != "None":
            self.trainings_set = trainings_set
        pattern_number, pattern_size = self.trainings_set.shape
        assert pattern_size == self.node_number, "incompatible array size"
        self.get_storage_capacity()
        for n in range(pattern_number):
            self.weights += np.outer(self.trainings_set[n], self.trainings_set[n])
        self.weights /= self.node_number
        if self.is_self_coupling():
            print("The Modell is self coupling. This can produce spurious states.")
        else:
            print("The Modell is not self coupling.")

    def load_data(self, name="test"):
        self.trainings_set = np.load(name + ".npy")
        print("Load Data")


    def get_storage_capacity(self) -> "Storage capacity":
        """Compute the storage capacity of the trainings_set. if C > 1 the Modell
        is not stable"""
        assert type(self.trainings_set) != None, "No trainings_set given."
        number_of_pattern, pattern_size = self.trainings_set.shape
        C = np.zeros( (number_of_pattern, pattern_size) )
        # TODO: Improve the multiplication by numpy operations
        for m in range(number_of_pattern):
            for i in range(pattern_size):
                s = 0
                for n in [x for x in range(number_of_pattern) if x != i]:
                    s += self.trainings_set[n][i] * np.dot(self.trainings_set[n], self.trainings_set[m])
                C[m][i] = -self.trainings_set[m][i] * s
        C = C / self.node_number
        if np.max(C) > 1:
            print("Modell may be not stable.")
        else:
            print("Storage capacity is below 1.")
        return C


    def energy_function(self, pattern):
        """Evaluate the energy_function H = - \frac{1}{2} \sum w_{ij} S_i S_j
        of the HopfieldModell for the given pattern."""
        if pattern.shape != (self.size, self.size):
            S = pattern.flatten()
        H = np.dot(S, np.dot(self.weights, S))
        return -H / 2.0

    def plot_energy(self):
        plt.plot(range(len(self.H)), self.H)
        plt.show()

    def is_self_coupling(self) -> "Bool":
        """The nodes are self coupling if there are weights[i][i] != 0. If so the
        function returns True else False. Self coupling can produce spurious
        states and is therefore not likely. See delete_self_coupling()."""
        if np.sum(np.diagonal(self.weights)) != 0:
            return True
        else:
            return False

    def delete_self_coupling(self):
        """Set the diagonal entries of weights[i][i] to 0 for avoiding spurious
        states."""
        self.weights -= np.diag(np.diagonal(self.weights))


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

    def test_self_coupling(self):
        h = HopfieldModell(2)
        h.weights = np.diag(np.ones(4))
        self.assertTrue(h.is_self_coupling())
        h.delete_self_coupling()
        self.assertFalse(h.is_self_coupling())

test = 0
version = 2
if not test:
    if version == 1:
        n = 20
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
        h.plot_energy()
    if version == 2:
        n = 15
        h = HopfieldModell(n)
        h.load_data("Symbols")
        h.training()
        #h.delete_self_coupling()
        test_pattern = h.trainings_set[1].reshape((n,n))
        for i in range(int(n/2)):
            index1 = np.random.randint(n)
            index2 = np.random.randint(n)
            test_pattern[index1][index2] = np.random.randint(3) - 1
        plt.imshow(test_pattern)
        plt.show()
        test_result = h.run(test_pattern, 2000)
        plt.imshow(test_result)
        plt.show()









else:
    unittest.main()
