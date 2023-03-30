# Math142 Constrained Voter Simulation
import random
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython import display
matplotlib.use("TkAgg")


class Model:
    def __init__(self, initial_left, initial_right, initial_center, birth_chance, death_chance, iterations):
        self.left = initial_left  # 0
        self.right = initial_right  # 1
        self.center = initial_center  # 2
        self.total = self.left + self.right + self.center
        self.birth_rate = birth_chance
        self.death_rate = death_chance
        self.leftDens = self.left / self.total
        self.centerDens = self.center / self.total
        self.rightDens = self.right / self.total
        self.iterations = iterations

    def get_probability(self, i, j):
        n = [self.left, self.right, self.center]  # convenience
        if (i == j):
            return (n[i] * (n[j] - 1)) / (self.total * (self.total - 1))
        else:
            return (n[i] * n[j]) / (self.total * (self.total - 1))

    def select_individual_pair(self, ):
        dist = []
        for i in range(3):
            for j in range(3):
                dist.append(self.get_probability(i, j))
        value = random.uniform(0, 1)
        sum = 0
        for i in range(3):
            for j in range(3):
                sum += dist[3 * i + j]
                if value <= sum:
                    return i, j
        return 2, 2

    def change_mind(self, i, j):  # j changes mind of i
        if i == 0 and j == 2:
            self.left -= 1
            self.center += 1
        elif i == 2 and j == 0:
            self.center -= 1
            self.left += 1
        elif i == 1 and j == 2:
            self.right -= 1
            self.center += 1
        elif i == 2 and j == 1:
            self.center -= 1
            self.right += 1

    def transition(self):
        dist = []
        for i in range(3):
            for j in range(3):
                dist.append(self.get_probability(i, j))
        value = random.uniform(0, 1)
        sum = 0
        for i in range(3):
            for j in range(3):
                sum += dist[3 * i + j]
                if value <= sum:
                    # print(str(i) + " " + str(j))
                    self.change_mind(i, j)
                    self.updateValues()
                    return
        self.change_mind(2, 2)  # does nothing
        self.updateValues()
        # print("nothin")

    def equilibrium(self):
        if (self.center == 0):
            return True
        elif (self.left == self.total or self.right == self.total or self.center == self.total):
            return True
        else:
            return False

    def updateValues(self):
        self.total = self.center + self.left + self.right
        self.leftDens = self.left / self.total
        self.centerDens = self.center / self.total
        self.rightDens = self.right / self.total

    def add_to_species(self, i):
        if i == 0:
            self.left += 1
        elif i == 1:
            self.right += 1
        elif i == 2:
            self.center += 1
        self.updateValues()

    def birth_singular(self):
        value = random.uniform(0, 1)
        probs = [self.birth_rate * self.leftDens, self.birth_rate * self.rightDens, self.birth_rate * self.centerDens]
        norm = 0
        for i in probs:
            norm += i
        for i in range(3):
            probs[i] = probs[i] / norm
        for i in range(3):
            if value <= probs[i]:
                self.add_to_species(i)
                self.updateValues()
                return
        self.add_to_species(2)
        self.updateValues()

    def birth(self):
        value = random.uniform(0, 1)
        probs = [self.birth_rate * self.leftDens, self.birth_rate * self.rightDens, self.birth_rate * self.centerDens]
        s = []
        sum = 0
        for i in probs:
            sum += i
            s.append(sum)
        for i in range(3):
            if value <= s[i]:
                self.add_to_species(i)
                self.updateValues()
                return

    def birth_multiple(self):
        probs = [self.birth_rate * self.leftDens, self.birth_rate * self.rightDens, self.birth_rate * self.centerDens]
        rands = [random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)]
        if rands[0] <= probs[0]:
            self.left += 1
        if rands[1] <= probs[1]:
            self.right += 1
        if rands[2] <= probs[2]:
            self.center += 1
        self.updateValues()

    def simulate(self):
        count = 0
        while not self.equilibrium():
            self.transition()
            count += 1
        return count

    def simulate_birth_multiple(self):
        count = 0
        while (not self.equilibrium()) and (count < self.iterations):
            self.transition()
            self.birth_multiple()
            count += 1
        return count

    def simulate_birth(self):
        count = 0
        while (not self.equilibrium()) and (count < self.iterations):
            self.transition()
            self.birth()
            count += 1
        return count

    def verify_dist(self):
        dist = []
        for i in range(3):
            for j in range(3):
                dist.append(self.get_probability(i, j))
        sum = 0.0
        for i in dist:
            sum += i
        print(sum)
        print(dist)

    def random_walk(self, modulus):
        """Return a 3D random walk as (num_steps, 3) array."""
        start_pos = np.array([self.leftDens, self.rightDens, self.centerDens])
        steparr = [start_pos]
        for i in range(self.iterations):
            self.transition()
            self.birth()
            if i % modulus == 0:
                steparr.append((self.leftDens, self.rightDens, self.centerDens))
        steps = np.array(steparr)
        # print(steps)
        # walk = start_pos + np.cumsum(steps, axis=0)
        return steps

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


iterations = 10000

walks = [Model(random.randint(10, 100), random.randint(10, 100), random.randint(10, 100), 0, 0, iterations).random_walk(50) for _ in range(8)]

fig = plt.figure()

ax2d = fig.add_subplot(1, 2, 1, box_aspect=1.0)

ax = fig.add_subplot(1, 2, 2, projection="3d", sharex=ax2d, sharey=ax2d)
ax.view_init(45, 45)

fig.tight_layout()

# Create lines initially without data
lines = [ax.plot([], [], [])[0] for _ in walks]
lines.append(ax.plot(np.linspace(0, 1), 1-np.linspace(0, 1), [0 for _ in np.linspace(0, 1)]))
lines.append(ax.plot(np.linspace(0, 1), [0 for _ in np.linspace(0, 1)], 1-np.linspace(0, 1)))
lines.append(ax.plot([0 for _ in np.linspace(0, 1)], np.linspace(0, 1), 1-np.linspace(0, 1)))

lines2d = [ax2d.plot([], [])[0] for _ in walks]
lines2d.append(ax2d.plot(np.linspace(0, 1), 1-np.linspace(0, 1)))

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

plt.show()
