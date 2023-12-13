import numpy as np
from matplotlib import pyplot as plt
import os
from utils.dir import get_values_from_file
from utils.path import data, images
from models.ops import save_image
from properties import vdd_start, vdd_stop, vdd_step, rows, cols


def snm_read_vdd_scaling_plotting():
    row = 0
    col = 0
    fig_read_snm, axs_read_snm = plt.subplots(rows, cols, figsize=(16, 6))
    plt.suptitle("Read Operation DC Simulation VDD Scaling")
    i = 0
    for scaling in np.arange(vdd_start, vdd_stop, -vdd_step):
        if row == rows:
            break
        vdd_scaled = round(scaling, 2)

        snm_read_file_path = "snm_read_vdd_scaling"
        vdd_scaled_str = str(vdd_scaled).replace('.', '')
        if vdd_scaled == 1:
            vdd_scaled_str = '1'
        snm_read_file_path = os.path.join(f'{data}/out/read/snm/vdd_scaling',
                                          snm_read_file_path + '_' + vdd_scaled_str + '.txt')

        snm_read_values = get_values_from_file(snm_read_file_path)

        axs_read_snm[row, col].hist(snm_read_values, bins=100, edgecolor='black')
        axs_read_snm[row, col].set_xlabel("SNM(READ)")
        axs_read_snm[row, col].set_ylabel("#")
        axs_read_snm[row, col].set_title(f"vdd={vdd_scaled} V Histogram")
        i = i+1

        if col == (cols - 1):
            row = row + 1
            col = 0
        else:
            col = col + 1

    plt.tight_layout()
    plt.subplots_adjust(hspace=1.5, wspace=1)
    save_image(image_path=os.path.join(images, "read_operation_dc_vdd_scaling.png"), plt=plt)
    plt.show()


if __name__ == "__main__":
    snm_read_vdd_scaling_plotting()
