import numpy as np
from matplotlib import pyplot as plt
import os
from utils.dir import get_values_from_file
from utils.path import data, images
from models.ops import save_image


def ileak_hold_vdd_scaling_plotting():
    iterations_scaling = 16
    rows = round(int(np.sqrt(iterations_scaling)))
    tmp = iterations_scaling % rows
    iterations = iterations_scaling
    if tmp == 1:
        iterations = iterations_scaling + (rows - 1)
    elif tmp == 2:
        iterations = iterations_scaling + (rows - 2)
    cols = int(iterations / rows)
    vdd_start = 1.0
    vdd_stop = vdd_start - (iterations / 10)
    vdd_step = 0.05

    row = 0
    col = 0

    fig_ileak_hold, axs_ileak_hold = plt.subplots(rows, cols, figsize=(16, 6))
    plt.suptitle("I Leak Hold Operation DC Simulation VDD Scaling")
    i = 0
    for scaling in np.arange(vdd_start, vdd_stop, -vdd_step):
        if row == rows:
            break
        vdd_scaled = round(scaling, 2)

        ileak_hold_file_path = "ileak_hold_vdd_scaling"
        vdd_scaled_str = str(vdd_scaled).replace('.', '')
        if vdd_scaled == 1:
            vdd_scaled_str = '1'
        ileak_hold_file_path = os.path.join(f'{data}/out/hold/ileak/vdd_scaling',
                                            ileak_hold_file_path + '_' + vdd_scaled_str + '.txt')

        ileak_hold_values = get_values_from_file(ileak_hold_file_path)

        axs_ileak_hold[row, col].hist(ileak_hold_values, bins=100, edgecolor='black')
        axs_ileak_hold[row, col].set_xlabel("I_LEAK(HOLD)")
        axs_ileak_hold[row, col].set_ylabel("#")
        axs_ileak_hold[row, col].set_title(f"vdd={vdd_scaled} V Histogram")
        i = i + 1

        if col == (cols - 1):
            row = row + 1
            col = 0
        else:
            col = col + 1

    plt.tight_layout()
    plt.subplots_adjust(hspace=1.5, wspace=1)
    save_image(image_path=os.path.join(images, "ileak_hold_operation_dc_vdd_scaling.png"), plt=plt)
    plt.show()


if __name__ == "__main__":
    ileak_hold_vdd_scaling_plotting()
