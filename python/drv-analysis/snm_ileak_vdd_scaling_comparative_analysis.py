from utils.path import images
from models.ops import save_image
from matplotlib import pyplot as plt
import os


def snm_ileak_vdd_scaling_comparative_analysis(
        vdd_gaussian_vth_scaled,
        snm_gaussian_vth_hold_mean,
        snm_gaussian_vth_hold_stdev,
        snm_gaussian_vth_read_mean,
        snm_gaussian_vth_read_stdev,
        vdd_standard_transient_scaled,
        i_leak_standard_transient_hold_mean,
        i_leak_standard_transient_hold_stdev
):
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
        vdd_standard_transient_scaled,
        snm_gaussian_vth_hold_mean,
        snm_gaussian_vth_hold_stdev,
        snm_gaussian_vth_read_mean,
        snm_gaussian_vth_read_stdev,
        i_leak_standard_transient_hold_mean,
        i_leak_standard_transient_hold_stdev
    ):
        vdd_str = f'{vdd} V'
        snm_hold_str = f'({round(snm_hold_mean, 3)} mV, {round(snm_hold_stdev, 3)} mV)'
        snm_read_str = f'({round(snm_read_mean, 3)} mV, {round(snm_read_stdev, 3)} mV)'
        ileak_str = f'({ileak_mean} A, {i_leak_stdev} A)'
        print("{:<10} {:<25} {:<25} {:<50}".format(vdd_str, snm_hold_str, snm_read_str, ileak_str))


    fig_table_1, axs_table_1 = plt.subplots(1, 3, figsize=(16, 4))
    plt.suptitle("VDD SCALING")

    axs_table_1[0].plot(vdd_gaussian_vth_scaled, snm_gaussian_vth_hold_mean)
    axs_table_1[0].set_xlabel("vdd")
    axs_table_1[0].set_ylabel("snm_hold")
    axs_table_1[0].legend(["snm_hold"])
    axs_table_1[0].set_title("SNM(HOLD)")
    axs_table_1[0].grid()

    axs_table_1[1].plot(vdd_gaussian_vth_scaled, snm_gaussian_vth_read_mean)
    axs_table_1[1].set_xlabel("vdd")
    axs_table_1[1].set_ylabel("snm_read")
    axs_table_1[1].legend(["snm_read"])
    axs_table_1[1].set_title("SNM(READ)")
    axs_table_1[1].grid()

    axs_table_1[2].plot(vdd_standard_transient_scaled, i_leak_standard_transient_hold_mean)
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
    axs_table_2_1.plot(vdd_gaussian_vth_scaled, snm_gaussian_vth_hold_mean, '-*', label='snm_hold', color='red')
    axs_table_2_1.text(vdd_gaussian_vth_scaled[7], snm_gaussian_vth_hold_mean[7], 'snm_hold')
    axs_table_2_1.plot(vdd_gaussian_vth_scaled, snm_gaussian_vth_read_mean, '-*', label='snm_read', color='red')
    axs_table_2_1.text(vdd_gaussian_vth_scaled[7], snm_gaussian_vth_read_mean[7], 'snm_read')
    axs_table_2_1.set_xlabel("vdd")
    axs_table_2_1.set_ylabel("snm_hold, snm_read", color='red')
    axs_table_2_1.tick_params(axis='y', labelcolor='red')
    axs_table_2_1.legend(["snm_hold", "snm_read"], loc='upper left')

    axs_table_2_2 = axs_table_2_1.twinx()
    axs_table_2_2.plot(vdd_standard_transient_scaled, i_leak_standard_transient_hold_mean, '-*', label='i_leak', color='green')
    axs_table_2_2.text(vdd_standard_transient_scaled[7], i_leak_standard_transient_hold_mean[7], 'i_leak')
    axs_table_2_2.set_ylabel("i_leak", color='green')
    axs_table_2_2.tick_params(axis='y', labelcolor='green')
    axs_table_2_2.legend(["i_leak"], loc='center left')

    axs_table_2_1.grid()
    axs_table_2_2.grid()

    fig_table_2.tight_layout()
    save_image(image_path=os.path.join(images, "comparative_analysis_vdd_scaling_2.png"), plt=plt)
    plt.show()
