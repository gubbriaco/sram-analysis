from utils.check import check_file, check_image
from PyLTSpice import RawRead, SpiceEditor
from IPython.display import Image, display
from matplotlib import pyplot
from enum import Enum
from properties import (
    l_ax_standard, l_pmos_q_standard, w_pmos_q_standard, l_nmos_q_standard, w_nmos_q_standard, l_pmos_q_neg_standard,
    w_pmos_q_neg_standard, l_nmos_q_neg_standard, w_nmos_q_neg_standard
)
from properties import (
    l_ax_seevinck, l_pmos_q_seevinck, w_pmos_q_seevinck, l_nmos_q_seevinck, w_nmos_q_seevinck, l_pmos_q_neg_seevinck,
    w_pmos_q_neg_seevinck, l_nmos_q_neg_seevinck, w_nmos_q_neg_seevinck, e1_seevinck, e2_seevinck, e3_seevinck,
    e4_seevinck, e5_seevinck, e6_seevinck, e7_seevinck, e8_seevinck
)
from properties import (
    l_ax_gaussian_vth, l_pmos_q_gaussian_vth, w_pmos_q_gaussian_vth, l_nmos_q_gaussian_vth, w_nmos_q_gaussian_vth,
    l_pmos_q_neg_gaussian_vth, w_pmos_q_neg_gaussian_vth, l_nmos_q_neg_gaussian_vth, w_nmos_q_neg_gaussian_vth,
    e1_gaussian_vth, e2_gaussian_vth, e3_gaussian_vth, e4_gaussian_vth, e5_gaussian_vth, e6_gaussian_vth,
    e7_gaussian_vth, e8_gaussian_vth, w_ax_gaussian_vth
)
from properties import (
    l_ax_standard_ileak, w_ax_standard_ileak, l_pmos_q_standard_ileak, w_pmos_q_standard_ileak,
    l_nmos_q_standard_ileak, w_nmos_q_standard_ileak, l_pmos_q_neg_standard_ileak,
    w_pmos_q_neg_standard_ileak, l_nmos_q_neg_standard_ileak, w_nmos_q_neg_standard_ileak
)
from utils.path import data, images
import re
from PyLTSpice import SimRunner
import numpy as np
import pandas as pd
from pandas.plotting import table
from matplotlib import pyplot as plt
import os


def load_schematic(schematic_image_path: str) -> None:
    """"
    Mostra a video lo schematic corrispondente al path passato in input
    :param schematic_image_path: Percorso dell'immagine dello schema da visualizzare.
    """

    # Visualizza l'immagine dello schema
    display(Image(schematic_image_path))


def load_asc(asc_file_path: str) -> SpiceEditor:
    """
    Carica un file .asc (netlist SPICE) e mostra l'immagine dello schema corrispondente.

    :param asc_file_path: Percorso del file .asc contenente il netlist SPICE.
    :return: Un oggetto SpiceEditor rappresentante il netlist caricato.
    """

    # Verifica che il file .asc esista
    check_file(asc_file_path)

    # Carica il netlist SPICE dal file .asc
    netlist = SpiceEditor(asc_file_path)

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


def table_creation(
        data_table,
        title_plot,
        title_image_saving,
        figsize
):
    df = pd.DataFrame(data_table)
    blankIndex = [''] * len(df)
    df.index = blankIndex

    fig_table, ax_table = plt.subplots(figsize=(figsize[0], figsize[1]))
    ax_table.set_frame_on(False)
    ax_table.set_title(title_plot, fontsize=16, color='blue')
    tab = table(
        ax_table,
        df,
        loc='center',
        colWidths=[0.14] * len(df.columns),
        cellLoc='center'
    )
    tab.auto_set_font_size(False)
    tab.set_fontsize(11)

    for i, key in enumerate(df.keys()):
        cell = tab[0, i]
        cell.set_fontsize(12)
        cell.set_text_props(weight='bold', color='black')
        cell.set_facecolor('lightblue')

    tab.scale(1.2, 1.2)
    ax_table.axis('off')

    fig_table.tight_layout()
    save_image(image_path=os.path.join(images, title_image_saving), plt=plt)
    plt.show()


def get_data(pattern: str, content: str) -> list[float]:
    content_data = re.search(pattern, content, re.DOTALL).group(1)
    lines = content_data.strip().split('\n')[1:]
    data = [float(line.split('\t')[1]) for line in lines]
    return data


class CircuitType(Enum):
    STANDARD = 0
    SEEVINCK = 1
    GAUSSIAN_VTH_DC = 2
    STANDARD_ILEAK = 3


class OperationType(Enum):
    HOLD = 0
    READ = 1


class RequestPlotSchematic(Enum):
    TRUE = 1
    FALSE = 0


def __init_model__(
        operation_type: OperationType,
        circuit_type: CircuitType,
        asc_file_path: str,
        schematic_image_path: str,
        request_plot_schematic: RequestPlotSchematic,
        vdd: str,
        vsweep: str,
        vwl: str,
        vbl: str,
        vblneg: str,
        params: list[str]
) -> tuple[
    list[int],
    np.ndarray,
    list[np.ndarray],
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    str
]:
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
        steps, x, ileaks, vq, vqneg, vdd, vwl, vbl, vblneg, log = __init_standard__(
            operation=operation,
            asc_file_path=asc_file_path,
            schematic_image_path=schematic_image_path,
            request_plot_schematic=request_plot_schematic,
            vdd=vdd,
            vsweep=vsweep,
            vwl=vwl,
            vbl=vbl,
            vblneg=vblneg,
            params=params
        )
    elif circuit_type == CircuitType.SEEVINCK:
        steps, x, ileaks, vq, vqneg, vdd, vwl, vbl, vblneg, log = __init_seevinck__(
            operation=operation,
            asc_file_path=asc_file_path,
            schematic_image_path=schematic_image_path,
            request_plot_schematic=request_plot_schematic,
            vdd=vdd,
            vsweep=vsweep,
            vwl=vwl,
            vbl=vbl,
            vblneg=vblneg,
            params=params
        )
    elif circuit_type == CircuitType.GAUSSIAN_VTH_DC:
        steps, x, ileaks, vq, vqneg, vdd, vwl, vbl, vblneg, log = __init_gaussian_vth_dc__(
            operation=operation,
            asc_file_path=asc_file_path,
            schematic_image_path=schematic_image_path,
            request_plot_schematic=request_plot_schematic,
            vdd=vdd,
            vsweep=vsweep,
            vwl=vwl,
            vbl=vbl,
            vblneg=vblneg,
            params=params
        )
    elif circuit_type == CircuitType.STANDARD_ILEAK:
        steps, x, ileaks, vq, vqneg, vdd, vwl, vbl, vblneg, log = __init_standard_ileak__(
            operation=operation,
            asc_file_path=asc_file_path,
            schematic_image_path=schematic_image_path,
            request_plot_schematic=request_plot_schematic,
            vdd=vdd,
            vsweep=vsweep,
            vwl=vwl,
            vbl=vbl,
            vblneg=vblneg,
            params=params
        )
    else:
        raise ValueError()

    return steps, x, ileaks, vq, vqneg, vdd, vwl, vbl, vblneg, log


def __init_standard__(
        operation: str,
        asc_file_path: str,
        schematic_image_path: str,
        request_plot_schematic: RequestPlotSchematic,
        vdd: str,
        vsweep: str,
        vwl: str,
        vbl: str,
        vblneg: str,
        params: list[str]
) -> tuple[
    list[int],
    np.ndarray,
    list[np.ndarray],
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    str
]:
    standard_netlist = load_asc(
        asc_file_path=asc_file_path
    )
    if request_plot_schematic == RequestPlotSchematic.TRUE:
        load_schematic(
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

    standard_runner = SimRunner(output_folder=f"{data}/in/standard/{operation}/")
    standard_runner.run(netlist=standard_netlist, timeout=3600)
    print('Successful/Total Simulations: ' + str(standard_runner.okSim) + '/' + str(standard_runner.runno), flush=True)

    standard_raw = ""
    standard_log = ""
    for raw, log in standard_runner:
        standard_raw = raw
        standard_log = log
        print("Raw file: %s, Log file: %s" % (standard_raw, standard_log), flush=True)

    standard_ltr = load_ltr(raw_file_path=standard_raw)
    v_q_standard = standard_ltr.get_trace("V(q)")
    v_sweep_standard = standard_ltr.get_trace('vsweep')
    steps = standard_ltr.get_steps()

    v_q_neg_standard = v_sweep_standard
    log = standard_log

    v_dd_standard = np.ndarray([])
    v_wl_standard = np.ndarray([])
    v_bl_standard = np.ndarray([])
    v_blneg_standard = np.ndarray([])
    i_leaks_standard = []

    return (
        steps,
        v_sweep_standard,
        i_leaks_standard,
        v_q_standard,
        v_q_neg_standard,
        v_dd_standard,
        v_wl_standard,
        v_bl_standard,
        v_blneg_standard,
        log
    )


def __init_seevinck__(
        operation: str,
        asc_file_path: str,
        schematic_image_path: str,
        request_plot_schematic: RequestPlotSchematic,
        vdd: str,
        vsweep: str,
        vwl: str,
        vbl: str,
        vblneg: str,
        params: list[str]
) -> tuple[
    list[int],
    np.ndarray,
    list[np.ndarray],
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    str
]:
    seevinck_netlist = load_asc(
        asc_file_path=asc_file_path
    )
    if request_plot_schematic == RequestPlotSchematic.TRUE:
        load_schematic(
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

    seevinck_runner = SimRunner(output_folder=f"{data}/in/seevinck/{operation}/")
    seevinck_runner.run(netlist=seevinck_netlist, timeout=3600)
    print('Successful/Total Simulations: ' + str(seevinck_runner.okSim) + '/' + str(seevinck_runner.runno), flush=True)

    seevinck_raw = ""
    seevinck_log = ""
    for raw, log in seevinck_runner:
        seevinck_raw = raw
        seevinck_log = log
        print("Raw file: %s, Log file: %s" % (seevinck_raw, seevinck_log), flush=True)

    seevinck_ltr = load_ltr(raw_file_path=seevinck_raw)
    v_1_seevinck = seevinck_ltr.get_trace("V(v1)")
    v_2_seevinck = seevinck_ltr.get_trace("V(v2)")
    v_sweep_seevinck = seevinck_ltr.get_trace('vsweep')
    steps = seevinck_ltr.get_steps()
    log = seevinck_log

    v_dd_seevinck = np.ndarray([])
    v_wl_seevinck = np.ndarray([])
    v_bl_seevinck = np.ndarray([])
    v_blneg_seevinck = np.ndarray([])
    i_leaks_gaussian_vth = []

    return (
        steps,
        v_sweep_seevinck,
        i_leaks_gaussian_vth,
        v_1_seevinck,
        v_2_seevinck,
        v_dd_seevinck,
        v_wl_seevinck,
        v_bl_seevinck,
        v_blneg_seevinck,
        log
    )


def __init_gaussian_vth_dc__(
        operation: str,
        asc_file_path: str,
        schematic_image_path: str,
        request_plot_schematic: RequestPlotSchematic,
        vdd: str,
        vsweep: str,
        vwl: str,
        vbl: str,
        vblneg: str,
        params: list[str]
) -> tuple[
    list[int],
    np.ndarray,
    list[np.ndarray],
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    str
]:
    gaussian_vth_dc_netlist = load_asc(
        asc_file_path=asc_file_path
    )
    if request_plot_schematic == RequestPlotSchematic.TRUE:
        load_schematic(
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

    gaussian_vth_dc_runner = SimRunner(output_folder=f"{data}/in/gaussian-vth/{operation}/")
    gaussian_vth_dc_runner.run(netlist=gaussian_vth_dc_netlist, timeout=36000)
    print('Successful/Total Simulations: ' + str(gaussian_vth_dc_runner.okSim) + '/' + str(
        gaussian_vth_dc_runner.runno), flush=True)

    gaussian_vth_dc_raw = ""
    gaussian_vth_dc_log = ""
    for raw, log in gaussian_vth_dc_runner:
        gaussian_vth_dc_raw = raw
        gaussian_vth_dc_log = log
        print("Raw file: %s, Log file: %s" % (gaussian_vth_dc_raw, gaussian_vth_dc_log), flush=True)

    gaussian_vth_dc_ltr = load_ltr(raw_file_path=gaussian_vth_dc_raw)
    v_1_gaussian_dc_vth = gaussian_vth_dc_ltr.get_trace("V(v1)")
    v_2_gaussian_dc_vth = gaussian_vth_dc_ltr.get_trace("V(v2)")
    v_sweep_gaussian_vth_dc = gaussian_vth_dc_ltr.get_trace('vsweep')
    steps = gaussian_vth_dc_ltr.get_steps()

    log = gaussian_vth_dc_log

    v_dd_gaussian_vth = np.ndarray([])
    v_wl_gaussian_vth = np.ndarray([])
    v_bl_gaussian_vth = np.ndarray([])
    v_blneg_gaussian_vth = np.ndarray([])
    i_leaks_gaussian_vth_dc = []

    return (
        steps,
        v_sweep_gaussian_vth_dc,
        i_leaks_gaussian_vth_dc,
        v_1_gaussian_dc_vth,
        v_2_gaussian_dc_vth,
        v_dd_gaussian_vth,
        v_wl_gaussian_vth,
        v_bl_gaussian_vth,
        v_blneg_gaussian_vth,
        log
    )


def __init_standard_ileak__(
        operation: str,
        asc_file_path: str,
        schematic_image_path: str,
        request_plot_schematic: RequestPlotSchematic,
        vdd: str,
        vsweep: str,
        vwl: str,
        vbl: str,
        vblneg: str,
        params: list[str]
) -> tuple[
    list[int],
    np.ndarray,
    list[np.ndarray],
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    str
]:
    standard_ileak_netlist = load_asc(
        asc_file_path=asc_file_path
    )
    if request_plot_schematic == RequestPlotSchematic.TRUE:
        load_schematic(
            schematic_image_path=schematic_image_path
        )
    standard_ileak_netlist.set_parameter('l_ax', l_ax_standard_ileak)
    standard_ileak_netlist.set_parameter('w_ax', w_ax_standard_ileak)
    standard_ileak_netlist.set_parameter('l_pmos_q', l_pmos_q_standard_ileak)
    standard_ileak_netlist.set_parameter('w_pmos_q', w_pmos_q_standard_ileak)
    standard_ileak_netlist.set_parameter('l_nmos_q', l_nmos_q_standard_ileak)
    standard_ileak_netlist.set_parameter('w_nmos_q', w_nmos_q_standard_ileak)
    standard_ileak_netlist.set_parameter('l_pmos_q_neg', l_pmos_q_neg_standard_ileak)
    standard_ileak_netlist.set_parameter('w_pmos_q_neg', w_pmos_q_neg_standard_ileak)
    standard_ileak_netlist.set_parameter('l_nmos_q_neg', l_nmos_q_neg_standard_ileak)
    standard_ileak_netlist.set_parameter('w_nmos_q_neg', w_nmos_q_neg_standard_ileak)
    standard_ileak_netlist.set_parameter('vdd', vdd)
    standard_ileak_netlist.set_parameter('vsweep', vsweep)
    standard_ileak_netlist.set_parameter('vwl', vwl)
    standard_ileak_netlist.set_component_value('Vbl', vbl)
    standard_ileak_netlist.set_component_value('Vblneg', vblneg)
    for param in params:
        standard_ileak_netlist.add_instructions(param)

    standard_ileak_runner = SimRunner(output_folder=f"{data}/in/standard/{operation}_ileak/")
    standard_ileak_runner.run(netlist=standard_ileak_netlist, timeout=36000)
    print('Successful/Total Simulations: ' + str(standard_ileak_runner.okSim) + '/' + str(
        standard_ileak_runner.runno), flush=True)

    standard_ileak_raw = ""
    standard_ileak_log = ""
    for raw, log in standard_ileak_runner:
        standard_ileak_raw = raw
        standard_ileak_log = log
        print("Raw file: %s, Log file: %s" % (standard_ileak_raw, standard_ileak_log), flush=True)

    standard_ileak_ltr = load_ltr(raw_file_path=standard_ileak_raw)
    v_1_standard_ileak = standard_ileak_ltr.get_trace("V(q)")
    v_2_standard_ileak = standard_ileak_ltr.get_trace("V(qneg)")
    v_dd_standard_ileak = standard_ileak_ltr.get_trace("V(vdd)")
    v_wl_standard_ileak = standard_ileak_ltr.get_trace("V(wl)")
    v_bl_standard_ileak = standard_ileak_ltr.get_trace("V(bl)")
    v_blneg_standard_ileak = standard_ileak_ltr.get_trace("V(blneg)")
    time = standard_ileak_ltr.get_trace('vsweep')
    steps = standard_ileak_ltr.get_steps()

    log = standard_ileak_log

    i_leaks_standard_ileak = get_ileaks(standard_ileak_ltr, operation)

    return (
        steps,
        time,
        i_leaks_standard_ileak,
        v_1_standard_ileak,
        v_2_standard_ileak,
        v_dd_standard_ileak,
        v_wl_standard_ileak,
        v_bl_standard_ileak,
        v_blneg_standard_ileak,
        log
    )


def get_ileaks(
        ltr: RawRead,
        operation: str
) -> list[np.ndarray]:
    i_leaks = []
    if operation == "hold":
        i_leak_ax_q = ltr.get_trace("Id(M7)")
        i_leak_pu_q = ltr.get_trace("Id(M6)")
        i_leak_pd_qneg = ltr.get_trace("Id(M3)")
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
