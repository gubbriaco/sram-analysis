from properties import vwl_hold
from properties import dc_vsweep_standard, rit_models_montecarlo
from properties import vsweep_standard_transient, step_param_run_standard_transient
from utils.path import ltspice, schematics, images, data
from models.ops import save_image, __init_model__, CircuitType, OperationType, RequestPlotSchematic
from matplotlib import pyplot as plt
import os
from statistics import mean, stdev
from IPython.display import Image, display
import numpy as np


def ileak_hold_vdd_scaling_analysis(
        snm_gaussian_vth_hold_mean,
        snm_gaussian_vth_hold_stdev,
        snm_gaussian_vth_read_mean,
        snm_gaussian_vth_read_stdev
):
    schematic_image_path = os.path.join(schematics, "standard_transient.png")
    display(Image(schematic_image_path))

    iterations_scaling = 16
    rows = round(int(np.sqrt(iterations_scaling)))
    tmp = iterations_scaling % rows
    iterations = iterations_scaling
    if tmp == 1:
        iterations = iterations_scaling + (rows - 1)
    elif tmp == 2:
        iterations = iterations_scaling + (rows - 2)
    cols = int(iterations / rows)
    fig_standard_transient_hold_ileak, axs_standard_transient_hold_ileak = plt.subplots(rows, cols, figsize=(16, 6))
    plt.suptitle("Hold Operation Standard Transient Simulation VDD Scaling")
    vdd_start = 1.0
    vdd_stop = vdd_start - (iterations / 10)
    vdd_step = 0.05
    print('VDD Scaling Initialised')
    row = 0
    col = 0
    vdd_standard_transient_scaled = []
    i_leak_standard_transient_hold_mean = []
    i_leak_standard_transient_hold_stdev = []
    for scaling in np.arange(vdd_start, vdd_stop, -vdd_step):
        if row == rows:
            break
        vdd_scaled = round(scaling, 2)
        vdd_standard_transient_scaled.append(vdd_scaled)
        print(
            '****************************************************************************************************************')
        print(f'vdd = {vdd_scaled} V')
        (
            steps,
            time_standard_transient_hold,
            i_leaks_standard_transient_hold,
            v_q_standard_transient_hold,
            v_q_neg_standard_transient_hold,
            v_dd_standard_transient_hold,
            v_wl_standard_transient_hold,
            v_bl_standard_transient_hold,
            v_blneg_standard_transient_hold,
            standard_hold_transient_log
        ) = __init_model__(
            operation_type=OperationType.HOLD,
            circuit_type=CircuitType.STANDARD_TRANSIENT,
            asc_file_path=os.path.join(ltspice, "standard/hold/transient/standard_hold.asc"),
            schematic_image_path=os.path.join(schematics, "standard_transient.png"),
            request_plot_schematic=RequestPlotSchematic.FALSE,
            vdd=f'{vdd_scaled}',
            vsweep=vsweep_standard_transient,
            vwl=vwl_hold,
            vbl=f'{vdd_scaled}',
            vblneg=f'{vdd_scaled}',
            params=[rit_models_montecarlo, step_param_run_standard_transient, dc_vsweep_standard]
        )

        i_leak_ax_q = i_leaks_standard_transient_hold[0]
        i_leak_pu_q = i_leaks_standard_transient_hold[1]
        i_leak_pd_qneg = i_leaks_standard_transient_hold[2]

        ileakaxq = []
        ileakpuq = []
        ileakpdqneg = []

        for step in range(len(steps)):
            ileakaxq_value = i_leak_ax_q.get_wave(step)
            ileakpuq_value = i_leak_pu_q.get_wave(step)
            ileakpdqneg_value = i_leak_pd_qneg.get_wave(step)

            ileakaxq.append(abs(ileakaxq_value))
            ileakpuq.append(abs(ileakpuq_value))
            ileakpdqneg.append(abs(ileakpdqneg_value))

        ileakaxq_transient = []
        ileakpuq_transient = []
        ileakpdqneg_transient = []
        for i, value in enumerate(ileakaxq):
            ileakaxq_transient.append(value[len(value) - 1])
        for i, value in enumerate(ileakpuq):
            ileakpuq_transient.append(value[len(value) - 1])
        for i, value in enumerate(ileakpdqneg):
            ileakpdqneg_transient.append(value[len(value) - 1])

        i_leak_hold = [value1 + value2 + value3 for value1, value2, value3 in
                       zip(ileakaxq_transient, ileakpuq_transient, ileakpdqneg_transient)]

        i_leak_hold_file_path = "ileak_hold"
        vdd_scaled_str = str(vdd_scaled).replace('.', '')
        if vdd_scaled == 1:
            vdd_scaled_str = '1'
        i_leak_hold_file_path = os.path.join(f'{data}/out/hold/ileak',
                                             i_leak_hold_file_path + '_' + vdd_scaled_str + '.txt')
        with open(i_leak_hold_file_path, 'w') as file:
            for val in i_leak_hold:
                file.write(f'{val}\n')

        axs_standard_transient_hold_ileak[row, col].hist(i_leak_hold, bins=100, edgecolor='black')
        axs_standard_transient_hold_ileak[row, col].set_xlabel("I_LEAK(HOLD)")
        axs_standard_transient_hold_ileak[row, col].set_ylabel("#")
        axs_standard_transient_hold_ileak[row, col].set_title(f"vdd={vdd_scaled} V Histogram")

        i_leak_mean = mean(i_leak_hold)
        i_leak_stdev = stdev(i_leak_hold)
        i_leak_standard_transient_hold_mean.append(i_leak_mean)
        i_leak_standard_transient_hold_stdev.append(i_leak_stdev)
        print(f'i_leak_mean_standard_transient_hold = {i_leak_mean} A')
        print(f'i_leak_stdev_standard_transient_hold = {i_leak_stdev} A')

        if col == (cols - 1):
            row = row + 1
            col = 0
        else:
            col = col + 1

    plt.tight_layout()
    plt.subplots_adjust(hspace=1.5, wspace=1)
    save_image(image_path=os.path.join(images, "hold_operation_transient_vdd_scaling.png"), plt=plt)
    plt.show()

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

    return vdd_standard_transient_scaled, i_leak_standard_transient_hold_mean
