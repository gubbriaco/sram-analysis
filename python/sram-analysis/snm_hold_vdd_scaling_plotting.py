import numpy as np
from matplotlib import pyplot as plt
import os
from utils.dir import get_values_from_file
from utils.path import data, images
from models.ops import save_image


def snm_hold_vdd_scaling_plotting():
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
    fig_hold_snm, axs_hold_snm = plt.subplots(rows, cols, figsize=(16, 6))
    plt.suptitle("Hold Operation DC Simulation VDD Scaling")
    i = 0
    for scaling in np.arange(vdd_start, vdd_stop, -vdd_step):
        if row == rows:
            break
        vdd_scaled = round(scaling, 2)

        snm_hold_file_path = "snm_hold_vdd_scaling"
        vdd_scaled_str = str(vdd_scaled).replace('.', '')
        if vdd_scaled == 1:
            vdd_scaled_str = '1'
        snm_hold_file_path = os.path.join(f'{data}/out/hold/snm/vdd_scaling',
                                          snm_hold_file_path + '_' + vdd_scaled_str + '.txt')

        snm_hold_values = get_values_from_file(snm_hold_file_path)

        axs_hold_snm[row, col].hist(snm_hold_values, bins=100, edgecolor='black')
        axs_hold_snm[row, col].set_xlabel("SNM(HOLD)")
        axs_hold_snm[row, col].set_ylabel("#")
        axs_hold_snm[row, col].set_title(f"vdd={vdd_scaled} V Histogram")
        i = i+1

        if col == (cols - 1):
            row = row + 1
            col = 0
        else:
            col = col + 1

    plt.tight_layout()
    plt.subplots_adjust(hspace=1.5, wspace=1)
    save_image(image_path=os.path.join(images, "hold_operation_dc_vdd_scaling.png"), plt=plt)
    plt.show()


if __name__ == "__main__":
    snm_hold_vdd_scaling_plotting()
