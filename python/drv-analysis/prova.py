import math

import matplotlib.pyplot as plt
import numpy as np

iterations_scaling = 12
rows = round(int(np.sqrt(iterations_scaling)))
tmp = iterations_scaling % rows
iterations = iterations_scaling
if tmp == 1:
    iterations = iterations_scaling + (rows-1)
elif tmp == 2:
    iterations = iterations_scaling + (rows-2)
cols = int(iterations / rows)
fig, axs = plt.subplots(rows, cols, figsize=(16, 6))
fig, axs = plt.subplots(rows, cols, figsize=(16, 6))
vdd_start = 1.0
vdd_stop = vdd_start - (iterations * 0.1)
vdd_step = 0.05
print('VDD Scaling Initialised')
row = 0
col = 0
for scaling in np.arange(vdd_start, vdd_stop, -vdd_step):
    if row == rows:
        break
    vdd_scaled = round(scaling, 2)
    axs[row, col].hist(math.sin(0.3), bins=100, edgecolor='black')
    axs[row, col].set_xlabel("SNM(HOLD)")
    axs[row, col].set_ylabel("#")
    axs[row, col].set_title(f"vdd={vdd_scaled} V Histogram")
    if col == (cols-1):
        row = row + 1
        col = 0
    else:
        col = col + 1
plt.subplots_adjust(hspace=1, wspace=1)
plt.show()