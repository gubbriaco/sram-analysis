import os
from statistics import mean, stdev


def get_values_from_file(
        file_path
):
    values = []
    with open(file_path, 'r') as file:
        values = [float(line.strip()) for line in file]
    return values


def get_values_from_dir(
        files_dir_path
):
    files_dir = os.listdir(files_dir_path)
    files_values = []
    for file in files_dir:
        file_path = os.path.join(files_dir_path, file)
        with open(file_path, 'r') as f:
            values = [float(line.strip()) for line in f]
            files_values.append(values)
    rows_mean = [(i, mean(row)) for i, row in enumerate(files_values)]
    rows_mean_ordered = sorted(rows_mean, key=lambda x: x[1], reverse=True)
    files_values = [files_values[i] for i, _ in rows_mean_ordered]
    return files_values


def get_mean_from_file(values):
    mean_values_file = []
    for row in values:
        mean_values_file.append(mean(row))
    return mean_values_file


def get_stdev_from_file(values):
    stdev_values_file = []
    for row in values:
        stdev_values_file.append(stdev(row))
    return stdev_values_file
