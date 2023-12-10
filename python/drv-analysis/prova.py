import threading
from properties import vwl_hold, vbl_hold, vblneg_hold, vwl_read, vbl_read, vblneg_read, w_ax_range
from properties import vdd_standard, vdd_seevinck
from properties import vsweep_standard, vsweep_seevinck, vsweep_gaussian_vth
from properties import rit_models, dc_vsweep_standard, w_ax_step_param_standard, save_w_ax_standard, dc_vsweep_seevinck, \
    snm_max, snm_min, w_ax_step_param_seevinck, save_w_ax_seevinck, rit_models_montecarlo, dc_vsweep_gaussian_vth, \
    step_param_run_gaussian_vth
from properties import vdd_standard_transient, tran_standard, vbl_hold_transient, vblneg_hold_transient, \
    vsweep_standard_transient, step_param_run_standard_transient
from utils.path import ltspice, schematics, images, data
from utils.patterns import w_ax_standard_pattern, w_ax_seevinck_pattern, snm_max_seevinck_pattern, \
    snm_min_seevinck_pattern
from models.snm import graphical_processing, rotate_points, seevinck_processing, RequestPlot
from models.ops import save_image, get_data, __init_model__, CircuitType, OperationType, RequestPlotSchematic
from matplotlib import pyplot as plt
import os
from statistics import mean, stdev
from IPython.display import Image, display
import numpy as np

print_lock = threading.Lock()








if __name__ == "__main__":
    t1 = threading.Thread(target=snm_hold_exe)
    t2 = threading.Thread(target=snm_read_exe)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("Esecuzione completata.")
