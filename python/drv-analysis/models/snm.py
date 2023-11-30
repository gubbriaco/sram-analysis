import numpy as np
from matplotlib import patches
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d
from typing import Union
from math import sqrt


def rotate_points(x: Union[float, list[float]], y: Union[float, list[float]], angle_degrees: float) -> tuple[
    Union[float, list[float]],
    Union[float, list[float]]
]:
    """
    Ruota un punto o un insieme di punti di un angolo specificato in gradi.

    :param x: Coordinata x del punto o coordinate x di un insieme di punti da ruotare .
    :param y: Coordinata y del punto o coordinate y di un insieme di punti da ruotare.
    :param angle_degrees: Angolo di rotazione in gradi.
    :return: Tuple contenente le coordinate x e y del punto ruotato o dell'insieme di punti ruotati.

    Questo metodo permette la rotazione di un punto avente coordinate (x,y) o di un insieme di punti avente coordinate
    (x,y) di un angolo specificato in gradi.
    """
    angle_radians = np.radians(angle_degrees)
    x_rotated = x * np.cos(angle_radians) - y * np.sin(angle_radians)
    y_rotated = x * np.sin(angle_radians) + y * np.cos(angle_radians)
    return x_rotated, y_rotated


def graphical_processing(
        x_vq: list[float], vq: list[float],
        x_vqneg: list[float], vqneg: list[float],
        ax: plt.axes,
        factor: int = 100
) -> float:
    """
    Processo grafico basato su interpolazione e calcolo di lunghezze con rappresentazione grafica.

    :param x_vq: Lista delle coordinate x per il primo set di dati.
    :param vq: Lista delle coordinate y per il primo set di dati.
    :param x_vqneg: Lista delle coordinate x per il secondo set di dati.
    :param vqneg: Lista delle coordinate y per il secondo set di dati.
    :param ax: Oggetto Axes di matplotlib per il disegno del grafico.
    :param factor: Fattore di interpolazione per ottenere curve più lisce (default: 100, tipo int).
    :return: La somma normalizzata di Manifold (SNM) calcolata durante il processo grafico (tipo float).

    Questo metodo esegue un processo grafico basato su interpolazione e calcolo di lunghezze. Prende in input due set
    di dati specificati da coordinate x e y, esegue un'interpolazione, calcola le intersezioni tra le curve
    risultanti e lo Static Noise Margin (SNM). Nello specifico, vengono tracciati i quadrati inscrivibili all'interno
    dei lobi ottenuti tramite intersezione delle curve.
    """
    x1, y1 = interpolate(x_v=x_vq, v=vq, factor=factor)
    x2, y2 = interpolate(x_v=x_vqneg, v=vqneg, factor=factor)

    cross_index = np.argwhere(np.diff(np.sign(np.array(y1) - np.array(y2))) != 0).reshape(-1) + 0
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


def interpolate(x_v: list[float], v: list[float], factor: int) -> tuple[np.ndarray[float], np.ndarray[float]]:
    """
    Interpolazione cubica di un set di dati.

    :param x_v: Lista delle coordinate x del set di dati originale.
    :param v: Lista delle coordinate y del set di dati originale.
    :param factor: Fattore di interpolazione per ottenere un numero maggiore di punti.
    :return: Tuple contenente le coordinate x e y del set di dati interpolato.

    Questo metodo esegue un'interpolazione cubica dei dati forniti. Prende in input le coordinate x e y del set di
    dati originale e un fattore di interpolazione. Restituisce una tupla con le nuove coordinate x e y del set di
    dati interpolato.
    """
    x = np.linspace(start=np.min(x_v), stop=np.max(x_v), num=len(v) * int(factor))
    f = interp1d(x_v, v, kind='cubic')
    y = f(x)
    return x, y


def graphical_plot(ax: plt.axes,
                   x1: np.ndarray[float], y1: np.ndarray[float],
                   x2: np.ndarray[float], y2: np.ndarray[float],
                   edge: float, snm: float,
                   x: np.ndarray[float], y: np.ndarray[float]
                   ) -> None:
    """
    Plotta un grafico con curve, testo e quadrati per rappresentare il risultato del processo grafico effettuato.

    :param ax: Oggetto Axes di matplotlib per il disegno del grafico.
    :param x1: Lista delle coordinate x per la prima curva.
    :param y1: Lista delle coordinate y per la prima curva.
    :param x2: Lista delle coordinate x per la seconda curva.
    :param y2: Lista delle coordinate y per la seconda curva.
    :param edge: Lunghezza del lato del quadrato.
    :param snm: Static Noise Margin
    :param x: Lista delle coordinate x per il quadrato.
    :param y: Lista delle coordinate y per il quadrato.
    :return: None

    Le curve definite dai dati (x1, y1) e (x2, y2) sono rappresentate in blu e verde rispettivamente. Nello
    specifico, vengono plottate le due curve corrispondenti per interpolazione e vengono tracciati i due quadrati
    inscrivibili nei due lobi corrispondenti all'intersezione tra le due curve.
    """
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


def seevinck_processing(x_v1_minus_v2: list[float], v1_minus_v2: list[float], ax: plt.axes) -> float:
    """
    Processo di elaborazione basato su metodo di Seevinck.

    :param x_v1_minus_v2: Lista dei valori delle ascisse corrispondenti a v1_minus_v2.
    :param v1_minus_v2: Lista dei valori delle ordinate corrispondenti a v1_minus_v2.
    :param ax: Oggetto axes di matplotlib per il plotting.
    :return: Static Noise Margin (SNM)

    Questo metodo esegue un processo di elaborazione basato su metodo di Seevinck. Trova segmenti nei dati, determina
    altezza e larghezza, calcola la SNM utilizzando un quadrato inscrivibile e disegna il risultato sul grafico.
    Restituisce l'SNM calcolato durante il processo.
    """
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
    snm = (1/sqrt(2)) * snm

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


def find_segments(samples: list[float]) -> list[list[float]]:
    """
    Trova segmenti in una lista di campioni.

    :param samples: Lista di campioni su cui cercare i segmenti.
    :return: Lista di segmenti trovati, ciascuno rappresentato come una lista di campioni.
    """
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


def inscribable_square(height: float, width: float) -> tuple[
    float, float, float, list[float], list[float], list[float], list[float]
]:
    """
    Calcola i parametri di un quadrato inscrivibile in un lobo specificato.

    :param height: Altezza del rettangolo (in questo caso facendo riferimento ad un quadrato).
    :param width: Larghezza del rettangolo (in questo caso facendo riferimento ad un quadrato).
    :return: Tuple contenente i parametri del quadrato inscrivibile: SNM, coordinate di inizio e fine, coordinate di
    inizio e fine ruotate a -45 gradi (tipo tuple[float, float, float, float, float, float, float]).

    Questo metodo calcola i parametri di un quadrato inscrivibile in un lobo. Restituisce una tupla contenente l'SNM, le
    coordinate di inizio e fine del quadrato, e le coordinate di inizio e fine ruotate a -45 gradi.
    """
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


def seevinck_plot(ax: plt.axes,
                  snm: float,
                  x_snm_start: float, y_snm_start: float,
                  x_diff: list[float], y_diff: list[float],
                  x_snm_diff: list[list[float]], y_snm_diff: list[list[float]]
                  ) -> None:
    """
    Disegna un grafico per il processo di elaborazione basato su metodo di Seevinck.

    :param ax: Oggetto axes di matplotlib per il plot.
    :param snm: Static Noise Margin
    :param x_snm_start: Coordinata x del quadrato rappresentante l'SNM.
    :param y_snm_start: Coordinata y del quadrato rappresentante l'SNM.
    :param x_diff: Lista dei valori delle ascisse della curva rappresentate la differenza tra V1 e V2.
    :param y_diff: Lista dei valori delle ordinate della curva rappresentate la differenza tra V1 e V2.
    :param x_snm_diff: Lista delle coordinate x del quadrato rappresentante l'SNM.
    :param y_snm_diff: Lista delle coordinate y del quadrato rappresentante l'SNM.
    :return: None

    Questo metodo disegna un grafico per il processo di elaborazione basato su metodo di Seevinck.
    La curva del processo è rappresentata in rosso, mentre la rappresentazione della SNM in nero.
    Viene aggiunto del testo con il valore della SNM e una griglia al grafico.
    """
    ax.plot(x_diff, y_diff, 'red')
    ax.plot(x_snm_diff, y_snm_diff, 'k')
    ax.text(x_snm_start + 0.05, y_snm_start + 0.05, 'SNM= %.3f mV' % snm, fontsize=14)
    ax.set_title("V(v1)-V(v2) Curve Hold Phase and SNM")
    ax.grid()
