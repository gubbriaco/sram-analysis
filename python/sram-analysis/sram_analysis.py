import threading
from matplotlib import pyplot as plt
import numpy as np
import os
from models.ops import save_image
from utils.path import images
from standard_hold_snm_analysis import standard_hold_snm_analysis as standardhold
from standard_read_snm_analysis import standard_read_snm_analysis as standardread
from seevinck_hold_snm_analysis import seevinck_hold_snm_analysis as seevinckhold
from seevinck_read_snm_analysis import seevinck_read_snm_analysis as seevinckread
from graphical_seevinck_comparative_analysis import \
    graphical_seevinck_comparative_analysis as graphicalseevinckcomparative
from snm_hold_vdd_scaling_analysis import snm_hold_vdd_scaling_analysis as snmholdvddscaling
from snm_read_vdd_scaling_analysis import snm_read_vdd_scaling_analysis as snmreadvddscaling
from ileak_hold_vdd_scaling_analysis import ileak_hold_vdd_scaling_analysis as ileakvddscaling
from snm_ileak_vdd_scaling_comparative_analysis import \
    snm_ileak_vdd_scaling_comparative_analysis as snmileakvddscalingcomparative
from drv_analysis import drv_analysis as drvanalysis
from properties import w_ax_pos
from utils.dir import get_values_from_file
from utils.path import data


GENERATE_DATA = True
'''
Boolean constant to choose whether to generate the data via N Gaussian V_TH simulations or not (WARNING: 
Generating the data would take a long time. To display only plots and results set to False, otherwise if you want to 
generate new ones set to True)
'''


print_lock = threading.Lock()
plot_lock = threading.Lock()
graphical_seevinck_comparative_analysis_semaphore = threading.Semaphore(0)
vdd_scaling_semaphore = threading.Semaphore(0)
snm_hold_vdd_scaling_semaphore = threading.Semaphore(0)
snm_read_vdd_scaling_semaphore = threading.Semaphore(0)
ileak_hold_vdd_scaling_semaphore = threading.Semaphore(0)
vdd_scaling_comparative_analysis_semaphore = threading.Semaphore(0)
drv_analysis_semaphore = threading.Semaphore(0)
snm_hold_vdd_scaling_plotting_semaphore = threading.Semaphore(0)
snm_read_vdd_scaling_plotting_semaphore = threading.Semaphore(0)
ileak_hold_vdd_scaling_plotting_semaphore = threading.Semaphore(0)


def t_standard_hold_run():
    global w_ax_standard_hold, snm_standard_hold
    (
        w_ax_standard_hold,
        snm_standard_hold
    ) = standardhold(
        w_ax_pos,
        print_lock,
        plot_lock
    )
    graphical_seevinck_comparative_analysis_semaphore.release()


def t_standard_read_run():
    global w_ax_standard_read, snm_standard_read
    (
        w_ax_standard_read,
        snm_standard_read
    ) = standardread(
        w_ax_pos,
        print_lock,
        plot_lock
    )
    graphical_seevinck_comparative_analysis_semaphore.release()


def t_seevinck_hold_run():
    global w_ax_seevinck_hold, snm_seevinck_hold
    (
        w_ax_seevinck_hold,
        snm_seevinck_hold
    ) = seevinckhold(
        w_ax_pos,
        print_lock,
        plot_lock
    )
    graphical_seevinck_comparative_analysis_semaphore.release()


def t_seevinck_read_run():
    global w_ax_seevinck_read, snm_seevinck_read
    (
        w_ax_seevinck_read,
        snm_seevinck_read
    ) = seevinckread(
        w_ax_pos,
        print_lock,
        plot_lock
    )
    graphical_seevinck_comparative_analysis_semaphore.release()


def t_graphical_seevinck_comparative_analysis_run():
    graphical_seevinck_comparative_analysis_semaphore.acquire()
    graphical_seevinck_comparative_analysis_semaphore.acquire()
    graphical_seevinck_comparative_analysis_semaphore.acquire()
    graphical_seevinck_comparative_analysis_semaphore.acquire()
    '''If four traffic light permits have been acquired then this means that the previous analyses have been 
    completed and the comparative analysis can proceed.'''
    graphicalseevinckcomparative(
        w_ax_standard_hold,
        snm_standard_hold,
        snm_standard_read,
        snm_seevinck_hold,
        snm_seevinck_read,
        plot_lock
    )
    vdd_scaling_semaphore.release()


def t_vdd_scaling_run():
    vdd_scaling_semaphore.acquire()
    snm_hold_vdd_scaling_semaphore.release()
    snm_read_vdd_scaling_semaphore.release()


def t_snm_hold_vdd_scaling_run():
    snm_hold_vdd_scaling_semaphore.acquire()
    global vdd_gaussian_vth_scaled, snm_gaussian_vth_hold_mean, snm_gaussian_vth_hold_stdev
    (
        snm_hold_array,
        vdd_gaussian_vth_scaled,
        snm_gaussian_vth_hold_mean,
        snm_gaussian_vth_hold_stdev
    ) = snmholdvddscaling()
    snm_hold_vdd_scaling_plotting_semaphore.release()
    ileak_hold_vdd_scaling_semaphore.release()
    drv_analysis_semaphore.release()


def t_snm_hold_vdd_scaling_plotting():
    if GENERATE_DATA:
        snm_hold_vdd_scaling_plotting_semaphore.acquire()
    with plot_lock:
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
        fig_hold_snm, axs_hold_snm = plt.subplots(rows, cols, figsize=(16, 6))
        plt.suptitle("Hold Operation DC Simulation VDD Scaling")
        i = 0
        for scaling in np.arange(vdd_start, vdd_stop, -vdd_step):
            if row == rows:
                break
            vdd_scaled = round(scaling, 2)

            snm_hold_file_path = "snm_hold"
            vdd_scaled_str = str(vdd_scaled).replace('.', '')
            if vdd_scaled == 1:
                vdd_scaled_str = '1'
            snm_hold_file_path = os.path.join(f'{data}/out/hold/snm',
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


def t_snm_read_vdd_scaling_run():
    snm_read_vdd_scaling_semaphore.acquire()
    global vdd_gaussian_vth_scaled, snm_gaussian_vth_read_mean, snm_gaussian_vth_read_stdev
    (
        snm_read_array,
        vdd_gaussian_vth_scaled,
        snm_gaussian_vth_read_mean,
        snm_gaussian_vth_read_stdev
    ) = snmreadvddscaling()
    snm_read_vdd_scaling_plotting_semaphore.release()
    ileak_hold_vdd_scaling_semaphore.release()


def t_snm_read_vdd_scaling_plotting():
    if GENERATE_DATA:
        snm_read_vdd_scaling_plotting_semaphore.acquire()
    with plot_lock:
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
        fig_read_snm, axs_read_snm = plt.subplots(rows, cols, figsize=(16, 6))
        plt.suptitle("Read Operation DC Simulation VDD Scaling")
        i = 0
        for scaling in np.arange(vdd_start, vdd_stop, -vdd_step):
            if row == rows:
                break
            vdd_scaled = round(scaling, 2)

            snm_read_file_path = "snm_read"
            vdd_scaled_str = str(vdd_scaled).replace('.', '')
            if vdd_scaled == 1:
                vdd_scaled_str = '1'
            snm_read_file_path = os.path.join(f'{data}/out/read/snm',
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


def t_ileak_hold_vdd_scaling_run():
    ileak_hold_vdd_scaling_semaphore.acquire()
    ileak_hold_vdd_scaling_semaphore.acquire()
    global vdd_standard_transient_scaled, i_leak_standard_transient_hold_mean, i_leak_standard_transient_hold_stdev
    (
        i_leak_hold_array,
        vdd_standard_transient_scaled,
        i_leak_standard_transient_hold_mean,
        i_leak_standard_transient_hold_stdev
    ) = ileakvddscaling()
    ileak_hold_vdd_scaling_plotting_semaphore.release()
    vdd_scaling_comparative_analysis_semaphore.release()


def t_ileak_hold_vdd_scaling_plotting():
    if GENERATE_DATA:
        ileak_hold_vdd_scaling_plotting_semaphore.acquire()
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
    with plot_lock:
        fig_ileak_hold, axs_ileak_hold = plt.subplots(rows, cols, figsize=(16, 6))
        plt.suptitle("I Leak Hold Operation DC Simulation VDD Scaling")
        i = 0
        for scaling in np.arange(vdd_start, vdd_stop, -vdd_step):
            if row == rows:
                break
            vdd_scaled = round(scaling, 2)

            ileak_hold_file_path = "ileak_hold"
            vdd_scaled_str = str(vdd_scaled).replace('.', '')
            if vdd_scaled == 1:
                vdd_scaled_str = '1'
            ileak_hold_file_path = os.path.join(f'{data}/out/hold/ileak',
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


def t_vdd_scaling_plotting_run():
    t_snm_hold_vdd_scaling_plotting()
    t_snm_read_vdd_scaling_plotting()
    t_ileak_hold_vdd_scaling_plotting()


def t_comparative_analysis_vdd_scaling_run():
    if GENERATE_DATA:
        vdd_scaling_comparative_analysis_semaphore.acquire()
    snmileakvddscalingcomparative(
        plot_lock
    )


def t_drv_analysis_run():
    if GENERATE_DATA:
        drv_analysis_semaphore.acquire()
    drvanalysis(
        plot_lock
    )


if __name__ == "__main__":

    w_ax_standard_hold, snm_standard_hold = None, None
    w_ax_standard_read, snm_standard_read = None, None
    w_ax_seevinck_hold, snm_seevinck_hold = None, None
    w_ax_seevinck_read, snm_seevinck_read = None, None
    vdd_gaussian_vth_scaled = None
    snm_gaussian_vth_hold_mean, snm_gaussian_vth_hold_stdev = None, None
    snm_gaussian_vth_read_mean, snm_gaussian_vth_read_stdev = None, None
    vdd_standard_transient_scaled = None
    i_leak_standard_transient_hold_mean, i_leak_standard_transient_hold_stdev = None, None

    t_standard_hold = threading.Thread(target=t_standard_hold_run)
    t_standard_read = threading.Thread(target=t_standard_read_run)
    t_seevinck_hold = threading.Thread(target=t_seevinck_hold_run)
    t_seevinck_read = threading.Thread(target=t_seevinck_read_run)
    t_graphical_seevinck_comparative = threading.Thread(target=t_graphical_seevinck_comparative_analysis_run)
    t_vdd_scaling = threading.Thread(target=t_vdd_scaling_run)

    t_snm_hold_vdd_scaling = threading.Thread(target=t_snm_hold_vdd_scaling_run)
    t_snm_read_vdd_scaling = threading.Thread(target=t_snm_read_vdd_scaling_run)
    t_ileak_hold_vdd_scaling = threading.Thread(target=t_ileak_hold_vdd_scaling_run)

    t_vdd_scaling_plotting = threading.Thread(target=t_vdd_scaling_plotting_run)

    t_vdd_scaling_comparative = threading.Thread(target=t_comparative_analysis_vdd_scaling_run)
    t_drv_analysis = threading.Thread(target=t_drv_analysis_run)

    t_standard_hold.start()
    t_standard_read.start()
    t_seevinck_hold.start()
    t_seevinck_read.start()
    t_graphical_seevinck_comparative.start()
    t_vdd_scaling.start()

    if GENERATE_DATA:
        t_snm_hold_vdd_scaling.start()
        t_snm_read_vdd_scaling.start()
        t_ileak_hold_vdd_scaling.start()

    t_vdd_scaling_plotting.start()
    t_vdd_scaling_comparative.start()
    t_drv_analysis.start()

    t_standard_hold.join()
    t_standard_read.join()
    t_seevinck_hold.join()
    t_seevinck_read.join()
    t_graphical_seevinck_comparative.join()
    t_vdd_scaling.join()
    t_vdd_scaling_plotting.join()

    if GENERATE_DATA:
        t_snm_hold_vdd_scaling.join()
        t_snm_read_vdd_scaling.join()
        t_ileak_hold_vdd_scaling.join()

    t_vdd_scaling_comparative.join()
    t_drv_analysis.join()
