from matplotlib import pyplot as plt
import numpy as np
import os
from utils.path import data, images
from utils.dir import get_values_from_dir
from models.ops import save_image


def drv_analysis():
    snm_hold_values = get_values_from_dir(os.path.join(data, 'out', 'hold', 'snm', 'vdd_scaling'))

    '''
    Minimum snm threshold such that the cells begin to fail beyond it.
    '''
    range_threshold = [58, 62]

    '''
    Counter for each vdd scaling. -> counter array
    '''
    counter = []

    for row in snm_hold_values:
        count = 0
        for val in row:
            if range_threshold[0] < val < range_threshold[1]:
                count = count + 1
        counter.append(count)

    vdd_start = 1.0
    vdd_stop = 0.05
    vdd_step = 0.05
    vdd_scaled = np.arange(vdd_stop, vdd_start+vdd_step, vdd_step)

    plt.bar(vdd_scaled, counter[::-1], width=0.04, color='blue', edgecolor='black')
    plt.xlabel('vdd_scaled')
    plt.ylabel('# failed_cells')
    plt.title('DRV Analysis')
    plt.tight_layout()
    save_image(image_path=os.path.join(images, "drv_analysis.png"), plt=plt)
    plt.show()


if __name__ == "__main__":
    drv_analysis()
