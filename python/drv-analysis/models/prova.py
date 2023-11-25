import numpy as np
import matplotlib.pyplot as plt


def get_sine_samples(n):
    t = np.linspace(0, 2 * np.pi, n)
    return np.sin(t)


def draw_inscribable_square(height, width):
    x1, y1 = 0, 0
    x2, y2 = width, 0
    print(x2)
    x3, y3 = width, height
    x4, y4 = 0, height

    plt.plot([x2, x3], [y2, y3], 'r-')


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


def main():
    n = 1000
    samples = get_sine_samples(n)
    segments = find_segments(samples)

    height = max(segments[0])
    width = len(segments[0])
    draw_inscribable_square(height, width)

    plt.plot(range(n), samples, 'b-')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Sine Curve with Inscribable Squares')
    plt.show()


if __name__ == "__main__":
    main()
