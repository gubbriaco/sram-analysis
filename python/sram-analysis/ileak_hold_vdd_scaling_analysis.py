from properties import vwl_hold
from properties import dc_vsweep_standard, rit_models_montecarlo
from properties import vsweep_standard_transient, step_param_run_standard_transient
from utils.path import ltspice, schematics, images, data
from models.ops import __init_model__, CircuitType, OperationType, RequestPlotSchematic
import os
from statistics import mean, stdev
from IPython.display import Image, display
import numpy as np


def ileak_hold_vdd_scaling_analysis():
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
    vdd_start = 1.0
    vdd_stop = vdd_start - (iterations / 10)
    vdd_step = 0.05
    print('VDD Scaling Initialised')
    row = 0
    col = 0
    vdd_standard_transient_scaled = []
    i_leak_standard_transient_hold_mean = []
    i_leak_standard_transient_hold_stdev = []
    i_leak_hold_array = []
    for scaling in np.arange(vdd_start, vdd_stop, -vdd_step):
        if row == rows:
            break
        vdd_scaled = round(scaling, 2)
        vdd_standard_transient_scaled.append(vdd_scaled)
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
            asc_file_path=os.path.join(ltspice, "standard/hold/transient/standard_hold_ileak.asc"),
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

        i_leak_mean = mean(i_leak_hold)
        i_leak_stdev = stdev(i_leak_hold)
        i_leak_standard_transient_hold_mean.append(i_leak_mean)
        i_leak_standard_transient_hold_stdev.append(i_leak_stdev)
        i_leak_hold_array.append(i_leak_hold)

        print(f'i_leak_mean_standard_transient_hold[{vdd_scaled}V] = {i_leak_mean} A')
        print(f'i_leak_stdev_standard_transient_hold[{vdd_scaled}V] = {i_leak_stdev} A')

        if col == (cols - 1):
            row = row + 1
            col = 0
        else:
            col = col + 1

    return (
        i_leak_hold_array,
        vdd_standard_transient_scaled,
        i_leak_standard_transient_hold_mean,
        i_leak_standard_transient_hold_stdev
    )
