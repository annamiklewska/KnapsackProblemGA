import random
from dataclasses import dataclass
import numpy as np


@dataclass
class Task:
    n_items: int
    max_weight: int
    max_size: int
    weights: list
    sizes: list
    costs: list


@dataclass
class Item:
    weight: int
    size: int
    cost: int


class Individual:
    def __init__(self, backpack: list) -> None:
        self.backpack = backpack
        self.fitness_val = 0

    def __str__(self):
        return "An individual with fitness val: " + "{:,}".format(self.fitness_val)

    def evaluate(self, task: Task) -> None:
        weight = sum(val * w for val, w in zip(self.backpack, task.weights))
        size = sum(val * s for val, s in zip(self.backpack, task.sizes))
        if weight <= task.max_weight and size <= task.max_size:
            self.fitness_val = sum(val * c for val, c in zip(self.backpack, task.costs))
        else:
            self.fitness_val = 0


class Population:
    def __init__(self, size: int) -> None:
        self.size = size
        self.individuals = []

    def add_individual(self, new_individual: Individual) -> bool:
        if len(self.individuals) >= self.size:
            return False
        else:
            self.individuals.append(new_individual)
            return True

    def add_individuals(self, new_individuals: list) -> bool:
        if len(self.individuals) + len(new_individuals) > self.size:
            return False
        else:
            self.individuals.extend(new_individuals)
            return True

    def replace_individuals(self, individuals_list: list) -> bool:
        if len(individuals_list) == self.size:
            self.individuals = individuals_list
            return True
        else:
            return False

    def evaluate_pop(self, task: Task) -> None:
        for i in self.individuals:
            i.evaluate(task)

    def sort_pop(self):
        self.individuals.sort(key=lambda x: x.fitness_val, reverse=True)

    def get_sorted_individuals(self) -> list:
        return sorted(self.individuals, key=lambda x: x.fitness_val, reverse=True)

    @staticmethod
    def sort_sample(sample: list) -> list:
        return sorted(sample, key=lambda x: x.fitness_val, reverse=True)

    def get_best(self) -> Individual:
        return self.get_sorted_individuals()[0]

    def mean(self):
        return sum(i.fitness_val for i in self.individuals)/self.size

    @staticmethod
    def init_population(size: int, task: Task):
        pop = Population(size)
        individuals = []
        for _ in range(size):
            individual = Individual([np.random.choice(np.arange(0, 2), p=[0.8, 0.2]) for _ in range(task.n_items)])
            individual.evaluate(task)
            individuals.append(individual)
        pop.replace_individuals(individuals)
        pop.sort_pop()
        return pop
