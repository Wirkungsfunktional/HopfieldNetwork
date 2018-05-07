import numpy as np



class SimplePerceptron():

    def __init__(self, n_in_nodes, n_out_nodes):
        self.n_in_nodes = n_in_nodes
        self.n_out_nodes = n_out_nodes
        # +1 in reason of the treshold
        self.weights = np.zeros( (self.n_in_nodes + 1, self.n_out_nodes) )
        self.trainings_set = None
        self.example_set = {    np.array([0,1]):np.array([1,1,1,1,1]),
                                np.array([1,0]:np.array([0,0,0,0,0]),
                                np.array([1,1]:np.array([0,1,1,1,0])}

    def set_trainings_set(self, trainings_set):
        self.trainings_set = trainings_set

    def activation_func(self, x):
        return np.sign( np.dot(self.weights, x))

    def training(self):
        while :

        pass

    def run(self):
        pass
