import threading
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

# w_ax pick
w_ax_pos = 1

print_lock = threading.Lock()
plot_lock = threading.Lock()
graphical_seevinck_comparative_analysis_semaphore = threading.Semaphore(0)
vdd_scaling = threading.Semaphore(0)
snm_hold_vdd_scaling = threading.Semaphore(0)
snm_read_vdd_scaling = threading.Semaphore(0)
ileak_hold_vdd_scaling = threading.Semaphore(0)
vdd_scaling_comparative_analysis_semaphore = threading.Semaphore(0)


def t_standard_hold_run():
    global w_ax_standard_hold, snm_standard_hold
    w_ax_standard_hold, snm_standard_hold = standardhold(w_ax_pos, print_lock, plot_lock)
    graphical_seevinck_comparative_analysis_semaphore.release()


def t_standard_read_run():
    global w_ax_standard_read, snm_standard_read
    w_ax_standard_read, snm_standard_read = standardread(w_ax_pos, print_lock, plot_lock)
    graphical_seevinck_comparative_analysis_semaphore.release()


def t_seevinck_hold_run():
    global w_ax_seevinck_hold, snm_seevinck_hold
    w_ax_seevinck_hold, snm_seevinck_hold = seevinckhold(w_ax_pos, print_lock, plot_lock)
    graphical_seevinck_comparative_analysis_semaphore.release()


def t_seevinck_read_run():
    global w_ax_seevinck_read, snm_seevinck_read
    w_ax_seevinck_read, snm_seevinck_read = seevinckread(w_ax_pos, print_lock, plot_lock)
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
    vdd_scaling.release()


def t_vdd_scaling_run():
    vdd_scaling.acquire()
    snm_hold_vdd_scaling.release()
    snm_read_vdd_scaling.release()


def t_snm_hold_vdd_scaling_run():
    snm_hold_vdd_scaling.acquire()
    global vdd_gaussian_vth_scaled, snm_gaussian_vth_hold_mean, snm_gaussian_vth_hold_stdev
    vdd_gaussian_vth_scaled, snm_gaussian_vth_hold_mean, snm_gaussian_vth_hold_stdev = snmholdvddscaling()
    ileak_hold_vdd_scaling.release()


def t_snm_read_vdd_scaling_run():
    snm_read_vdd_scaling.acquire()
    global vdd_gaussian_vth_scaled, snm_gaussian_vth_read_mean, snm_gaussian_vth_read_stdev
    vdd_gaussian_vth_scaled, snm_gaussian_vth_read_mean, snm_gaussian_vth_read_stdev = snmreadvddscaling()
    ileak_hold_vdd_scaling.release()


def t_ileak_hold_vdd_scaling_run():
    ileak_hold_vdd_scaling.acquire()
    ileak_hold_vdd_scaling.acquire()
    global vdd_standard_transient_scaled, i_leak_standard_transient_hold_mean
    vdd_standard_transient_scaled, i_leak_standard_transient_hold_mean = ileakvddscaling(
        snm_gaussian_vth_hold_mean,
        snm_gaussian_vth_hold_stdev,
        snm_gaussian_vth_read_mean,
        snm_gaussian_vth_read_stdev
    )
    vdd_scaling_comparative_analysis_semaphore.release()


def t_comparative_analysis_vdd_scaling_run():
    vdd_scaling_comparative_analysis_semaphore.acquire()
    snmileakvddscalingcomparative(
        vdd_gaussian_vth_scaled,
        snm_gaussian_vth_hold_mean,
        snm_gaussian_vth_read_mean,
        vdd_standard_transient_scaled,
        i_leak_standard_transient_hold_mean
    )


if __name__ == "__main__":

    w_ax_standard_hold, snm_standard_hold = None, None
    w_ax_standard_read, snm_standard_read = None, None
    w_ax_seevinck_hold, snm_seevinck_hold = None, None
    w_ax_seevinck_read, snm_seevinck_read = None, None
    vdd_gaussian_vth_scaled = None
    snm_gaussian_vth_hold_mean, snm_gaussian_vth_hold_stdev = None, None
    snm_gaussian_vth_read_mean, snm_gaussian_vth_read_stdev = None, None
    vdd_standard_transient_scaled, i_leak_standard_transient_hold_mean = None, None

    t_standard_hold = threading.Thread(target=t_standard_hold_run)
    t_standard_read = threading.Thread(target=t_standard_read_run)
    t_seevinck_hold = threading.Thread(target=t_seevinck_hold_run)
    t_seevinck_read = threading.Thread(target=t_seevinck_read_run)
    t_graphical_seevinck_comparative = threading.Thread(target=t_graphical_seevinck_comparative_analysis_run)
    t_vdd_scaling = threading.Thread(target=t_vdd_scaling_run)
    t_snm_hold_vdd_scaling = threading.Thread(target=t_snm_hold_vdd_scaling_run)
    t_snm_read_vdd_scaling = threading.Thread(target=t_snm_read_vdd_scaling_run)
    t_ileak_hold_vdd_scaling = threading.Thread(target=t_ileak_hold_vdd_scaling_run)
    t_vdd_scaling_comparative = threading.Thread(target=t_comparative_analysis_vdd_scaling_run)

    t_standard_hold.start()
    t_standard_read.start()
    t_seevinck_hold.start()
    t_seevinck_read.start()
    t_graphical_seevinck_comparative.start()
    t_vdd_scaling.start()
    t_snm_hold_vdd_scaling.start()
    t_snm_read_vdd_scaling.start()
    t_ileak_hold_vdd_scaling.start()
    t_vdd_scaling_comparative.start()

    t_standard_hold.join()
    t_standard_read.join()
    t_seevinck_hold.join()
    t_seevinck_read.join()
    t_graphical_seevinck_comparative.join()
    t_vdd_scaling.join()
    t_snm_hold_vdd_scaling.join()
    t_snm_read_vdd_scaling.join()
    t_ileak_hold_vdd_scaling.join()
    t_vdd_scaling_comparative.join()
