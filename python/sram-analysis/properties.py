from utils.path import rit_models_for_ltspice_file_path, rit_models_for_ltspice_montecarlo_file_path

########################################################################################################################
########################################################################################################################
# COMMON PARAMETERS

# w-ax pick
w_ax_pos = 1

# rit-models
rit_models = f'.inc {rit_models_for_ltspice_file_path}'

# rit-models-gaussian
rit_models_montecarlo = f'.inc {rit_models_for_ltspice_montecarlo_file_path}'

# vwl, vbl, vblneg
vwl_hold = '0'
vbl_hold = '1'
vblneg_hold = '1'

vwl_read = '1'
vbl_read = '1'
vblneg_read = '1'

# range-w_ax
w_ax_start = 0.12
w_ax_stop = 0.24
w_ax_range = int(((w_ax_stop - w_ax_start) * 100) + 1)

########################################################################################################################
########################################################################################################################


########################################################################################################################
# SNM STANDARD

# AX
l_ax_standard = '0.12u'
w_ax_start_standard = f'{w_ax_start}u'
w_ax_stop_standard = f'{w_ax_stop}u'
w_ax_step_standard = '0.01u'
w_ax_step_param_standard = (
    f'.step param w_ax '
    f'{w_ax_start_standard} '
    f'{w_ax_stop_standard} '
    f'{w_ax_step_standard}'
)

# save w_ax
save_w_ax_standard = '.meas w_ax_values param w_ax'

# Q transistor
l_pmos_q_standard = '0.12u'
w_pmos_q_standard = '0.12u'
l_nmos_q_standard = '0.12u'
w_nmos_q_standard = '0.48u'

# Q neg transistor
l_pmos_q_neg_standard = '0.12u'
w_pmos_q_neg_standard = '0.12u'
l_nmos_q_neg_standard = '0.12u'
w_nmos_q_neg_standard = '0.48u'

# voltage
vdd_standard = '1'
vsweep_standard = '1'

# dc Vsweep
dc_vsweep_start_standard = 0
dc_vsweep_stop_standard = 1
dc_vsweep_step_standard = 0.01
dc_vsweep_standard = (
    f'.dc Vsweep '
    f'{dc_vsweep_start_standard} '
    f'{dc_vsweep_stop_standard} '
    f'{dc_vsweep_step_standard}'
)

########################################################################################################################
# SNM SEEVINCK

# snm-max and snm-min
v_sweep_seevinck = 0.655


def snm_max(v_sweep):
    return f'.measure dc snm_max MAX({v_sweep}*v(V1)-{v_sweep}*v(V2))'


def snm_min(v_sweep):
    return f'.measure dc snm_min MIN({v_sweep}*v(V1)-{v_sweep}*v(V2))'


# AX
l_ax_seevinck = '0.12u'
w_ax_start_seevinck = f'{w_ax_start}u'
w_ax_stop_seevinck = f'{w_ax_stop}u'
w_ax_step_seevinck = '0.01u'
w_ax_step_param_seevinck = (
    f'.step param w_ax '
    f'{w_ax_start_seevinck} '
    f'{w_ax_stop_seevinck} '
    f'{w_ax_step_seevinck}'
)

# save w_ax
save_w_ax_seevinck = '.meas w_ax_values param w_ax'

# Q transistor
l_pmos_q_seevinck = '0.12u'
w_pmos_q_seevinck = '0.12u'
l_nmos_q_seevinck = '0.12u'
w_nmos_q_seevinck = '0.48u'

# Q neg transistor
l_pmos_q_neg_seevinck = '0.12u'
w_pmos_q_neg_seevinck = '0.12u'
l_nmos_q_neg_seevinck = '0.12u'
w_nmos_q_neg_seevinck = '0.48u'

# voltage
vdd_seevinck = '1'
vsweep_seevinck = '1'

# dc Vsweep
dc_vsweep_start_seevinck = -v_sweep_seevinck
dc_vsweep_stop_seevinck = v_sweep_seevinck
dc_vsweep_step_seevinck = 0.01
dc_vsweep_seevinck = f'.dc Vsweep {dc_vsweep_start_seevinck} {dc_vsweep_stop_seevinck} {dc_vsweep_step_seevinck}'

# E1 E2 E3 E4 E5 E6 E7 E8
e1_seevinck = '0.707'
e2_seevinck = '0.707'
e3_seevinck = '1'
e4_seevinck = '1.41'
e5_seevinck = '-1'
e6_seevinck = '1.41'
e7_seevinck = '0.707'
e8_seevinck = '-0.707'


########################################################################################################################
# GAUSSIAN-VTH

# AX
l_ax_gaussian_vth = '0.12u'
w_ax_gaussian_vth = '0.13u'
w_ax_start_gaussian_vth = f'{w_ax_start}u'
w_ax_stop_gaussian_vth = f'{w_ax_stop}u'
w_ax_step_gaussian_vth = '0.01u'
w_ax_step_param_gaussian_vth = f'.step param w_ax {w_ax_start_seevinck} {w_ax_stop_seevinck} {w_ax_step_seevinck}'

# save w_ax
save_w_ax_gaussian_vth = '.meas w_ax_values param w_ax'

# Q transistor
l_pmos_q_gaussian_vth = '0.12u'
w_pmos_q_gaussian_vth = '0.12u'
l_nmos_q_gaussian_vth = '0.12u'
w_nmos_q_gaussian_vth = '0.48u'

# Q neg transistor
l_pmos_q_neg_gaussian_vth = '0.12u'
w_pmos_q_neg_gaussian_vth = '0.12u'
l_nmos_q_neg_gaussian_vth = '0.12u'
w_nmos_q_neg_gaussian_vth = '0.48u'

# voltage
vdd_gaussian_vth = '1'
vsweep_gaussian_vth = '1'


def dc_vsweep_gaussian_vth(dc_vsweep_start_gaussian_vth, dc_vsweep_stop_gaussian_vth, dc_vsweep_step_gaussian_vth):
    return f'.dc Vsweep {dc_vsweep_start_gaussian_vth} {dc_vsweep_stop_gaussian_vth} {dc_vsweep_step_gaussian_vth}'


tran_gaussian_vth = ".tran 0 50n 0"

# E1 E2 E3 E4 E5 E6 E7 E8
e1_gaussian_vth = '0.707'
e2_gaussian_vth = '0.707'
e3_gaussian_vth = '1'
e4_gaussian_vth = '1.41'
e5_gaussian_vth = '-1'
e6_gaussian_vth = '1.41'
e7_gaussian_vth = '0.707'
e8_gaussian_vth = '-0.707'

# step param run
step_param_run_gaussian_vth_start = 1
step_param_run_gaussian_vth_stop = 400
step_param_run_gaussian_vth_step = 1
step_param_run_gaussian_vth = (
    f'.step param run '
    f'{step_param_run_gaussian_vth_start} '
    f'{step_param_run_gaussian_vth_stop} '
    f'{step_param_run_gaussian_vth_step}'
)

########################################################################################################################
# I LEAK STANDARD DC

# AX
l_ax_standard_ileak = '0.12u'
w_ax_standard_ileak = '0.13u'
w_ax_start_standard_ileak = f'{w_ax_start}u'
w_ax_stop_standard_ileak = f'{w_ax_stop}u'
w_ax_step_standard_ileak = '0.01u'
w_ax_step_param_standard_ileak = (
    f'.step param w_ax '
    f'{w_ax_start_standard_ileak} '
    f'{w_ax_stop_standard_ileak} '
    f'{w_ax_step_standard_ileak}'
)

# Q transistor
l_pmos_q_standard_ileak = '0.12u'
w_pmos_q_standard_ileak = '0.12u'
l_nmos_q_standard_ileak = '0.12u'
w_nmos_q_standard_ileak = '0.48u'

# Q neg transistor
l_pmos_q_neg_standard_ileak = '0.12u'
w_pmos_q_neg_standard_ileak = '0.12u'
l_nmos_q_neg_standard_ileak = '0.12u'
w_nmos_q_neg_standard_ileak = '0.48u'

# vdd
vdd_standard_ileak = '1'
# vsweep
vsweep_standard_ileak = '1'

# tran
tran_standard_range = '150n'
tran_standard = f'.tran {tran_standard_range}'

# vbl_hold ileak
vbl_hold_ileak_vinitial = vdd_standard_ileak
vbl_hold_ileak_von = '0'
vbl_hold_ileak_tdelay = '100p'
vbl_hold_ileak_trise = '10p'
vbl_hold_ileak_tfall = '10p'
vbl_hold_ileak_ton = '490p'
vbl_hold_ileak_tperiod = '1n'
vbl_hold_ileak = (
    f'PULSE('
    f'{vbl_hold_ileak_vinitial} '
    f'{vbl_hold_ileak_von} '
    f'{vbl_hold_ileak_tdelay} '
    f'{vbl_hold_ileak_trise} '
    f'{vbl_hold_ileak_tfall} '
    f'{vbl_hold_ileak_ton} '
    f'{vbl_hold_ileak_tperiod}'
    f')'
)

# vbl_neg_hold ileak
vblneg_hold_ileak_vinitial = vdd_standard_ileak
vblneg_hold_ileak_von = '0'
vblneg_hold_ileak_tdelay = '100p'
vblneg_hold_ileak_trise = '10p'
vblneg_hold_ileak_tfall = '10p'
vblneg_hold_ileak_ton = '490p'
vblneg_hold_ileak_tperiod = '1n'
vblneg_hold_ileak = (
    f'PULSE('
    f'{vblneg_hold_ileak_vinitial} '
    f'{vblneg_hold_ileak_von} '
    f'{vblneg_hold_ileak_tdelay} '
    f'{vblneg_hold_ileak_trise} '
    f'{vblneg_hold_ileak_tfall} '
    f'{vblneg_hold_ileak_ton} '
    f'{vblneg_hold_ileak_tperiod}'
    f')'
)

# step param run
step_param_run_standard_ileak_start = 1
step_param_run_standard_ileak_stop = 400
step_param_run_standard_ileak_step = 1
step_param_run_standard_ileak = (
    f'.step param run '
    f'{step_param_run_standard_ileak_start} '
    f'{step_param_run_standard_ileak_stop} '
    f'{step_param_run_standard_ileak_step}'
)
