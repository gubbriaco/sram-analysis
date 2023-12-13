from properties import vwl_read, vbl_read, vblneg_read, w_ax_range
from properties import vdd_seevinck
from properties import vsweep_seevinck
from properties import rit_models, dc_vsweep_seevinck, snm_max, snm_min, w_ax_step_param_seevinck, save_w_ax_seevinck
from utils.path import ltspice, schematics, images
from utils.patterns import w_ax_seevinck_pattern, snm_max_seevinck_pattern, snm_min_seevinck_pattern
from models.snm import graphical_processing, rotate_points, seevinck_processing, RequestPlot
from models.ops import save_image, get_data, __init_model__, CircuitType, OperationType, RequestPlotSchematic
from matplotlib import pyplot as plt
import os
from properties import w_ax_pos


def seevinck_read_snm_analysis():
    (
        steps,
        vsweep_seevinck_read,
        i_leaks_seevinck_read,
        v_1_seevinck_read,
        v_2_seevinck_read,
        v_dd_seevinck_read,
        v_wl_seevinck_read,
        v_bl_seevinck_read,
        v_blneg_seevinck_read,
        seevinck_read_log
    ) = __init_model__(
        operation_type=OperationType.READ,
        circuit_type=CircuitType.SEEVINCK,
        asc_file_path=os.path.join(ltspice, "seevinck/read/seevinck_read.asc"),
        schematic_image_path=os.path.join(schematics, "seevinck.png"),
        request_plot_schematic=RequestPlotSchematic.TRUE,
        vdd=vdd_seevinck,
        vsweep=vsweep_seevinck,
        vwl=vwl_read,
        vbl=vbl_read,
        vblneg=vblneg_read,
        params=[rit_models, dc_vsweep_seevinck, snm_max(0.655), snm_min(0.655), w_ax_step_param_seevinck,
                save_w_ax_seevinck]
    )

    plt.figure(figsize=(16, 4))
    vq_seevinck_read = []
    vqneg_seevinck_read = []
    vq_vqneg_seevinck_read = []
    x_seevinck_read = []
    for step in range(len(steps)):
        vq = v_1_seevinck_read.get_wave(step)
        vqneg = v_2_seevinck_read.get_wave(step)
        vq_minus_vqneg = vq - vqneg
        vq_seevinck_read.append(vq)
        vqneg_seevinck_read.append(vqneg)
        vq_vqneg_seevinck_read.append(vq_minus_vqneg)
        x = vsweep_seevinck_read.get_wave(step)
        x_seevinck_read.append(x)
        plt.plot(x, vq, label=steps[step], color='blue')
        plt.plot(x, vqneg, label=steps[step], color='green')
        plt.plot(x, vq_minus_vqneg, label=steps[step], color='red')
    plt.title("V(v1), V(v2), V(v1)-V(v2) Curves Read Phase")
    plt.xlabel("steps");
    plt.ylabel("Read Voltages")
    plt.legend(["V(v1)", "V(v2)", "V(v1)-V(v2)"])
    save_image(image_path=os.path.join(images, "seevinck_read_simulation.png"), plt=plt)
    plt.show()

    seevinck_read_log_file_path = f"./{seevinck_read_log}"
    with open(seevinck_read_log_file_path, "r") as file:
        content = file.read()

    w_ax_seevinck_read = get_data(pattern=w_ax_seevinck_pattern, content=content)

    snm_max_seevinck_read = get_data(pattern=snm_max_seevinck_pattern, content=content)
    snm_max_seevinck_read = [1000 * value for value in snm_max_seevinck_read]

    snm_min_seevinck_read = get_data(pattern=snm_min_seevinck_pattern, content=content)
    snm_min_seevinck_read = [abs(1000 * value) for value in snm_min_seevinck_read]

    print("{:<20} {:<30} {:<30}".format("w_ax", "SNM_MAX(READ)", "SNM_MIN(READ)"))
    for w, smax, smin in zip(w_ax_seevinck_read, snm_max_seevinck_read, snm_min_seevinck_read):
        print("{:<20} {:<30} {:<30}".format(f'{w} u', f'{smax} mV', f'{smin} mV'))

    snm_seevinck_read = []
    for snm_max_read, snm_min_read in zip(snm_max_seevinck_read, snm_min_seevinck_read):
        if snm_max_read > snm_min_read:
            snm_seevinck_read.append(snm_min_read)
        else:
            snm_seevinck_read.append(snm_max_read)

    print(f'snm_seevinck_read[{w_ax_seevinck_read[w_ax_pos]} u] = {snm_seevinck_read[w_ax_pos]}')

    plt.figure(figsize=(16, 4))
    plt.plot(w_ax_seevinck_read, snm_max_seevinck_read)
    plt.plot(w_ax_seevinck_read, snm_min_seevinck_read)
    plt.xlabel("w_ax");
    plt.ylabel("snm")
    plt.legend(["snm_max", "snm_min"])
    plt.title("SNM SEEVINCK READ GENERATED BY LTSPICE")
    save_image(image_path=os.path.join(images, "snm_seevinck_read_generated_by_ltspice.png"), plt=plt)
    plt.show()


    fig, axs = plt.subplots(1, 3, figsize=(16, 6))

    snm_seevinck_read_seevinck_processing = []
    snm_seevinck_read_standard_processing = []

    for w in range(w_ax_range):

        # vq-vqneg rotating
        for vq_array, vqneg_array in zip(vq_seevinck_read, vqneg_seevinck_read):
            vq_vqneg_array = vq_array - vqneg_array
            x_diff, y_diff = rotate_points(x=x_seevinck_read[w], y=vq_vqneg_array, angle_degrees=-45)
            axs[0].plot(x_diff, y_diff, color='red')
        axs[0].set_title("V(v1)-V(v2) Curve Read Phase")
        axs[0].legend(["V(v1) - V(v2)"])

        # vq and vqneg rotating
        xsread1, ysread1 = rotate_points(x=x_seevinck_read[w], y=vq_seevinck_read[w], angle_degrees=-45)
        xsread2, ysread2 = rotate_points(x=x_seevinck_read[w], y=vqneg_seevinck_read[w], angle_degrees=-45)
        axs[1].plot(xsread1, ysread1, color='blue')
        axs[1].plot(xsread2, ysread2, color='green')

        # seevinck processing
        snm_seevinck_read_seevinck_processing_value = seevinck_processing(
            x_v1_minus_v2=x_seevinck_read[w],
            v1_minus_v2=vq_vqneg_seevinck_read[w],
            ax=axs[1],
            request_text_plot=RequestPlot.FALSE
        )
        snm_seevinck_read_seevinck_processing.append(snm_seevinck_read_seevinck_processing_value)

        # graphical-processing
        snm_seevinck_read_standard_processing_value = graphical_processing(
            x_vq=xsread1,
            vq=ysread1,
            x_vqneg=xsread2,
            vqneg=ysread2,
            ax=axs[1],
            request_text_plot=RequestPlot.FALSE
        )
        snm_seevinck_read_standard_processing.append(snm_seevinck_read_standard_processing_value)

    axs[1].set_title("V(v1)-V(v2) Curve Read Phase and SNM")
    axs[1].grid()

    # vq-vqneg rotating
    for vq_array, vqneg_array in zip(vq_seevinck_read, vqneg_seevinck_read):
        vq_vqneg_array = vq_array - vqneg_array
        x_diff, y_diff = rotate_points(x=x_seevinck_read[w_ax_pos], y=vq_vqneg_array, angle_degrees=-45)
        axs[0].plot(x_diff, y_diff, color='red')
    axs[2].set_title("V(v1)-V(v2) Curve Read Phase")
    axs[2].legend(["V(v1) - V(v2)"])

    # vq and vqneg rotating
    xsread1, ysread1 = rotate_points(x=x_seevinck_read[w_ax_pos], y=vq_seevinck_read[w_ax_pos], angle_degrees=-45)
    xsread2, ysread2 = rotate_points(x=x_seevinck_read[w_ax_pos], y=vqneg_seevinck_read[w_ax_pos],
                                     angle_degrees=-45)
    axs[2].plot(xsread1, ysread1, color='blue')
    axs[2].plot(xsread2, ysread2, color='green')

    # seevinck processing
    snm_seevinck_read_seevinck_processing_w_ax = seevinck_processing(
        x_v1_minus_v2=x_seevinck_read[w_ax_pos],
        v1_minus_v2=vq_vqneg_seevinck_read[w_ax_pos],
        ax=axs[2],
        request_text_plot=RequestPlot.TRUE
    )

    # graphical-processing
    snm_seevinck_read_standard_processing_w_ax = graphical_processing(
        x_vq=xsread1,
        vq=ysread1,
        x_vqneg=xsread2,
        vqneg=ysread2,
        ax=axs[2],
        request_text_plot=RequestPlot.TRUE
    )

    axs[2].set_title("V(v1)-V(v2) Curve Read Phase and SNM")
    axs[2].grid()

    print("{:<30} {:<30} {:<30}".format("w_ax", "snm(read)_seevinck", "snm(read)_graphical"))
    for w, snm_read_seevinck, snm_read_graphical in zip(w_ax_seevinck_read, snm_seevinck_read_seevinck_processing,
                                                        snm_seevinck_read_standard_processing):
        print("{:<30} {:<30} {:<30}".format(w, snm_read_seevinck, snm_read_graphical))

    save_image(image_path=os.path.join(images, "v1_minus_v2_seevinck_read.png"), plt=plt)
    plt.show()

    return (
        w_ax_seevinck_read,
        snm_seevinck_read
    )


if __name__ == "__main__":
    seevinck_read_snm_analysis()
