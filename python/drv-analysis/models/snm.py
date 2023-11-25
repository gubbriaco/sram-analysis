import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from scipy.interpolate import interp1d


def standard_processing(x_vq, vq, x_vqneg, vqneg, ax, factor=100):
    x1 = np.linspace(np.min(x_vq), np.max(x_vq), len(vq) * int(factor))
    f = interp1d(x_vq, vq, kind='cubic')
    y1 = f(x1)

    x2 = np.linspace(np.min(x_vqneg), np.max(x_vqneg), len(vqneg) * int(factor))
    f = interp1d(x_vqneg, vqneg, kind='cubic')
    y2 = f(x2)

    ax.plot(x1, y1, color='blue')
    ax.plot(x2, y2, color='green')
    cross_index = np.argwhere(np.diff(np.sign(y1 - y2)) != 0).reshape(-1) + 0
    cross_index = cross_index[len(cross_index) // 2]
    # ax.plot(x1[cross_index], y1[cross_index], 'go', color='red')

    if y1[cross_index - 1] < y2[cross_index + 1]:
        x1, y1, x2, y2 = x2, y2, x1, y1

    b = np.diff(y1[:cross_index])[::-1][:len(y1) - cross_index]
    b = np.cumsum(-b)
    max_len = 0
    mask_index1 = -1
    mask_index2 = -1
    for bi in b:
        cross_index1 = np.argwhere(np.diff(np.sign(y1 - x1 - bi)) != 0).reshape(-1)
        cross_index2 = np.argwhere(np.diff(np.sign(y2 - x2 - bi)) != 0).reshape(-1)
        line_len = (x1[cross_index1] - x2[cross_index2]) ** 2 + \
                   (y1[cross_index1] - y2[cross_index2]) ** 2
        if line_len > max_len:
            mask_index1 = cross_index1
            mask_index2 = cross_index2
            max_len = line_len
    x, y = [x2[mask_index2], x1[mask_index1]], [y2[mask_index2], y1[mask_index1]]
    edge = np.sqrt(max_len / 2)

    snm = np.sqrt(max_len)[0]

    ax.text(x[0] + edge + 0.05, y[0] + edge + 0.05, 'SNM= %.3f' % snm, fontsize=14)
    ax.add_patch(patches.Rectangle((x[0], y[0]), width=edge, height=edge, fill=False))
    ax.plot([x[0], x[0] + edge], [y[0], y[0] + edge], 'k')

    ax.add_patch(
        patches.Rectangle((y[0], x[0]), width=edge, height=edge, fill=False))
    ax.plot([y[0], y[0] + edge], [x[0], x[0] + edge], 'k')

    ax.grid()

    ax.legend(["V(q)", "V(q_neg)"])
    ax.set_title("Standard Method and SNM")

    return snm


def draw_inscribable_square(height, width, ax):
    x_snm_start, y_snm_start = width, 0
    x_snm_stop, y_snm_stop = width, height

    ax.plot([x_snm_start, x_snm_stop], [y_snm_start, y_snm_stop], 'r-')
    snm = y_snm_stop
    ax.text(x_snm_stop + 0.05, y_snm_stop + 0.05, 'SNM= %.3f' % snm, fontsize=14)

    return snm


def find_segments(samples):
    local_maxima = [i for i in range(1, len(samples) - 1) if samples[i - 1] < samples[i] > samples[i + 1]]
    segments = []
    start = 0
    for local_max in local_maxima:
        end = local_max
        segment = samples[start:end + 1]
        segments.append(segment)
        start = end
    segment = samples[start:]
    segments.append(segment)
    return segments


def seevinck_processing(x_v1_minus_v2, v1_minus_v2, ax):
    segments = find_segments(v1_minus_v2)

    height = max(segments[0])
    width = len(segments[0])
    draw_inscribable_square(height, width, ax)

    ax.plot(x_v1_minus_v2, v1_minus_v2, 'red')
    plt.title('Seevinck Method and SNM')
    plt.show()
