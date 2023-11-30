import numpy as np
from matplotlib import patches
from scipy.interpolate import interp1d


def rotate_points(x: float, y: float, angle_degrees: float) -> tuple[float, float]:
    """
    Ruota un punto attorno all'origine di un angolo specificato in gradi.

    :param x: Coordinata x del punto da ruotare (tipo float).
    :param y: Coordinata y del punto da ruotare (tipo float).
    :param angle_degrees: Angolo di rotazione in gradi (tipo float).
    :return: Tuple contenente le coordinate x e y del punto ruotato.

    Questo metodo prende le coordinate (x, y) di un punto e lo ruota attorno all'origine di un angolo specificato in gradi.
    Restituisce una tupla con le nuove coordinate (x_rotated, y_rotated) del punto ruotato.
    """
    angle_radians = np.radians(angle_degrees)
    x_rotated = x * np.cos(angle_radians) - y * np.sin(angle_radians)
    y_rotated = x * np.sin(angle_radians) + y * np.cos(angle_radians)
    return x_rotated, y_rotated


def graphical_processing(x_vq, vq, x_vqneg, vqneg, ax, factor=100):
    x1, y1 = interpolate(x_v=x_vq, v=vq, factor=factor)
    x2, y2 = interpolate(x_v=x_vqneg, v=vqneg, factor=factor)

    cross_index = np.argwhere(np.diff(np.sign(y1 - y2)) != 0).reshape(-1) + 0
    cross_index = cross_index[len(cross_index) // 2]

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

    snm = 1000 * edge

    graphical_plot(
        ax=ax,
        x1=x1,
        y1=y1,
        x2=x2,
        y2=y2,
        edge=edge,
        snm=snm,
        x=x,
        y=y
    )

    return snm[0]


def interpolate(x_v, v, factor):
    x = np.linspace(start=np.min(x_v), stop=np.max(x_v), num=len(v) * int(factor))
    f = interp1d(x_v, v, kind='cubic')
    y = f(x)
    return x, y


def graphical_plot(ax, x1, y1, x2, y2, edge, snm, x, y):
    ax.plot(x1, y1, color='blue')
    ax.plot(x2, y2, color='green')

    ax.text(x[0] + edge + 0.05, y[0] + edge + 0.05, 'SNM= %.3f mV' % snm, fontsize=14)

    ax.add_patch(patches.Rectangle((x[0], y[0]), width=edge, height=edge, fill=False))
    ax.plot([x[0], x[0] + edge], [y[0], y[0] + edge], 'k')

    ax.add_patch(patches.Rectangle((y[0], x[0]), width=edge, height=edge, fill=False))
    ax.plot([y[0], y[0] + edge], [x[0], x[0] + edge], 'k')

    ax.grid()
    ax.legend(["V(q)", "V(q_neg)"])
    ax.set_title("Standard Method and SNM")


def seevinck_processing(x_v1_minus_v2, v1_minus_v2, ax):
    segments = find_segments(samples=v1_minus_v2)

    height = max(segments[0])
    i_width = np.where(v1_minus_v2 == height)[0]
    width = x_v1_minus_v2[i_width]
    (
        snm,
        x_snm_start,
        y_snm_start,
        x_diff_snm_start,
        y_diff_snm_start,
        x_diff_snm_stop,
        y_diff_snm_stop
    ) = inscribable_square(height=height, width=width)

    x_diff, y_diff = rotate_points(x=x_v1_minus_v2, y=v1_minus_v2, angle_degrees=-45)

    seevinck_plot(
        ax=ax,
        snm=snm,
        x_snm_start=x_snm_start,
        y_snm_start=y_snm_start,
        x_diff=x_diff,
        y_diff=y_diff,
        x_snm_diff=[x_diff_snm_start, x_diff_snm_stop],
        y_snm_diff=[y_diff_snm_start, y_diff_snm_stop]
    )

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


def inscribable_square(height, width):
    x_snm_start, y_snm_start = width, 0
    x_snm_stop, y_snm_stop = width, height

    x_diff_snm_start, y_diff_snm_start = rotate_points(x=x_snm_start, y=y_snm_start, angle_degrees=-45)
    x_diff_snm_stop, y_diff_snm_stop = rotate_points(x=x_snm_stop, y=y_snm_stop, angle_degrees=-45)

    snm = 1000 * height

    return (
        snm,
        x_snm_start,
        y_snm_start,
        x_diff_snm_start,
        y_diff_snm_start,
        x_diff_snm_stop,
        y_diff_snm_stop
    )


def seevinck_plot(ax, snm, x_snm_start, y_snm_start, x_diff, y_diff, x_snm_diff, y_snm_diff):
    ax.plot(x_diff, y_diff, 'red')
    ax.plot(x_snm_diff, y_snm_diff, 'k')
    ax.text(x_snm_start + 0.05, y_snm_start + 0.05, 'SNM= %.3f mV' % snm, fontsize=14)
    ax.set_title("V(v1)-V(v2) Curve Hold Phase and SNM")
    ax.grid()
