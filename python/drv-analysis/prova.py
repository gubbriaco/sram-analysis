from PyLTSpice import RawRead, SpiceEditor
from PyLTSpice import SimRunner


def load_asc(asc_file_path):
    netlist = SpiceEditor(asc_file_path)
    return netlist


def load_ltr(raw_file_path):
    ltr = RawRead(raw_file_path)
    return ltr


minimum_inverter_sizing_analysis_netlist = load_asc(
    asc_file_path="C:/Users/fremb/Downloads/minimum_inverter_connected.asc"
)
minimum_inverter_sizing_analysis_netlist.set_parameter('l_min_pmos', "0.12u")
minimum_inverter_sizing_analysis_netlist.set_parameter('l_min_nmos', "0.12u")
minimum_inverter_sizing_analysis_netlist.set_parameter('w_min_nmos', "0.24u")
minimum_inverter_sizing_analysis_netlist.add_instructions(".inc C:/Users/fremb/OneDrive/Desktop/Hardware and Software Codesign/Progettazione low power/Elaborato1/RIT_Models_For_LTSPICE.txt"
)
minimum_inverter_sizing_analysis_runner = SimRunner(output_folder="C:/Users/fremb/Desktop")
minimum_inverter_sizing_analysis_runner.run(netlist=minimum_inverter_sizing_analysis_netlist, timeout=3600)
print('Successful/Total Simulations: ' + str(minimum_inverter_sizing_analysis_runner.okSim) + '/' + str(
    minimum_inverter_sizing_analysis_runner.runno))

minimum_inverter_sizing_analysis_raw = ""
minimum_inverter_sizing_analysis_log = ""
for minimum_inverter_sizing_analysis_raw, minimum_inverter_sizing_analysis_log in minimum_inverter_sizing_analysis_runner:
    print("Raw file: %s, Log file: %s" % (minimum_inverter_sizing_analysis_raw, minimum_inverter_sizing_analysis_log))

minimum_inverter_sizing_analysis_ltr = load_ltr(raw_file_path=minimum_inverter_sizing_analysis_raw)
v_in_minimum_inverter_sizing_analysis = minimum_inverter_sizing_analysis_ltr.get_trace("V(in)")
v_out_minimum_inverter_sizing_analysis = minimum_inverter_sizing_analysis_ltr.get_trace("V(out)")
v_supply_minimum_inverter_sizing_analysis = minimum_inverter_sizing_analysis_ltr.get_trace("V(supply)")
time = minimum_inverter_sizing_analysis_ltr.get_trace('time')
steps = minimum_inverter_sizing_analysis_ltr.get_steps()


minimum_inverter_sizing_analysis_log_file_path = f"./{minimum_inverter_sizing_analysis_log}"

with open(minimum_inverter_sizing_analysis_log_file_path, "r") as file:
    content = file.read()