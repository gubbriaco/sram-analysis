from utils.path import rit_models_for_ltspice_file_path


# rit-models
rit_models = f'.inc {rit_models_for_ltspice_file_path}'

# AX
l_ax = '0.12u'
w_ax_start = '0.12u'
w_ax_stop = '0.24u'
w_ax_step = '0.01u'
w_ax_step_param = f'.step param w_ax {w_ax_start} {w_ax_stop} {w_ax_step}'

# save w_ax
save_w_ax = '.meas w_ax_values param w_ax'

# Q transistor
l_pmos_q = '0.12u'
w_pmos_q = '0.12u'
l_nmos_q = '0.12u'
w_nmos_q = '0.48u'

# Q neg transistor
l_pmos_q_neg = '0.12u'
w_pmos_q_neg = '0.12u'
l_nmos_q_neg = '0.12u'
w_nmos_q_neg = '0.48u'

# voltage
vdd = '1'
vsweep = '1'

# dc Vsweep
dc_vsweep_start = 0
dc_vsweep_stop = 1
dc_vsweep_step = 0.01
dc_vsweep = f'.dc Vsweep {dc_vsweep_start} {dc_vsweep_stop} {dc_vsweep_step}'
