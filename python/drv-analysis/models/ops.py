from utils.check import check_file
from PyLTSpice import RawRead, SpiceEditor
from IPython.display import Image, display


def load(raw_file_path, asc_file_path, schematic_image_path):
    check_file(raw_file_path)
    ltr = RawRead(raw_file_path)

    check_file(asc_file_path)
    netlist = SpiceEditor(asc_file_path)

    display(Image(schematic_image_path))

    return ltr, netlist
