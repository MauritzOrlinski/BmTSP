from GA import GA, include_percent_all_points
from utils import needed_time_path, battery_underflow
import itertools
import csip_solver


def ga_phase(points, charging_stations, number_of_UAVs, population_size, left_percent, mutation_percent,
             crossover_percent, iterations):
    ga = GA(points, charging_stations, number_of_UAVs, population_size, left_percent, mutation_percent,
            crossover_percent, iterations)
    return ga.get_best_chromosome().genes


def charging_station_insertion(route, charging_stations):
    csip_solver.charging_station_insertion(route, charging_stations)
        

def solve(points, charging_stations, number_of_UAVs, population_size, left_percent, mutation_percent, crossover_percent,
           iterations_mtsp, iterations_csip, use_ga=True):
    best_chromosome = ga_phase(points, charging_stations, number_of_UAVs, population_size, left_percent,
                               mutation_percent, crossover_percent, iterations_mtsp)

    # check if the best chromosome is a solution
    if include_percent_all_points(best_chromosome, points) != 1:
        print("The best chromosome is not a solution")
        return []

    for i in range(len(best_chromosome)):
        print("Charging station insertion for route", i)
        if use_ga:
            best_chromosome[i] = csip_solver.charging_station_insertion_GA(best_chromosome[i], charging_stations,
                                                                          iterations_csip, population_size, left_percent,
                                                                          mutation_percent, crossover_percent)
        else:
            best_chromosome[i] = charging_station_insertion(best_chromosome[i], charging_stations)

    return best_chromosome
