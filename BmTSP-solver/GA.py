import random
from Problemmodel import include_percent_all_points
from utils import random_partition, remove_charging_stations, needed_time
from heuristics import greedy
from tqdm import tqdm

time_penalty_skip = -10000000000000000000000000
time_penalty_battery_underflow = 100000000000000000000000


class Chromosom:
    def __init__(self):
        self.genes = []
        self.fitness = 0
        self.isSolution = False

    def generate_genes(self, points, number_of_UAVs):
        self.genes = []
        if random.random() < 0.8:
            self.genes = random_partition(number_of_UAVs, points)
        else:
            self.genes = greedy(points, number_of_UAVs).solution

    def calc_fitness(self, points):
        self.fitness = 0
        w = include_percent_all_points(self.genes, points)
        if w != 1:
            self.isSolution = True
            return 0
        self.fitness = needed_time(self.genes)
        self.isSolution = True
        return self.fitness


    def mutate_in_route(self):
        route_index = random.randint(0, len(self.genes) - 1)
        route = self.genes[route_index]
        if len(route) == 0:
            return
        random_index_1 = random.randint(0, len(route) - 1)
        random_index_2 = random.randint(0, len(route) - 1)

        route[random_index_1], route[random_index_2] = route[random_index_2], route[random_index_1]

    def swap_mutation(self):
        route_index_1 = random.randint(0, len(self.genes) - 1)
        route_index_2 = random.randint(0, len(self.genes) - 1)
        route_1 = self.genes[route_index_1]
        route_2 = self.genes[route_index_2]
        if len(route_1) == 0 or len(route_2) == 0:
            return
        random_index_1 = random.randint(0, len(route_1) - 1)
        random_index_2 = random.randint(0, len(route_2) - 1)

        route_1[random_index_1], route_2[random_index_2] = route_2[random_index_2], route_1[random_index_1]

    def insertion_mutation(self):
        self.genes = remove_charging_stations(self.genes)
        route_index_1 = random.randint(0, len(self.genes) - 1)
        route_index_2 = random.randint(0, len(self.genes) - 1)
        route_1 = self.genes[route_index_1]
        route_2 = self.genes[route_index_2]

        if len(route_1) == 0 or len(route_2) == 0:
            return

        route_2.insert(random.randint(0, len(route_2)), route_1.pop(random.randint(0, len(route_1) - 1)))

    def mutate(self, points, mutation_route_p, mutation_between_route_p, mutation_iter):
        for i in range(mutation_iter):
            if random.random() < mutation_route_p:
                if random.random() < 0.5:
                    self.swap_mutation()
                else:
                    self.insertion_mutation()

            if random.random() < mutation_between_route_p:
                self.mutate_in_route()
        self.calc_fitness(points)

    def crossover(self, other, points):
        child = Chromosom()
        child.genes = []
        already_used = set()
        for i in range(min(len(self.genes), len(other.genes))):
            child.genes.append([])
            for j in range(max(len(self.genes), len(other.genes))):
                if j >= len(self.genes[i]) and j >= len(other.genes[i]):
                    break
                if j >= len(self.genes[i]):
                    if other.genes[i][j] in already_used:
                        continue
                    child.genes[i].append(other.genes[i][j])
                elif j >= len(other.genes[i]):
                    if self.genes[i][j] in already_used:
                        continue
                    child.genes[i].append(self.genes[i][j])
                else:
                    if random.random() < 0.5:
                        child.genes[i].append(self.genes[i][j])
                    else:
                        child.genes[i].append(other.genes[i][j])
                already_used.add(child.genes[i][-1])
        child.calc_fitness(points)
        return child


class Population:
    def __init__(self):
        self.chromosomes = []

    def generate_chromosomes(self, points, number_of_UAVs, population_size):
        for i in range(population_size):
            self.chromosomes.append(Chromosom())
            self.chromosomes[i].generate_genes(points,  number_of_UAVs)
            self.chromosomes[i].calc_fitness(points)

        self.chromosomes.sort(key=lambda x: (not x.isSolution, x.fitness))

    def print_all_chromosomes(self):
        print("Population: \n \n")
        for i in self.chromosomes:
            if (i.isSolution):
                print(i.fitness)

    def update_population(self, points, leaving_percent, mutation_percent, crossover_percent=0.3,
                          number_of_UAVs=3):
        self.chromosomes.sort(key=lambda x: (not x.isSolution, x.fitness))
        old_population_size = len(self.chromosomes)
        leaving_count = int(old_population_size * leaving_percent)
        population = self.chromosomes[:leaving_count]

        mutation_count = int(old_population_size * mutation_percent)
        for i in range(mutation_count):
            population.append(random.choice(self.chromosomes[:leaving_count]))
            population[-1].mutate(points, 0.5, 0.5, 20)

        crossover_count = int(old_population_size * crossover_percent)
        for i in range(crossover_count):
            population.append(random.choice(self.chromosomes))
            population[-1].crossover(random.choice(self.chromosomes), points)

        for i in range(len(population), old_population_size):
            population.append(Chromosom())
            population[-1].generate_genes(points, number_of_UAVs)
            population[-1].calc_fitness(points)

        self.chromosomes = population
        self.chromosomes.sort(key=lambda x: (not x.isSolution, x.fitness))

    def get_best_chromosome(self):
        self.chromosomes.sort(key=lambda x: (not x.isSolution, x.fitness))
        print("best fitness: ", self.chromosomes[0].fitness)
        print("worst fitness: ", self.chromosomes[-1].fitness)
        print("worst time: ", needed_time(self.chromosomes[-1].genes))
        return self.chromosomes[0]


class GA:
    def __init__(self, points, charging_stations, number_of_UAVs, population_size, left_percent, mutation_percent,
                 crossover_percent, iterations):
        print(number_of_UAVs)
        self.population = Population()
        self.population.generate_chromosomes(points, number_of_UAVs, population_size)
        self.population.update_population(points, left_percent, mutation_percent, crossover_percent,
                                          number_of_UAVs)
        for i in tqdm(range(iterations)):
            self.population.update_population(points, left_percent, mutation_percent,
                                              crossover_percent, number_of_UAVs)

    def get_best_chromosome(self):
        return self.population.get_best_chromosome()
