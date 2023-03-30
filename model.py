import numpy as np
import random


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
        # Probability of selecting the individual pair i,j
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

    def persuasive_collision(self):
        # Transition the model by one persuasive act
        prob_dens = []  # probability density function
        for i in range(3):
            for j in range(3):
                prob_dens.append(self.get_probability(i, j))
        value = random.uniform(0, 1)
        cum_sum = 0
        for i in range(3):
            for j in range(3):
                cum_sum += prob_dens[3 * i + j]
                if value <= cum_sum:
                    # print(str(i) + " " + str(j))
                    self.change_mind(i, j)
                    self.update_values()
                    return
        self.change_mind(2, 2)  # does nothing
        self.update_values()

    def equilibrium(self):
        if self.center == 0:
            return self.birth_rate - self.death_rate == 0  # Not equilibrium unless net growth is zero
        elif self.left == self.total or self.right == self.total or self.center == self.total:
            return True
        else:
            return False

    def update_values(self):
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
        self.update_values()

    def remove_from_species(self, i):
        if i == 0 and self.left > 0:
            self.left -= 1
        elif i == 1 and self.right > 0:
            self.right -= 1
        elif i == 2 and self.center > 0:
            self.center -= 1
        self.update_values()

    def birth_given_occurs(self):
        # Determine whether a birth occurs. If one does, compute the probability that given species has birth given
        # that birth occurs.
        value = random.uniform(0, 1)
        probabilities = [self.birth_rate * self.leftDens, self.birth_rate * self.rightDens,
                         self.birth_rate * self.centerDens]
        norm = 0
        for i in probabilities:
            norm += i
        for i in range(3):
            probabilities[i] = probabilities[i] / norm
        for i in range(3):
            if value <= probabilities[i]:
                self.add_to_species(i)
                self.update_values()
                return
        self.add_to_species(2)

    def birth(self):
        # Randomly select a species to birth into, or none at all
        value = random.uniform(0, 1)
        probabilities = [self.birth_rate * self.leftDens, self.birth_rate * self.rightDens, self.birth_rate * self.centerDens]
        s = []
        cum_sum = 0
        for i in probabilities:
            cum_sum += i
            s.append(cum_sum)
        for i in range(3):
            if value <= s[i]:
                self.add_to_species(i)
                return

    def death(self):
        # Randomly select a species to subtract from, or none at all
        value = random.uniform(0, 1)
        probabilities = [self.death_rate * self.leftDens, self.death_rate * self.rightDens, self.death_rate * self.centerDens]
        s = []
        cum_sum = 0
        for i in probabilities:
            cum_sum += i
            s.append(cum_sum)
        for i in range(3):
            if value <= s[i]:
                self.remove_from_species(i)
                return

    def birth_multiple(self):
        # uniform randomly determine whether a species produces a child. More than one species may produce a child.
        probabilities = [self.birth_rate * self.leftDens, self.birth_rate * self.rightDens, self.birth_rate * self.centerDens]
        rands = [random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)]

        if rands[0] <= probabilities[0]:
            self.left += 1
        if rands[1] <= probabilities[1]:
            self.right += 1
        if rands[2] <= probabilities[2]:
            self.center += 1
        self.update_values()

    def simulate_birth_multiple(self):
        count = 0
        while (not self.equilibrium()) and (count < self.iterations):
            self.persuasive_collision()
            self.birth_multiple()
            count += 1
        return count

    def simulate_birth(self):
        count = 0
        while (not self.equilibrium()) and (count < self.iterations):
            self.persuasive_collision()
            self.birth()
            count += 1
        return count

    def random_walk(self, modulus):
        """Return a 3D random walk as (num_steps, 3) array."""
        start_pos = np.array([self.leftDens, self.rightDens, self.centerDens])
        steparr = [start_pos]
        for i in range(self.iterations):
            self.persuasive_collision()
            if(self.birth_rate > 0):
                self.birth()
            if(self.death_rate > 0):
                self.death()
            if i % modulus == 0:
                steparr.append((self.leftDens, self.rightDens, self.centerDens))
        steps = np.array(steparr)
        # print(steps)
        # walk = start_pos + np.cumsum(steps, axis=0)
        return steps
