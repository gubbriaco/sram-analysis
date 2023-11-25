from utils.path import rit_models_for_ltspice_file_path


# rit-models
rit_models = f'.inc {rit_models_for_ltspice_file_path}'


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
dc_vsweep_start_seevinck = -0.650
dc_vsweep_stop_seevinck = 0.650
dc_vsweep_step_seevinck = 0.01
dc_vsweep_seevinck = f'.dc Vsweep {dc_vsweep_start_seevinck} {dc_vsweep_stop_seevinck} {dc_vsweep_step_seevinck}'

# E1 E2 E3 E4 E5 E6 E7 E8
e1 = '0.707'
e2 = '0.707'
e3 = '1'
e4 = '1.41'
e5 = '-1'
e6 = '1.41'
e7 = '0.707'
e8 = '-0.707'
