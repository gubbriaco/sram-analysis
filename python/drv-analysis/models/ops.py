import numpy as np

from utils.check import check_file, check_image
from PyLTSpice import RawRead, SpiceEditor
from IPython.display import Image, display
from matplotlib import pyplot
from enum import Enum
from properties import rit_models, l_ax_standard, w_ax_step_param_standard, save_w_ax_standard, l_pmos_q_standard, \
    w_pmos_q_standard, l_nmos_q_standard, w_nmos_q_standard, l_pmos_q_neg_standard, w_pmos_q_neg_standard, \
    l_nmos_q_neg_standard, w_nmos_q_neg_standard, dc_vsweep_standard, vsweep_standard
from properties import snm_max, snm_min
from properties import l_ax_seevinck, w_ax_step_param_seevinck, save_w_ax_seevinck, l_pmos_q_seevinck, \
    w_pmos_q_seevinck, l_nmos_q_seevinck, w_nmos_q_seevinck, l_pmos_q_neg_seevinck, w_pmos_q_neg_seevinck, \
    l_nmos_q_neg_seevinck, w_nmos_q_neg_seevinck, dc_vsweep_seevinck, vsweep_seevinck, e1_seevinck, \
    e2_seevinck, e3_seevinck, e4_seevinck, e5_seevinck, e6_seevinck, e7_seevinck, e8_seevinck
from properties import rit_models_montecarlo, l_ax_gaussian_vth, l_pmos_q_gaussian_vth, w_pmos_q_gaussian_vth, \
    l_nmos_q_gaussian_vth, w_nmos_q_gaussian_vth, l_pmos_q_neg_gaussian_vth, w_pmos_q_neg_gaussian_vth, \
    l_nmos_q_neg_gaussian_vth, w_nmos_q_neg_gaussian_vth, dc_vsweep_gaussian_vth, vsweep_gaussian_vth, \
    e1_gaussian_vth, e2_gaussian_vth, e3_gaussian_vth, e4_gaussian_vth, e5_gaussian_vth, e6_gaussian_vth, \
    e7_gaussian_vth, e8_gaussian_vth, step_param_run_gaussian_vth, w_ax_gaussian_vth, tran_gaussian_vth
from utils.path import data
import re
from PyLTSpice import SimRunner


def load_asc(asc_file_path: str, schematic_image_path: str) -> SpiceEditor:
    """
    Carica un file .asc (netlist SPICE) e mostra l'immagine dello schema corrispondente.

    :param asc_file_path: Percorso del file .asc contenente il netlist SPICE.
    :param schematic_image_path: Percorso dell'immagine dello schema da visualizzare.
    :return: Un oggetto SpiceEditor rappresentante il netlist caricato.
    """

    # Verifica che il file .asc esista
    check_file(asc_file_path)

    # Carica il netlist SPICE dal file .asc
    netlist = SpiceEditor(asc_file_path)

    # Visualizza l'immagine dello schema
    # display(Image(schematic_image_path))

    # Restituisci l'oggetto SpiceEditor contenente la netlist
    return netlist


def load_ltr(raw_file_path: str) -> RawRead:
    """
    Carica un file .raw contenente dati di simulazione LTspice.

    :param raw_file_path: Percorso del file .raw contenente i dati di simulazione LTspice.
    :return: Un oggetto RawRead rappresentante i dati caricati dalla simulazione LTspice.
    """

    # Verifica che il file .raw esista
    check_file(raw_file_path)

    # Carica i dati dalla simulazione LTspice dal file .raw
    ltr = RawRead(raw_file_path)

    # Restituisci l'oggetto RawRead contenente i dati di simulazione
    return ltr


def save_image(image_path: str, plt: pyplot) -> None:
    """
    Salva un'immagine utilizzando il percorso specificato e un oggetto pyplot di matplotlib.

    :param image_path: Percorso in cui salvare l'immagine.
    :param plt: Oggetto pyplot di matplotlib contenente l'immagine da salvare.
    :return: None
    """

    # Verifica che il percorso e l'immagine siano validi
    check_image(image_path)

    # Salva l'immagine utilizzando l'oggetto pyplot
    plt.savefig(image_path, format='png')


def get_data(pattern: str, content: str) -> list[float]:
    content_data = re.search(pattern, content, re.DOTALL).group(1)
    lines = content_data.strip().split('\n')[1:]
    data = [float(line.split('\t')[1]) for line in lines]
    return data


class CircuitType(Enum):
    STANDARD = 0
    SEEVINCK = 1
    GAUSSIAN_VTH_DC = 2
    GAUSSIAN_VTH_TRANSIENT = 3


class OperationType(Enum):
    HOLD = 0
    READ = 1


def __init_model__(
        operation_type: OperationType,
        circuit_type: CircuitType,
        asc_file_path: str,
        schematic_image_path: str,
        vdd: str,
        vsweep: str,
        vwl: str,
        vbl: str,
        vblneg: str,
        params: list[str]
) -> tuple[list[int], np.ndarray, list[np.ndarray], np.ndarray, np.ndarray, str]:
    """
    Salva un'immagine utilizzando il percorso specificato e un oggetto pyplot di matplotlib.

    :param circuit_type: CircuitType
    :param asc_file_path: str
    :param schematic_image_path: str
    :param vdd: float
    :param vwl: float
    :param vbl: float
    :param vblneg: float
    :return: x, ileaks, vq, vqneg, log
    """

    if operation_type == OperationType.HOLD:
        operation = "hold"
    elif operation_type == OperationType.READ:
        operation = "read"
    else:
        raise ValueError()

    steps = []
    x = []
    ileaks = []
    vq = []
    vqneg = []
    log = ""
    if circuit_type == CircuitType.STANDARD:
        steps, x, ileaks, vq, vqneg, log = __init_standard__(
            operation=operation,
            asc_file_path=asc_file_path,
            schematic_image_path=schematic_image_path,
            vdd=vdd,
            vsweep=vsweep,
            vwl=vwl,
            vbl=vbl,
            vblneg=vblneg,
            params=params
        )
    elif circuit_type == CircuitType.SEEVINCK:
        steps, x, ileaks, vq, vqneg, log = __init_seevinck__(
            operation=operation,
            asc_file_path=asc_file_path,
            schematic_image_path=schematic_image_path,
            vdd=vdd,
            vsweep=vsweep,
            vwl=vwl,
            vbl=vbl,
            vblneg=vblneg,
            params=params
        )
    elif circuit_type == CircuitType.GAUSSIAN_VTH_DC:
        steps, x, ileaks, vq, vqneg, log = __init_gaussian_vth_dc__(
            operation=operation,
            asc_file_path=asc_file_path,
            schematic_image_path=schematic_image_path,
            vdd=vdd,
            vsweep=vsweep,
            vwl=vwl,
            vbl=vbl,
            vblneg=vblneg,
            params=params
        )
    elif circuit_type == CircuitType.GAUSSIAN_VTH_TRANSIENT:
        steps, x, ileaks, vq, vqneg, log = __init_gaussian_vth_transient__(
            operation=operation,
            asc_file_path=asc_file_path,
            schematic_image_path=schematic_image_path,
            vdd=vdd,
            vsweep=vsweep,
            vwl=vwl,
            vbl=vbl,
            vblneg=vblneg,
            params=params
        )
    else:
        raise ValueError()

    return steps, x, ileaks, vq, vqneg, log


def __init_standard__(
        operation: str,
        asc_file_path: str,
        schematic_image_path: str,
        vdd: str,
        vsweep: str,
        vwl: str,
        vbl: str,
        vblneg: str,
        params: list[str]
) -> tuple[list[int], np.ndarray, list[np.ndarray], np.ndarray, np.ndarray, str]:
    standard_netlist = load_asc(
        asc_file_path=asc_file_path,
        schematic_image_path=schematic_image_path
    )
    standard_netlist.set_parameter('l_ax', l_ax_standard)
    standard_netlist.set_parameter('l_pmos_q', l_pmos_q_standard)
    standard_netlist.set_parameter('w_pmos_q', w_pmos_q_standard)
    standard_netlist.set_parameter('l_nmos_q', l_nmos_q_standard)
    standard_netlist.set_parameter('w_nmos_q', w_nmos_q_standard)
    standard_netlist.set_parameter('l_pmos_q_neg', l_pmos_q_neg_standard)
    standard_netlist.set_parameter('w_pmos_q_neg', w_pmos_q_neg_standard)
    standard_netlist.set_parameter('l_nmos_q_neg', l_nmos_q_neg_standard)
    standard_netlist.set_parameter('w_nmos_q_neg', w_nmos_q_neg_standard)
    standard_netlist.set_parameter('vdd', vdd)
    standard_netlist.set_parameter('vwl', vwl)
    standard_netlist.set_parameter('vbl', vbl)
    standard_netlist.set_parameter('vblneg', vblneg)
    standard_netlist.set_parameter('vsweep', vsweep)
    for param in params:
        standard_netlist.add_instructions(param)

    standard_runner = SimRunner(output_folder=f"{data}/standard/{operation}/")
    standard_runner.run(netlist=standard_netlist, timeout=3600)
    print('Successful/Total Simulations: ' + str(standard_runner.okSim) + '/' + str(standard_runner.runno))

    standard_raw = ""
    standard_log = ""
    for standard_raw, standard_log in standard_runner:
        print("Raw file: %s, Log file: %s" % (standard_raw, standard_log))

    standard_ltr = load_ltr(raw_file_path=standard_raw)
    v_q_standard = standard_ltr.get_trace("V(q)")
    v_sweep_standard = standard_ltr.get_trace('vsweep')
    steps = standard_ltr.get_steps()

    v_q_neg_standard = v_sweep_standard
    log = standard_log

    i_leaks_standard = []

    return steps, v_sweep_standard, i_leaks_standard, v_q_standard, v_q_neg_standard, log


def __init_seevinck__(
        operation: str,
        asc_file_path: str,
        schematic_image_path: str,
        vdd: str,
        vsweep: str,
        vwl: str,
        vbl: str,
        vblneg: str,
        params: list[str]
) -> tuple[list[int], np.ndarray, list[np.ndarray], np.ndarray, np.ndarray, str]:
    seevinck_netlist = load_asc(
        asc_file_path=asc_file_path,
        schematic_image_path=schematic_image_path
    )
    seevinck_netlist.set_parameter('l_ax', l_ax_seevinck)
    seevinck_netlist.set_parameter('l_pmos_q', l_pmos_q_seevinck)
    seevinck_netlist.set_parameter('w_pmos_q', w_pmos_q_seevinck)
    seevinck_netlist.set_parameter('l_nmos_q', l_nmos_q_seevinck)
    seevinck_netlist.set_parameter('w_nmos_q', w_nmos_q_seevinck)
    seevinck_netlist.set_parameter('l_pmos_q_neg', l_pmos_q_neg_seevinck)
    seevinck_netlist.set_parameter('w_pmos_q_neg', w_pmos_q_neg_seevinck)
    seevinck_netlist.set_parameter('l_nmos_q_neg', l_nmos_q_neg_seevinck)
    seevinck_netlist.set_parameter('w_nmos_q_neg', w_nmos_q_neg_seevinck)
    seevinck_netlist.set_parameter('vdd', vdd)
    seevinck_netlist.set_parameter('vwl', vwl)
    seevinck_netlist.set_parameter('vbl', vbl)
    seevinck_netlist.set_parameter('vblneg', vblneg)
    seevinck_netlist.set_parameter('vsweep', vsweep)
    seevinck_netlist.set_parameter('e1', e1_seevinck)
    seevinck_netlist.set_parameter('e2', e2_seevinck)
    seevinck_netlist.set_parameter('e3', e3_seevinck)
    seevinck_netlist.set_parameter('e4', e4_seevinck)
    seevinck_netlist.set_parameter('e5', e5_seevinck)
    seevinck_netlist.set_parameter('e6', e6_seevinck)
    seevinck_netlist.set_parameter('e7', e7_seevinck)
    seevinck_netlist.set_parameter('e8', e8_seevinck)
    for param in params:
        seevinck_netlist.add_instructions(param)

    seevinck_runner = SimRunner(output_folder=f"{data}/seevinck/{operation}/")
    seevinck_runner.run(netlist=seevinck_netlist, timeout=3600)
    print('Successful/Total Simulations: ' + str(seevinck_runner.okSim) + '/' + str(seevinck_runner.runno))

    seevinck_raw = ""
    seevinck_log = ""
    for seevinck_raw, seevinck_log in seevinck_runner:
        print("Raw file: %s, Log file: %s" % (seevinck_raw, seevinck_log))

    seevinck_ltr = load_ltr(raw_file_path=seevinck_raw)
    v_1_seevinck = seevinck_ltr.get_trace("V(v1)")
    v_2_seevinck = seevinck_ltr.get_trace("V(v2)")
    v_sweep_seevinck = seevinck_ltr.get_trace('vsweep')
    steps = seevinck_ltr.get_steps()
    log = seevinck_log

    i_leaks_gaussian_vth = []

    return steps, v_sweep_seevinck, i_leaks_gaussian_vth, v_1_seevinck, v_2_seevinck, log


def __init_gaussian_vth_dc__(
        operation: str,
        asc_file_path: str,
        schematic_image_path: str,
        vdd: str,
        vsweep: str,
        vwl: str,
        vbl: str,
        vblneg: str,
        params: list[str]
) -> tuple[list[int], np.ndarray, list[np.ndarray], np.ndarray, np.ndarray, str]:
    gaussian_vth_dc_netlist = load_asc(
        asc_file_path=asc_file_path,
        schematic_image_path=schematic_image_path
    )
    gaussian_vth_dc_netlist.set_parameter('l_ax', l_ax_gaussian_vth)
    gaussian_vth_dc_netlist.set_parameter('w_ax', w_ax_gaussian_vth)
    gaussian_vth_dc_netlist.set_parameter('l_pmos_q', l_pmos_q_gaussian_vth)
    gaussian_vth_dc_netlist.set_parameter('w_pmos_q', w_pmos_q_gaussian_vth)
    gaussian_vth_dc_netlist.set_parameter('l_nmos_q', l_nmos_q_gaussian_vth)
    gaussian_vth_dc_netlist.set_parameter('w_nmos_q', w_nmos_q_gaussian_vth)
    gaussian_vth_dc_netlist.set_parameter('l_pmos_q_neg', l_pmos_q_neg_gaussian_vth)
    gaussian_vth_dc_netlist.set_parameter('w_pmos_q_neg', w_pmos_q_neg_gaussian_vth)
    gaussian_vth_dc_netlist.set_parameter('l_nmos_q_neg', l_nmos_q_neg_gaussian_vth)
    gaussian_vth_dc_netlist.set_parameter('w_nmos_q_neg', w_nmos_q_neg_gaussian_vth)
    gaussian_vth_dc_netlist.set_parameter('vdd', vdd)
    gaussian_vth_dc_netlist.set_parameter('vwl', vwl)
    gaussian_vth_dc_netlist.set_parameter('vbl', vbl)
    gaussian_vth_dc_netlist.set_parameter('vblneg', vblneg)
    gaussian_vth_dc_netlist.set_parameter('vsweep', vsweep)
    gaussian_vth_dc_netlist.set_parameter('e1', e1_gaussian_vth)
    gaussian_vth_dc_netlist.set_parameter('e2', e2_gaussian_vth)
    gaussian_vth_dc_netlist.set_parameter('e3', e3_gaussian_vth)
    gaussian_vth_dc_netlist.set_parameter('e4', e4_gaussian_vth)
    gaussian_vth_dc_netlist.set_parameter('e5', e5_gaussian_vth)
    gaussian_vth_dc_netlist.set_parameter('e6', e6_gaussian_vth)
    gaussian_vth_dc_netlist.set_parameter('e7', e7_gaussian_vth)
    gaussian_vth_dc_netlist.set_parameter('e8', e8_gaussian_vth)
    for param in params:
        gaussian_vth_dc_netlist.add_instructions(param)

    gaussian_vth_dc_runner = SimRunner(output_folder=f"{data}/gaussian-vth/{operation}/")
    gaussian_vth_dc_runner.run(netlist=gaussian_vth_dc_netlist, timeout=3600)
    print('Successful/Total Simulations: ' + str(gaussian_vth_dc_runner.okSim) + '/' + str(
        gaussian_vth_dc_runner.runno))

    gaussian_vth_dc_raw = ""
    gaussian_vth_dc_log = ""
    for gaussian_vth_dc_raw, gaussian_vth_dc_log in gaussian_vth_dc_runner:
        print("Raw file: %s, Log file: %s" % (gaussian_vth_dc_raw, gaussian_vth_dc_log))

    gaussian_vth_dc_ltr = load_ltr(raw_file_path=gaussian_vth_dc_raw)
    v_1_gaussian_dc_vth = gaussian_vth_dc_ltr.get_trace("V(v1)")
    v_2_gaussian_dc_vth = gaussian_vth_dc_ltr.get_trace("V(v2)")
    v_sweep_gaussian_vth_dc = gaussian_vth_dc_ltr.get_trace('vsweep')
    steps = gaussian_vth_dc_ltr.get_steps()

    log = gaussian_vth_dc_log

    i_leaks_gaussian_vth_dc = []

    return steps, v_sweep_gaussian_vth_dc, i_leaks_gaussian_vth_dc, v_1_gaussian_dc_vth, v_2_gaussian_dc_vth, log


def __init_gaussian_vth_transient__(
        operation: str,
        asc_file_path: str,
        schematic_image_path: str,
        vdd: str,
        vsweep: str,
        vwl: str,
        vbl: str,
        vblneg: str,
        params: list[str]
) -> tuple[list[int], np.ndarray, list[np.ndarray], np.ndarray, np.ndarray, str]:
    gaussian_vth_transient_netlist = load_asc(
        asc_file_path=asc_file_path,
        schematic_image_path=schematic_image_path
    )
    gaussian_vth_transient_netlist.set_parameter('l_ax', l_ax_gaussian_vth)
    gaussian_vth_transient_netlist.set_parameter('w_ax', w_ax_gaussian_vth)
    gaussian_vth_transient_netlist.set_parameter('l_pmos_q', l_pmos_q_gaussian_vth)
    gaussian_vth_transient_netlist.set_parameter('w_pmos_q', w_pmos_q_gaussian_vth)
    gaussian_vth_transient_netlist.set_parameter('l_nmos_q', l_nmos_q_gaussian_vth)
    gaussian_vth_transient_netlist.set_parameter('w_nmos_q', w_nmos_q_gaussian_vth)
    gaussian_vth_transient_netlist.set_parameter('l_pmos_q_neg', l_pmos_q_neg_gaussian_vth)
    gaussian_vth_transient_netlist.set_parameter('w_pmos_q_neg', w_pmos_q_neg_gaussian_vth)
    gaussian_vth_transient_netlist.set_parameter('l_nmos_q_neg', l_nmos_q_neg_gaussian_vth)
    gaussian_vth_transient_netlist.set_parameter('w_nmos_q_neg', w_nmos_q_neg_gaussian_vth)
    gaussian_vth_transient_netlist.set_parameter('vdd', vdd)
    gaussian_vth_transient_netlist.set_parameter('vwl', vwl)
    gaussian_vth_transient_netlist.set_parameter('vbl', vbl)
    gaussian_vth_transient_netlist.set_parameter('vblneg', vblneg)
    gaussian_vth_transient_netlist.set_parameter('vsweep', vsweep)
    gaussian_vth_transient_netlist.set_parameter('e1', e1_gaussian_vth)
    gaussian_vth_transient_netlist.set_parameter('e2', e2_gaussian_vth)
    gaussian_vth_transient_netlist.set_parameter('e3', e3_gaussian_vth)
    gaussian_vth_transient_netlist.set_parameter('e4', e4_gaussian_vth)
    gaussian_vth_transient_netlist.set_parameter('e5', e5_gaussian_vth)
    gaussian_vth_transient_netlist.set_parameter('e6', e6_gaussian_vth)
    gaussian_vth_transient_netlist.set_parameter('e7', e7_gaussian_vth)
    gaussian_vth_transient_netlist.set_parameter('e8', e8_gaussian_vth)
    for param in params:
        gaussian_vth_transient_netlist.add_instructions(param)

    gaussian_vth_transient_runner = SimRunner(output_folder=f"{data}/gaussian-vth/{operation}/")
    gaussian_vth_transient_runner.run(netlist=gaussian_vth_transient_netlist, timeout=3600)
    print('Successful/Total Simulations: ' + str(gaussian_vth_transient_runner.okSim) + '/' + str(
        gaussian_vth_transient_runner.runno))

    gaussian_vth_transient_raw = ""
    gaussian_vth_transient_log = ""
    for gaussian_vth_transient_raw, gaussian_vth_transient_log in gaussian_vth_transient_runner:
        print("Raw file: %s, Log file: %s" % (gaussian_vth_transient_raw, gaussian_vth_transient_log))

    gaussian_vth_transient_ltr = load_ltr(raw_file_path=gaussian_vth_transient_raw)
    v_1_gaussian_vth_transient = gaussian_vth_transient_ltr.get_trace("V(v1)")
    v_2_gaussian_vth_transient = gaussian_vth_transient_ltr.get_trace("V(v2)")
    time = gaussian_vth_transient_ltr.get_trace('time')
    steps = gaussian_vth_transient_ltr.get_steps()

    log = gaussian_vth_transient_log

    i_leaks_gaussian_vth_transient = get_ileaks(gaussian_vth_transient_ltr, operation)

    return steps, time, i_leaks_gaussian_vth_transient, v_1_gaussian_vth_transient, v_2_gaussian_vth_transient, log


def get_ileaks(ltr: RawRead, operation: str) -> list[np.ndarray]:
    i_leaks = []
    if operation == "hold":
        i_leak_ax_q = ltr.get_trace("Id(M5)")
        i_leak_pu_q = ltr.get_trace("Id(M1)")
        i_leak_pd_qneg = ltr.get_trace("Id(M4)")
        i_leaks.append(i_leak_ax_q)
        i_leaks.append(i_leak_pu_q)
        i_leaks.append(i_leak_pd_qneg)
    elif operation == "read":
        i_leaks.append([])
        i_leaks.append([])
        i_leaks.append([])
    else:
        raise ValueError()

    return i_leaks
