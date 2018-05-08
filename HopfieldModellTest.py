from HopfieldModell import HopfieldModell
import unittest



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
            test_pattern[index1][index2] *= -1
        test_result = h.run(test_pattern, 1000)
        self.assertTrue(np.sum( pattern - test_result ) < 10)

    def test_self_coupling(self):
        h = HopfieldModell(2)
        h.weights = np.diag(np.ones(4))
        self.assertTrue(h.is_self_coupling())
        h.delete_self_coupling()
        self.assertFalse(h.is_self_coupling())


test = 0
version = 3
if not test:
    if version == 1:
        n = 20
        h = HM.HopfieldModell(n)
        pattern = np.ones( (n, n) ) - 2*np.diag(np.ones(n))
        trainings_set = np.zeros( (1, n**2) )
        trainings_set[0] = pattern.flatten()
        h.training(trainings_set)
        test_pattern = pattern
        for i in range(int(n/4)):
            index1 = np.random.randint(n)
            index2 = np.random.randint(n)
            test_pattern[index1][index2] = np.random.randint(3) - 1
        test_result = h.run(test_pattern, 1000)
        h.plot_energy()
    if version == 2:
        n = 20
        h = HopfieldModell(n)
        h.load_data("test")
        h.training()
        h.delete_self_coupling()
        test_pattern = h.trainings_set[2].reshape((n,n)).copy()
        for i in range(int(n)):
            index1 = np.random.randint(n)
            index2 = np.random.randint(n)
            test_pattern[index1][index2] = -1
        plt.imshow(test_pattern)
        plt.show()
        test_result = h.run(test_pattern.copy(), 100000)
        #h.plot_energy()
        plt.imshow(test_result)
        plt.show()
    if version == 3:
        n = 10
        h = HopfieldModell(n)
        h.create_maximal_random_set()
        h.training()
        print(h.test_trainings_pattern(0.4, 10000))

else:
    unittest.main()
