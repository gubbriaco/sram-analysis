from properties import vwl_hold, vbl_hold, vblneg_hold, w_ax_range
from properties import vdd_standard
from properties import vsweep_standard
from properties import rit_models, dc_vsweep_standard, w_ax_step_param_standard, save_w_ax_standard
from utils.path import ltspice, schematics, images
from utils.patterns import w_ax_standard_pattern
from models.snm import graphical_processing, RequestPlot
from models.ops import save_image, get_data, __init_model__, CircuitType, OperationType, RequestPlotSchematic
from matplotlib import pyplot as plt
import os
from properties import w_ax_pos


def standard_hold_snm_analysis():
    (
        steps,
        vsweep_standard_hold,
        i_leaks_standard_hold,
        v_q_standard_hold,
        v_q_neg_standard_hold,
        v_dd_standard_hold,
        v_wl_standard_hold,
        v_bl_standard_hold,
        v_blneg_standard_hold,
        standard_hold_log
    ) = __init_model__(
        operation_type=OperationType.HOLD,
        circuit_type=CircuitType.STANDARD,
        asc_file_path=os.path.join(ltspice, "standard/hold/standard_hold.asc"),
        schematic_image_path=os.path.join(schematics, "standard.png"),
        request_plot_schematic=RequestPlotSchematic.TRUE,
        vdd=vdd_standard,
        vsweep=vsweep_standard,
        vwl=vwl_hold,
        vbl=vbl_hold,
        vblneg=vblneg_hold,
        params=[rit_models, dc_vsweep_standard, w_ax_step_param_standard, save_w_ax_standard]
    )


    plt.figure(figsize=(16, 4))
    for step in range(len(steps)):
        x = vsweep_standard_hold.get_wave(step)
        vq = v_q_standard_hold.get_wave(step)
        plt.plot(x, vq, label=steps[step], color='blue')
    plt.title("V(q) Curve Hold Phase")
    plt.legend(["V(q)"])
    save_image(image_path=os.path.join(images, "standard_hold_simulation.png"), plt=plt)
    plt.show()

    standard_hold_log_file_path = f"./{standard_hold_log}"

    with open(standard_hold_log_file_path, "r") as file:
        content = file.read()

    w_ax_standard_hold = get_data(pattern=w_ax_standard_pattern, content=content)
    print(f'w_ax_standard_hold = {w_ax_standard_hold}')

    plt.figure(figsize=(16, 4))
    plt.legend(['w_ax_standard_hold'])
    plt.plot(w_ax_standard_hold, label='w_ax_standard_hold')
    plt.ylabel('w_min_pmos_hold');
    plt.xlabel('steps');
    plt.title('W AX Trend Hold Phase')


    fig, axs = plt.subplots(1, 3, figsize=(16, 5))
    x_vq_standard_hold = []
    vq_standard_hold = []
    x_vqneg_standard_hold = []
    vqneg_standard_hold = []
    for step in range(len(steps)):
        x = vsweep_standard_hold.get_wave(step)
        vq = v_q_standard_hold.get_wave(step)
        x_vq_standard_hold.append(x)
        vq_standard_hold.append(vq)
        x_vqneg_standard_hold.append(vq)
        vqneg_standard_hold.append(x)
        axs[0].plot(x, vq, label=steps[step], color='blue')
        axs[0].plot(vq, x, label=steps[step], color='green')
    axs[0].set_title("Butterfly Curve Hold Phase")
    axs[0].legend(["V(q)", "V(q_neg)"])
    axs[0].grid()

    # graphical method
    print("{:<30} {:<30}".format("w_ax", "SNM(HOLD)"))
    snm_standard_hold = []
    for w in range(w_ax_range):
        snm_standard_hold_value = graphical_processing(
            x_vq=x_vq_standard_hold[w],
            vq=vq_standard_hold[w],
            x_vqneg=x_vqneg_standard_hold[w],
            vqneg=vqneg_standard_hold[w],
            ax=axs[1],
            request_text_plot=RequestPlot.FALSE
        )
        snm_standard_hold.append(snm_standard_hold_value)
        print("{:<30} {:<30}".format(w_ax_standard_hold[w], snm_standard_hold_value))

    snm_standard_hold_w_ax = graphical_processing(
        x_vq=x_vq_standard_hold[w_ax_pos],
        vq=vq_standard_hold[w_ax_pos],
        x_vqneg=x_vqneg_standard_hold[w_ax_pos],
        vqneg=vqneg_standard_hold[w_ax_pos],
        ax=axs[2],
        request_text_plot=RequestPlot.TRUE
    )
    print(f'snm_standard_hold[w_ax_pos={w_ax_standard_hold[w_ax_pos]} u] = {snm_standard_hold_w_ax}')

    save_image(image_path=os.path.join(images, "butterfly_curve_standard_hold.png"), plt=plt)
    plt.show()


    fig_standard_hold = plt.figure(figsize=(16, 4))
    plt.plot(w_ax_standard_hold, snm_standard_hold)
    plt.ylabel("snm")
    plt.xlabel("w_ax")
    plt.title("SNM HOLD GENERATED BY GRAPHICAL METHOD")
    plt.grid()
    save_image(image_path=os.path.join(images, "snm_standard_hold.png"), plt=plt)
    plt.show()

    return (
        w_ax_standard_hold,
        snm_standard_hold
    )


if __name__ == "__main__":
    standard_hold_snm_analysis()
