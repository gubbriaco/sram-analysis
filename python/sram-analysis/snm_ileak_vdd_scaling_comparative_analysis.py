from utils.dir import get_values_from_dir, get_mean_from_file, get_stdev_from_file
from utils.path import images
from models.ops import save_image
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table
import os
import numpy as np


def snm_ileak_vdd_scaling_comparative_analysis():
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
    print('VDD Scaling Initialised')
    row = 0
    col = 0
    vdd_scaled = []
    for scaling in np.arange(vdd_start, vdd_stop, -vdd_step):
        if row == rows:
            break
        vdd_scaled_value = round(scaling, 2)
        vdd_scaled.append(vdd_scaled_value)

        if col == (cols - 1):
            row = row + 1
            col = 0
        else:
            col = col + 1

    from utils.path import data
    snm_hold_values = get_values_from_dir(os.path.join(data, 'out', 'hold', 'snm', 'vdd_scaling'))
    snm_read_values = get_values_from_dir(os.path.join(data, 'out', 'read', 'snm', 'vdd_scaling'))
    ileak_hold_values = get_values_from_dir(os.path.join(data, 'out', 'hold', 'ileak', 'vdd_scaling'))

    snm_gaussian_vth_hold_mean = get_mean_from_file(snm_hold_values)
    snm_gaussian_vth_hold_stdev = get_stdev_from_file(snm_hold_values)

    snm_gaussian_vth_read_mean = get_mean_from_file(snm_read_values)
    snm_gaussian_vth_read_stdev = get_stdev_from_file(snm_read_values)

    i_leak_standard_hold_mean = get_mean_from_file(ileak_hold_values)
    i_leak_standard_hold_stdev = get_stdev_from_file(ileak_hold_values)

    print("{:<10} {:<25} {:<25} {:<50}".format("VDD", "SNM(HOLD)", "SNM(READ)", "I_LEAK"))
    for (
            vdd,
            snm_hold_mean,
            snm_hold_stdev,
            snm_read_mean,
            snm_read_stdev,
            ileak_mean,
            i_leak_stdev
    ) in zip(
        vdd_scaled,
        snm_gaussian_vth_hold_mean,
        snm_gaussian_vth_hold_stdev,
        snm_gaussian_vth_read_mean,
        snm_gaussian_vth_read_stdev,
        i_leak_standard_hold_mean,
        i_leak_standard_hold_stdev
    ):
        vdd_str = f'{vdd} V'
        snm_hold_str = f'({round(snm_hold_mean, 3)} mV, {round(snm_hold_stdev, 3)} mV)'
        snm_read_str = f'({round(snm_read_mean, 3)} mV, {round(snm_read_stdev, 3)} mV)'
        ileak_str = f'({ileak_mean} A, {i_leak_stdev} A)'
        print("{:<10} {:<25} {:<25} {:<50}".format(vdd_str, snm_hold_str, snm_read_str, ileak_str))


    fig_table_1, axs_table_1 = plt.subplots(1, 3, figsize=(16, 4))
    plt.suptitle("VDD SCALING")

    axs_table_1[0].plot(vdd_scaled, snm_gaussian_vth_hold_mean)
    axs_table_1[0].set_xlabel("vdd")
    axs_table_1[0].set_ylabel("snm_hold")
    axs_table_1[0].legend(["snm_hold"])
    axs_table_1[0].set_title("SNM(HOLD)")
    axs_table_1[0].grid()

    axs_table_1[1].plot(vdd_scaled, snm_gaussian_vth_read_mean)
    axs_table_1[1].set_xlabel("vdd")
    axs_table_1[1].set_ylabel("snm_read")
    axs_table_1[1].legend(["snm_read"])
    axs_table_1[1].set_title("SNM(READ)")
    axs_table_1[1].grid()

    axs_table_1[2].plot(vdd_scaled, i_leak_standard_hold_mean)
    axs_table_1[2].set_xlabel("vdd")
    axs_table_1[2].set_ylabel("i_leak")
    axs_table_1[2].legend(["i_leak"])
    axs_table_1[2].set_title("I_LEAK")
    axs_table_1[2].grid()

    plt.tight_layout()
    plt.subplots_adjust(wspace=0.5)
    save_image(image_path=os.path.join(images, "comparative_analysis_vdd_scaling_1.png"), plt=plt)
    plt.show()


    fig_table_2, axs_table_2_1 = plt.subplots(1, 1)
    plt.suptitle("VDD SCALING")
    axs_table_2_1.plot(vdd_scaled, snm_gaussian_vth_hold_mean, '-*', label='snm_hold', color='red')
    axs_table_2_1.text(vdd_scaled[7], snm_gaussian_vth_hold_mean[7], 'snm_hold')
    axs_table_2_1.plot(vdd_scaled, snm_gaussian_vth_read_mean, '-*', label='snm_read', color='red')
    axs_table_2_1.text(vdd_scaled[7], snm_gaussian_vth_read_mean[7], 'snm_read')
    axs_table_2_1.set_xlabel("vdd")
    axs_table_2_1.set_ylabel("snm_hold, snm_read", color='red')
    axs_table_2_1.tick_params(axis='y', labelcolor='red')
    axs_table_2_1.legend(["snm_hold", "snm_read"], loc='upper left')

    axs_table_2_2 = axs_table_2_1.twinx()
    axs_table_2_2.plot(vdd_scaled, i_leak_standard_hold_mean, '-*', label='i_leak', color='green')
    axs_table_2_2.text(vdd_scaled[7], i_leak_standard_hold_mean[7], 'i_leak')
    axs_table_2_2.set_ylabel("i_leak", color='green')
    axs_table_2_2.tick_params(axis='y', labelcolor='green')
    axs_table_2_2.legend(["i_leak"], loc='center left')

    axs_table_2_1.grid()
    axs_table_2_2.grid()

    fig_table_2.tight_layout()
    save_image(image_path=os.path.join(images, "comparative_analysis_vdd_scaling_2.png"), plt=plt)
    plt.show()

    data = {
        'vdd [V]': vdd_scaled,
        'snm(hold)_mean [mV]': snm_gaussian_vth_hold_mean,
        'snm(hold)_stdev [mV]': snm_gaussian_vth_hold_stdev,
        'snm(read)_mean [mV]': snm_gaussian_vth_read_mean,
        'snm(read)_stdev [mV]': snm_gaussian_vth_read_stdev,
        'ileak(hold)_mean [A]': i_leak_standard_hold_mean,
        'ileak(hold)_stdev [A]': i_leak_standard_hold_stdev
    }
    df = pd.DataFrame(data)
    blankIndex = [''] * len(df)
    df.index = blankIndex

    fig_table_comparative, ax_table_comparative = plt.subplots(figsize=(16, 4))
    ax_table_comparative.set_frame_on(False)
    tab = table(
        ax_table_comparative,
        df,
        loc='upper center',
        colWidths=[0.15] * len(df.columns),
        cellLoc='center'
    )
    tab.auto_set_font_size(False)
    tab.set_fontsize(10)
    tab.scale(1.2, 1.2)

    for key, cell in tab.get_celld().items():
        cell.set_text_props(fontweight='bold')

    ax_table_comparative.axis('off')

    fig_table_comparative.tight_layout()
    save_image(image_path=os.path.join(images, "table_comparative_analysis_vdd_scaling.png"), plt=plt)
    plt.show()


if __name__ == "__main__":
    snm_ileak_vdd_scaling_comparative_analysis()
