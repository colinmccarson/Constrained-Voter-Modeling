import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

import model


def update_3dlines(num, walks, lines):
    for line, walk in zip(lines, walks):
        # NOTE: there is no .set_data() for 3 dim data...
        line.set_data(walk[:num, :2].T)
        line.set_3d_properties(walk[:num, 2])
    return lines


def update_2dlines(num, walks, lines):
    for line, walk in zip(lines, walks):
        # NOTE: there is no .set_data() for 3 dim data...
        line.set_data(walk[:num, :2].T)
    return lines


def animate(iterations=10000, modulus=50, how_many=8, birth_rate=0, death_rate=0, init_cond=None):
    if init_cond is None:
        walks = [model.Model(random.randint(10, 100), random.randint(10, 100), random.randint(10, 100), birth_rate,
                             death_rate, iterations, modulus).random_walk() for _ in range(how_many)]
    else:
        walks = [model.Model(init_cond[0], init_cond[1], init_cond[2], birth_rate, death_rate,
                             iterations, modulus).random_walk() for _ in range(how_many)]

    fig = plt.figure()

    ax2d = fig.add_subplot(1, 2, 1, box_aspect=1.0)

    ax = fig.add_subplot(1, 2, 2, projection="3d", sharex=ax2d, sharey=ax2d)
    ax.view_init(45, 45)

    fig.tight_layout()

    # Create lines initially without data
    lines = [ax.plot([], [], [])[0] for _ in walks]
    lines.append(ax.plot(np.linspace(0, 1), 1 - np.linspace(0, 1), [0 for _ in np.linspace(0, 1)]))
    lines.append(ax.plot(np.linspace(0, 1), [0 for _ in np.linspace(0, 1)], 1 - np.linspace(0, 1)))
    lines.append(ax.plot([0 for _ in np.linspace(0, 1)], np.linspace(0, 1), 1 - np.linspace(0, 1)))

    lines2d = [ax2d.plot([], [])[0] for _ in walks]
    lines2d.append(ax2d.plot(np.linspace(0, 1), 1 - np.linspace(0, 1)))

    # Setting the axes properties
    ax.set(xlim3d=(0, 1), xlabel='X')
    ax.set(ylim3d=(0, 1), ylabel='Y')
    ax.set(zlim3d=(0, 1), zlabel='Z')

    ax2d.set(xlim=(0, 1), xlabel='X')
    ax2d.set(ylim=(0, 1), ylabel='Y')

    # Creating the Animation object
    ani = animation.FuncAnimation(
        fig, update_3dlines, iterations, fargs=(walks, lines), interval=1)
    ani2d = animation.FuncAnimation(fig, update_2dlines, iterations, fargs=(walks, lines2d), interval=1)
    return ani, ani2d
