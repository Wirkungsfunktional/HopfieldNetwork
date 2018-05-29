import HopfieldModell
from matplotlib import pyplot as plt
import numpy as np
import matplotlib
import scipy.special as sis
from scipy.optimize import fsolve
import scipy.stats as sst

def pattern_noise(pattern, p):
    sizeA, sizeB = pattern.shape
    for n in range(int(sizeA*sizeB * p)):
        index1 = np.random.randint(sizeA)
        index2 = np.random.randint(sizeB)
        pattern[index1][index2] *= - 1
    return pattern

def random_pattern_set(n, size):
    return np.array([np.ones(size**2) -  2*np.random.randint(2, size=(size**2))\
                        for i in range(n)])


def make_phase_plot(
        n: int,
        t_min: float, t_max: float, t_step: int,
        p_min: int  , p_step: int,
        iteration_number: int, p_noise: float):

    h = HopfieldModell.StochasticHopfieldModell(n)
    h.energy_option = 0
    p_max = int(0.15 * n**2 )
    cut_off = int(n**2 * p_noise)
    temp = np.linspace(t_min, t_max, t_step)
    p = np.arange(p_min, p_max + 0.1, p_step, dtype=int)
    erg = np.zeros( (len(temp), len(p)) )
    for i, pattern in enumerate(p):
        flag = 0
        h.trainings_set = random_pattern_set(pattern, n)
        h.training()
        j = 0
        while (flag < 4) and j < len(temp):
            h.temp = temp[j]
            s = []
            #test_pattern = np.copy(h.trainings_set[0]).reshape( (n, n) )
            for k in range(2):
                test_pattern = np.copy(h.trainings_set[np.random.randint(pattern)]).reshape( (n, n) )
                noise_pattern = pattern_noise(np.copy(test_pattern), p_noise)
                noise_pattern = h.run(noise_pattern, iteration_number)
                s.append(np.sum(np.abs(noise_pattern - test_pattern)))
            erg[j][i] = np.mean(s)
            if erg[j][i] > cut_off:
                flag += 1
            j += 1
        print(j)
    plt.imshow(erg, origin="lower", extent=(p_min/n**2, p_max/n**2, t_min, t_max), aspect="auto")
    plt.show()
    name =  "data/PhasePlot_ " + \
            "t_" + str(t_min) + "_" + str(t_max) + "_" + str(t_step) + "_" + \
            "p_" + str(p_min) + "_" + str(p_max) + "_" + str(p_step) + "_" +  \
            "size_" + str(n**2) + "_" + \
            "iter_" + str(iteration_number) + "_" + \
            "p_noise_" + str(p_noise)
    np.save(name, erg)

def load_data():
    font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 28}
    matplotlib.rc('font', **font)
    fig, ax = plt.subplots()
    data = np.load("t_0p01_1_20_p_1_844_20_n_75_i_50000.npy")
    n = 75
    p_min = 1
    p_max = int(0.15 * n**2 )
    p = np.arange(p_min, p_max + 0.1, 20)
    t_min = 0.01
    t_max = 1.0
    imgplot = plt.imshow(data, origin="lower", aspect="auto", extent=(p_min/n**2, p[-1]/n**2, t_min, t_max))
    imgplot.set_cmap('brg')
    cbar = fig.colorbar(imgplot)
    ax.set_xlabel(r"$\alpha$", fontsize=40)
    ax.set_ylabel(r"T", fontsize=40)
    plt.show()


if __name__ == '__main__':
    make_phase_plot(25, 0.01, 1.0, 10, 1, 20, 5000, 0.01)
    load_data()
