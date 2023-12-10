from utils.path import images, data
from models.ops import save_image
from matplotlib import pyplot as plt
import os

snm_hold_files_dir_path = os.path.join(data, 'out', 'hold', 'snm')
snm_hold_files_dir = os.listdir(snm_hold_files_dir_path)
array = []

for file_in_dir in snm_hold_files_dir:
    file_path = os.path.join(snm_hold_files_dir_path, file_in_dir)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
            array.append(content)

