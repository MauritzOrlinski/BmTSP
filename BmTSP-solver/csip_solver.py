from GA import GA, include_percent_all_points
from utils import needed_time_path, battery_underflow
import itertools
import random
from Problemmodel import include_percent_all_points
from utils import random_partition, remove_charging_stations, needed_time
from heuristics import greedy
from tqdm import tqdm

OPTIMIZATION_ITERATIONS = 1000


def charging_station_insertion(route, charging_stations):
    optimization_iterations = OPTIMIZATION_ITERATIONS
    if battery_underflow([route]) == 0:
        print("No Underflow")
        return route

    possible_charging_stations = charging_stations.copy()
    possible_charging_stations.append(None)
    print(len(route))
    found = False
    max_solution = route
    max_b = battery_underflow([route])
    min_time = needed_time_path(route)
    for i in itertools.permutations(possible_charging_stations, len(route)):
        if found:
            if optimization_iterations == 0:
                break
            optimization_iterations -= 1

        new_route = route.copy()
        for j in range(len(route) - 1, 0, -1):
            if i[j] is not None:
                new_route.insert(j + 1, i[j])
        if battery_underflow([new_route]) == 0 and not found:
            max_solution = new_route
            found = True
        elif battery_underflow([new_route]) == 0 and found and needed_time_path(new_route) < min_time:
            max_solution = new_route
            min_time = needed_time_path(new_route)

        if battery_underflow([new_route]) > max_b:
            max_solution = new_route
            max_b = battery_underflow([new_route])
    if not found:
        print("No solution found")
    else:
        print("Solution found")
    return max_solution


class Chromosom:
    def __init__(self, charging_stations):
        self.route = []
        self.battery_stops = []
        self.fitness = 0
        self.isSolution = False
        self.charging_stations = charging_stations

    def generate_genes(self, route):
        self.route = route
        self.battery_stops = [[] for _ in range(len(route) + 1)]

    def calc_fitness(self):
        new_route = self.insert_chargingstations()
        self.fitness = battery_underflow([new_route])
        if self.fitness == 0:
            self.isSolution = True
            self.fitness = needed_time([new_route])
        else:
            self.isSolution = False
        return self.fitness

    def mutate_remove_charging_station(self):
        rand_index = random.randint(0, len(self.battery_stops) - 1)
        if len(self.battery_stops[rand_index]) == 0:
            return
        self.battery_stops[rand_index].pop(random.randint(0, len(self.battery_stops[rand_index]) - 1))

    def mutate_add_charging_station(self):
        rand_index = random.randint(0, len(self.battery_stops) - 1)

        possible_charging_stations = [i for i in self.charging_stations if i not in self.battery_stops[rand_index]]
        if len(possible_charging_stations) == 0:
            return
        charging_station = random.choice(possible_charging_stations)
        self.battery_stops[rand_index].insert(random.randint(0, len(self.battery_stops[rand_index])), charging_station)

    def crossover(self, other):
        new_chromosom = Chromosom(self.charging_stations)
        new_chromosom.route = self.route
        for i in range(len(self.battery_stops)):
            if random.random() < 0.5:
                new_chromosom.battery_stops.append(self.battery_stops[i])
            else:
                new_chromosom.battery_stops.append(other.battery_stops[i])
        new_chromosom.calc_fitness()
        return new_chromosom

    def mutate(self):
        if self.isSolution:
            self.mutate_remove_charging_station()
        else:
            self.mutate_add_charging_station()
        self.calc_fitness()

    def insert_chargingstations(self):
        new_route = self.route.copy()
        for i in range(len(self.route), 0, -1):
            for j in self.battery_stops[i]:
                new_route.insert(i, j)
        return new_route


class Population:
    def __init__(self):
        self.chromosomes = []

    def generate_chromosomes(self, route, charging_points, population_size):
        for i in range(population_size):
            self.chromosomes.append(Chromosom(charging_points))
            self.chromosomes[i].generate_genes(route)
            self.chromosomes[i].calc_fitness()
        self.chromosomes.sort(key=lambda x: (not x.isSolution, x.fitness if x.isSolution else -x.fitness))
    def print_all_chromosomes(self):
        print("Population: \n Best: ", self.chromosomes[0],"\n")
        for i in self.chromosomes:
            print(i.fitness)

    def update_population(self, route, charging_stations, leaving_percent, mutation_percent, crossover_percent=0.3):
        self.chromosomes.sort(key=lambda x: (not x.isSolution, x.fitness if x.isSolution else -x.fitness))
        old_population_size = len(self.chromosomes)
        leaving_count = int(old_population_size * leaving_percent)
        population = self.chromosomes[:leaving_count]

        mutation_count = int(old_population_size * mutation_percent)
        for i in range(mutation_count):
            population.append(random.choice(self.chromosomes[:leaving_count]))
            population[-1].mutate()
        crossover_count = int(old_population_size * crossover_percent)
        for i in range(crossover_count):
            population.append(random.choice(self.chromosomes).crossover(random.choice(self.chromosomes)))

        for i in range(len(population), old_population_size):
            population.append(Chromosom(charging_stations))
            population[-1].generate_genes(route)
            population[-1].calc_fitness()

        self.chromosomes = population
        self.chromosomes.sort(key=lambda x: (not x.isSolution, x.fitness if x.isSolution else -x.fitness))

    def get_best_chromosome(self):
        self.chromosomes.sort(key=lambda x: (not x.isSolution, x.fitness if x.isSolution else -x.fitness))
        return self.chromosomes[0]


def charging_station_insertion_GA(route, charging_stations, iterations, population_size, leaving_percent, mutation_percent, crossover_percent):
    population = Population()
    population.generate_chromosomes(route, charging_stations, population_size)
    population.update_population(route, charging_stations, leaving_percent, mutation_percent, crossover_percent)
    for _ in tqdm(range(iterations)):
        population.update_population(route, charging_stations, leaving_percent, mutation_percent, crossover_percent)
    print("final fitness: ", population.get_best_chromosome().fitness)
    return population.get_best_chromosome().insert_chargingstations()
