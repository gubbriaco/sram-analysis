from matplotlib import pyplot as plt
import os
from utils.path import data
from utils.dir import get_values_from_dir
import numpy as np


def drv_analysis(plot_lock):
    snm_hold_values = get_values_from_dir(os.path.join(data, 'out', 'hold', 'snm'))

    '''
    Minimum voltage threshold such that the cells begin to fail beyond it.
    '''
    threshold = 60

    '''
    Counter for each vdd scaling. -> counter array
    '''
    counter = []

    for row in snm_hold_values:
        count = 0
        for val in row:
            if val < threshold:
                count = count + 1
        counter.append(count)

    vdd_start = 1.0
    vdd_stop = 0.25
    vdd_step = 0.05
    vdd_scaled = np.arange(vdd_stop, vdd_start+vdd_step, vdd_step)

    with plot_lock:
        plt.bar(vdd_scaled, counter[::-1], width=0.04, color='blue', edgecolor='black')
        plt.xlabel('vdd_scaled')
        plt.ylabel('# failed_cells')
        plt.title('DRV Analysis')
        plt.tight_layout()
        plt.show()
