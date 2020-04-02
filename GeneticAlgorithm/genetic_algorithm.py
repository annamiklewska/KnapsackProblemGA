import logging
import statistics

from common import *
from data_importer import read_csv
import matplotlib.pyplot as plt
from time import time
import numpy as np

logging.basicConfig(level=logging.INFO)


class GeneticAlgorithm:
    def __init__(self,
                 file_name: str = "items.csv",
                 tournament_size: int = 10,
                 pop_size: int = 50,
                 crossover_rate: float = 0.8,
                 mutation_rate: float = 0.01,
                 elitism_rate: float = 0.5
                 ) -> None:
        self.task = read_csv(file_name)
        self.n_items = self.task.n_items
        self.max_weight = self.task.max_weight
        self.max_size = self.task.max_size
        self.pop_size = pop_size
        self.tournament_size = tournament_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.pop = Population.init_population(pop_size, self.task)
        self.elitism_rate = elitism_rate
        self.best_per_pop = []
        self.mean_per_pop = []
        self.time_to_execute = 0
        logging.info(
            """ INITIAL CONFIG:
            file name: {0}
            pop size: {1}
            tournament size: {2}
            crossover rate: {3}
            mutation rate: {4}
            pop to keep: {5}""".format(
                file_name, str(self.pop_size), str(tournament_size),
                str(crossover_rate), str(mutation_rate), str(elitism_rate)))

    def tournament(self) -> Individual:
        participants = Population.sort_sample(random.sample(self.pop.individuals, self.tournament_size))
        return participants[0]

    def crossover(self, parent1: Individual, parent2: Individual) -> Individual:
        if random.random() < self.crossover_rate:
            # cut_point = random.randint(1, self.n_items - 1)
            cut_point = int(0.5 * self.n_items)
            child = Individual(parent1.backpack[0: cut_point] + parent2.backpack[cut_point: self.n_items])
            child.evaluate(self.task)
            return child
        else:
            return parent1

    def mutate(self, individual: Individual) -> None:
        genes = int(self.n_items * self.mutation_rate)
        indexes = random.sample(range(0, self.n_items), genes)
        for idx in indexes:
            if individual.backpack[idx] == 0:
                individual.backpack[idx] = 1
            else:
                individual.backpack[idx] = 0

    def draw(self, domain: int) -> None:
        domain = [_ for _ in range(domain)]
        plt.plot(domain, self.best_per_pop)
        plt.title("Best individuals")
        plt.ylabel("fitness of best individual")
        plt.xlabel("generations")
        plt.show()
        plt.plot(domain, self.mean_per_pop)
        plt.title("Mean of all individuals")
        plt.ylabel("mean fitness of individuals")
        plt.xlabel("generations")
        plt.show()
        logging.info("Best and mean fitness values of individuals plots generated")

    def run(self, iterations: int) -> Individual:
        logging.info("Time: start")
        start_time = time()
        self.best_per_pop = []
        for it in range(iterations):
            new_pop = Population(self.pop_size)
            new_pop.add_individuals(self.pop.individuals[0:int(self.elitism_rate * self.pop_size)])
            for _ in range(int(self.elitism_rate * self.pop_size), self.pop_size):
                parent1 = self.tournament()
                parent2 = self.tournament()
                child = self.crossover(parent1, parent2)
                self.mutate(child)
                child.evaluate(self.task)
                new_pop.add_individual(child)
            new_pop.sort_pop()
            self.best_per_pop.append(new_pop.individuals[0].fitness_val)
            self.mean_per_pop.append(self.pop.mean())
            self.pop = new_pop
        self.time_to_execute = round(time() - start_time, 4)
        logging.info("Time to execute: " + str(self.time_to_execute) + "[s]")
        return self.pop.get_best()

    @staticmethod
    def run_test(n_tests: int, generations: int) -> None:
        best_individuals = []
        best_per_pop = []
        times = []
        for _ in range(n_tests):
            ga = GeneticAlgorithm(file_name="items.csv",
                                  pop_size=100,
                                  tournament_size=30,
                                  crossover_rate=0.8,
                                  mutation_rate=0.002,
                                  elitism_rate=0.2)
            best_individuals.append(ga.run(generations))
            best_per_pop.append(ga.best_per_pop)
            times.append(ga.time_to_execute)
        result = np.apply_along_axis(lambda x: statistics.mean(x), 0, np.array([bpp for bpp in best_per_pop]))
        avg_best = result[generations - 1]
        domain = [_ for _ in range(generations)]
        plt.plot(domain, result)
        plt.title("Best individuals")
        plt.ylabel("Average fitness of best individual")
        plt.xlabel("generations")
        plt.show()
        logging.info("Show summary plot")
        logging.info("Average times for {0} generations: {1} [s]".format(generations, statistics.mean(times)))
        logging.info("Average best individual's fitness value: " + "{:,}".format(avg_best))


if __name__ == "__main__":
    GeneticAlgorithm.run_test(n_tests=5, generations=500)
