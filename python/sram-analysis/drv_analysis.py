from matplotlib import pyplot as plt
import numpy as np
import os
from utils.path import data, images
from models.ops import save_image, table_creation
from utils.dir import get_mean_from_file, get_stdev_from_file, get_values_from_dir


def drv_analysis():
    snm_hold_values = get_values_from_dir(os.path.join(data, 'out', 'hold', 'snm', 'vdd_scaling'))

    '''
    Minimum snm threshold such that the cells begin to fail beyond it.
    '''
    range_threshold = [58.5, 61.5]

    '''
    Counter for each vdd scaling. -> counter array
    '''
    counter = []

    for i, row in enumerate(snm_hold_values):
        count = 0
        for val in row:
            if range_threshold[0] < val < range_threshold[1]:
                count = count + 1
        counter.append(count)
        print(f'{round(1-(i*0.05), 2)}V -> {count} failed cells.')

    vdd_start = 1.0
    vdd_stop = 0.05
    vdd_step = 0.05
    vdd_scaled = np.arange(vdd_stop, vdd_start+vdd_step, vdd_step)

    data_table_drv_analysis = {
        'vdd [V]': [round(vdd, 2) for vdd in vdd_scaled[::-1]],
        'failed_cells': ['%g'%c for c in counter]
    }
    table_creation(
        data_table=data_table_drv_analysis,
        title_plot="DRV Analysis Failed Cells",
        title_image_saving="table_drv_analysis.png",
        figsize=[12, 6]
    )

    plt.bar(vdd_scaled, counter[::-1], width=0.04, color='blue', edgecolor='black')
    plt.xlabel('vdd_scaled')
    plt.ylabel('# failed_cells')
    plt.title('DRV Analysis')
    plt.tight_layout()
    save_image(image_path=os.path.join(images, "drv_analysis.png"), plt=plt)
    plt.show()


    snm_hold_values = get_values_from_dir(os.path.join(data, 'out', 'hold', 'snm', 'vdd_scaling'))
    snm_read_values = get_values_from_dir(os.path.join(data, 'out', 'read', 'snm', 'vdd_scaling'))
    ileak_hold_values = get_values_from_dir(os.path.join(data, 'out', 'hold', 'ileak', 'vdd_scaling'))

    snm_gaussian_vth_hold_mean = get_mean_from_file(snm_hold_values)
    snm_gaussian_vth_hold_stdev = get_stdev_from_file(snm_hold_values)

    snm_gaussian_vth_read_mean = get_mean_from_file(snm_read_values)
    snm_gaussian_vth_read_stdev = get_stdev_from_file(snm_read_values)

    i_leak_standard_hold_mean = get_mean_from_file(ileak_hold_values)
    i_leak_standard_hold_stdev = get_stdev_from_file(ileak_hold_values)

    p_leak_standard_hold_mean = [ileakmean * vdd for ileakmean, vdd in zip(i_leak_standard_hold_mean, vdd_scaled)]
    p_leak_standard_hold_stdev = [ileakstdev * vdd for ileakstdev, vdd in zip(i_leak_standard_hold_stdev, vdd_scaled)]

    data_table_comparative_analysis_vdd_scaling = {
        'vdd [V]': [round(vdd, 2) for vdd in vdd_scaled[::-1]],
        'snm(hold)_mean [mV]': [round(val, 5) for val in snm_gaussian_vth_hold_mean],
        'snm(hold)_stdev [mV]': [round(val, 5) for val in snm_gaussian_vth_hold_stdev],
        'snm(read)_mean [mV]': [round(val, 5) for val in snm_gaussian_vth_read_mean],
        'snm(read)_stdev [mV]': [round(val, 5) for val in snm_gaussian_vth_read_stdev],
        'ileak(hold)_mean [A]': [round(val, 11) for val in i_leak_standard_hold_mean],
        'ileak(hold)_stdev [A]': [round(val, 11) for val in i_leak_standard_hold_stdev],
        'pleak(hold)_mean [W]': [round(val, 11) for val in p_leak_standard_hold_mean],
        'pleak(hold)_stdev [W]': [round(val, 11) for val in p_leak_standard_hold_stdev],
        'failed_cells': ['%g'%c for c in counter]
    }
    table_creation(
        data_table=data_table_comparative_analysis_vdd_scaling,
        title_plot="Comparative Analysis VDD Scaling with DRV Analysis",
        title_image_saving="table_comparative_drv_analysis_vdd_scaling.png",
        figsize=[28, 6]
    )


if __name__ == "__main__":
    drv_analysis()
