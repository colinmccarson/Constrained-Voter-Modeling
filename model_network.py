import numpy as np
import random
import functools

import model


class Node:
    # linter?
    def __init__(self, node_model: model.Model, neighbors, attractiveness, emigration_resistance):
        self.model = node_model
        self.neighbors = neighbors  # connected nodes
        self.attractiveness = attractiveness  # list for values of left, right, center
        self.emigration_resistance = emigration_resistance  # resistance to leaving this node, same for everyone

    def emigrate_one(self):
        # If there exists a neighbor with attractiveness > self.attractiveness + emigration resistance, then leave move
        i = self.model.select_individual()
        attractive_neighbors = []
        for n in self.neighbors:
            if n[i] > self.attractiveness[i] + self.emigration_resistance:
                self.model.remove_from_species(i)
                attractive_neighbors.append(n)
        attract = [k[i] for k in attractive_neighbors]
        total = functools.reduce(lambda a, b: a + b, attract)
        prob_dens = list(map(lambda a: a / total, attract))
        cdf = list(map(lambda j: functools.reduce(lambda x, y: x + y, prob_dens[:j + 1]), range(len(prob_dens))))
        value = random.uniform(0, 1)
        for p in range(len(cdf)):
            if value <= cdf[p]:
                attractive_neighbors[p].add_to_species(i)
            elif p == len(cdf) - 1:  # handle floating point error in case last entry isn't 1
                attractive_neighbors[-1].add_to_species(i)


class Network:
    def __init__(self, size: int, maxCon: int, minPops: int, maxPops: int, growthBound: float = .01, attractBound: int = 100, emiBound: int = 100, complete:bool = False, iterations:int = 10000, modulus:int = 50):
        self.nodes: list[Node] = []
        self._models: list[model.Model] = []

        for i in range(size):
            maxPop = random.randint(minPops, maxPops)

            centrist_density = random.uniform(0, 1)
            leftist_density = random.uniform(0, 1-centrist_density)
            rightist_density = 1-centrist_density-leftist_density

            cent_pop = centrist_density*maxPop
            left_pop = leftist_density*maxPop
            right_pop = rightist_density*maxPop

            birth_rate = random.uniform(0, growthBound)
            death_rate = random.uniform(0, growthBound)

            self._models.append(model.Model(left_pop, right_pop, cent_pop, birth_rate, death_rate, iterations, modulus))

        # Generate nodelist
        for m in self._models:
            attractiveness = random.randint(0, attractBound)
            emigration_resistance = random.randint(0, emiBound)
            self.nodes.append(Node(m, [], attractiveness, emigration_resistance))

        # Generate edges
        if complete:
            for j in range(len(self.nodes)):
                self.nodes[j].neighbors = self.nodes[:j] + self.nodes[j + 1:]
        else:
            for n in self.nodes:
                k_neighbors = random.randint(0, maxCon)
                n.neighbors = [self.nodes[j] for j in random.sample([i for i in range(len(self.nodes))], k_neighbors)]






    def transition(self):
        for n in self.nodes:
            n.model.transition()
            n.emigrate_one()

