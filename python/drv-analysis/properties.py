from utils.path import rit_models_for_ltspice_file_path, rit_models_for_ltspice_montecarlo_file_path


# rit-models
rit_models = f'.inc {rit_models_for_ltspice_file_path}'

# rit-models-gaussian
rit_models_montecarlo = f'.inc {rit_models_for_ltspice_montecarlo_file_path}'

# snm-max and snm-min
v_sweep_seevinck = 0.707
snm_max = f'.measure dc snm_max MAX({v_sweep_seevinck}*v(V1)-{v_sweep_seevinck}*v(V2))'
snm_min = f'.measure dc snm_min MIN({v_sweep_seevinck}*v(V1)-{v_sweep_seevinck}*v(V2))'


# vwl, vbl, vblneg
vwl_hold = '0'
vbl_hold = '1'
vblneg_hold = '1'

vwl_read = '1'
vbl_read = '1'
vblneg_read = '1'


########################################################################################################################
# SNM STANDARD

# AX
l_ax_standard = '0.12u'
w_ax_start_standard = '0.12u'
w_ax_stop_standard = '0.24u'
w_ax_step_standard = '0.01u'
w_ax_step_param_standard = f'.step param w_ax {w_ax_start_standard} {w_ax_stop_standard} {w_ax_step_standard}'

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
dc_vsweep_standard = f'.dc Vsweep {dc_vsweep_start_standard} {dc_vsweep_stop_standard} {dc_vsweep_step_standard}'


########################################################################################################################
# SNM SEEVINCK

# AX
l_ax_seevinck = '0.12u'
w_ax_start_seevinck = '0.12u'
w_ax_stop_seevinck = '0.24u'
w_ax_step_seevinck = '0.01u'
w_ax_step_param_seevinck = f'.step param w_ax {w_ax_start_seevinck} {w_ax_stop_seevinck} {w_ax_step_seevinck}'

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
w_ax_gaussian_vth = '0.24u'
w_ax_start_gaussian_vth = '0.12u'
w_ax_stop_gaussian_vth = '0.24u'
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

# dc Vsweep
dc_vsweep_start_gaussian_vth = -v_sweep_seevinck
dc_vsweep_stop_gaussian_vth = v_sweep_seevinck
dc_vsweep_step_gaussian_vth = 0.01
dc_vsweep_gaussian_vth = f'.dc Vsweep {dc_vsweep_start_gaussian_vth} {dc_vsweep_stop_gaussian_vth} {dc_vsweep_step_gaussian_vth}'

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
step_param_run_gaussian_vth = f'.step param run {step_param_run_gaussian_vth_start} {step_param_run_gaussian_vth_stop} {step_param_run_gaussian_vth_step}'
