from GA import GA, include_percent_all_points
from utils import needed_time_path, battery_underflow
import itertools

OPTIMIZATION_ITERATIONS = 1000

def ga_phase(points, charging_stations, number_of_UAVs, population_size, left_percent, mutation_percent,
             crossover_percent, iterations):
    ga = GA(points, charging_stations, number_of_UAVs, population_size, left_percent, mutation_percent,
            crossover_percent, iterations)
    return ga.get_best_chromosome().genes


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
        for j in range(len(route)-1, 0, -1):
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
        

def solve(points, charging_stations, number_of_UAVs, population_size, left_percent, mutation_percent, crossover_percent,
           iterations):
    best_chromosome = ga_phase(points, charging_stations, number_of_UAVs, population_size, left_percent,
                               mutation_percent, crossover_percent, iterations)

    # check if the best chromosome is a solution
    if include_percent_all_points(best_chromosome, points) != 1:
        print("The best chromosome is not a solution")
        return []

    for i in range(len(best_chromosome)):
        print("Charging station insertion for route", i)
        best_chromosome[i] = charging_station_insertion(best_chromosome[i], charging_stations)

    return best_chromosome
