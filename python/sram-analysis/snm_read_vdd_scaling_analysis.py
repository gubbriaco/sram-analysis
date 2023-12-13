from properties import vsweep_gaussian_vth
from properties import snm_max, snm_min, rit_models_montecarlo, dc_vsweep_gaussian_vth, step_param_run_gaussian_vth
from utils.path import ltspice, schematics, data
from utils.patterns import snm_max_seevinck_pattern, snm_min_seevinck_pattern
from models.ops import get_data, __init_model__, CircuitType, OperationType, RequestPlotSchematic
import os
from statistics import mean, stdev
import numpy as np


def snm_read_vdd_scaling_analysis():
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
    vdd_gaussian_vth_scaled = []
    snm_gaussian_vth_read_mean = []
    snm_gaussian_vth_read_stdev = []
    snm_read_array = []
    for scaling in np.arange(vdd_start, vdd_stop, -vdd_step):
        if row == rows:
            break
        vdd_scaled = round(scaling, 2)
        vdd_gaussian_vth_scaled.append(vdd_scaled)
        (
            steps,
            vsweep_gaussian_vth_read,
            i_leaks_gaussian_vth_read,
            v_1_gaussian_vth_read,
            v_2_gaussian_vth_read,
            v_dd_gaussian_vth_read,
            v_wl_gaussian_vth_read,
            v_bl_gaussian_vth_read,
            v_blneg_gaussian_vth_read,
            gaussian_vth_read_log
        ) = __init_model__(
            operation_type=OperationType.READ,
            circuit_type=CircuitType.GAUSSIAN_VTH_DC,
            asc_file_path=os.path.join(ltspice, "gaussian-vth/read/gaussian_vth_read.asc"),
            schematic_image_path=os.path.join(schematics, "gaussian_vth.png"),
            request_plot_schematic=RequestPlotSchematic.FALSE,
            vdd=f'{vdd_scaled}',
            vsweep=vsweep_gaussian_vth,
            vwl=f'{vdd_scaled}',
            vbl=f'{vdd_scaled}',
            vblneg=f'{vdd_scaled}',
            params=[rit_models_montecarlo, dc_vsweep_gaussian_vth(-0.707 * scaling, 0.707 * scaling, 0.01),
                    step_param_run_gaussian_vth, snm_max(0.707), snm_min(0.707)]
        )

        vq_gaussian_vth_read = []
        vqneg_gaussian_vth_read = []
        vq_vqneg_gaussian_vth_read = []
        x_gaussian_vth_read = []

        for step in range(len(steps)):
            vq = v_1_gaussian_vth_read.get_wave(step)
            vqneg = v_2_gaussian_vth_read.get_wave(step)
            vq_minus_vqneg = vq - vqneg
            vq_gaussian_vth_read.append(vq)
            vqneg_gaussian_vth_read.append(vqneg)
            vq_vqneg_gaussian_vth_read.append(vq_minus_vqneg)
            x = vsweep_gaussian_vth_read.get_wave(step)
            x_gaussian_vth_read.append(x)

        gaussian_vth_read_log_file_path = f"./{gaussian_vth_read_log}"
        with open(gaussian_vth_read_log_file_path, "r") as file:
            content = file.read()

        snm_max_gaussian_vth_read = get_data(pattern=snm_max_seevinck_pattern, content=content)
        snm_max_gaussian_vth_read = [1000 * value for value in snm_max_gaussian_vth_read]

        snm_min_gaussian_vth_read = get_data(pattern=snm_min_seevinck_pattern, content=content)
        snm_min_gaussian_vth_read = [abs(1000 * value) for value in snm_min_gaussian_vth_read]

        snm_read = []
        for snm_max_read, snm_min_read in zip(snm_max_gaussian_vth_read, snm_min_gaussian_vth_read):
            if snm_max_read > snm_min_read:
                snm_read.append(snm_min_read)
            else:
                snm_read.append(snm_max_read)

        snm_gaussian_vth_read_file_path = "snm_read_vdd_scaling"
        vdd_scaled_str = str(vdd_scaled).replace('.', '')
        if vdd_scaled == 1:
            vdd_scaled_str = '1'
        snm_gaussian_vth_read_file_path = os.path.join(f'{data}/out/read/snm/vdd_scaling',
                                                       snm_gaussian_vth_read_file_path + '_' + vdd_scaled_str + '.txt')
        with open(snm_gaussian_vth_read_file_path, 'w') as file:
            for val in snm_read:
                file.write(f'{val}\n')

        snm_mean = mean(snm_read)
        snm_stdev = stdev(snm_read)
        snm_gaussian_vth_read_mean.append(snm_mean)
        snm_gaussian_vth_read_stdev.append(snm_stdev)
        snm_read_array.append(snm_read)

        print(f'snm_mean_gaussian_vth_read[{vdd_scaled}V] = {snm_mean} mV', flush=True)
        print(f'snm_stdev_gaussian_vth_read[{vdd_scaled}V] = {snm_stdev} mV', flush=True)

        if col == (cols - 1):
            row = row + 1
            col = 0
        else:
            col = col + 1

    return (
        snm_read_array,
        vdd_gaussian_vth_scaled,
        snm_gaussian_vth_read_mean,
        snm_gaussian_vth_read_stdev
    )


if __name__ == "__main__":
    snm_read_vdd_scaling_analysis()
