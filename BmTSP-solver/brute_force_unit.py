import random
from Problemmodel import battery_cost, Point
from utils import needed_time, battery_underflow
from sys import maxsize

MAX_SEARCH_DEPTH = 10


def check_battery_underflow(route):
    underflow = 0
    battery = 100
    for i in range(len(route) - 1):
        battery -= battery_cost(route[i], route[(i + 1)])
        if battery < 0:
            underflow += battery
        if route[(i + 1)].is_charging_station:
            battery = 100
    return underflow


def circle_in_charging_stations(route, charging_stations, number_of_points):
    if len(route) > number_of_points * (len(charging_stations) + 1) + 1:
        return True
    sub = []
    for i in range(len(route)):
        if not route[i].is_charging_station:
            sub = []
        else:
            if route[i] in sub:
                return True
            sub.append(route[i])
    return False


def solve_brute_force(points, charging_stations, number_of_UAVs):
    best_solution = []
    min_time = maxsize
    number_of_checks = 0
    def brute_force_recursive(route, points_sub, number_of_UAVs):
        nonlocal best_solution
        nonlocal min_time
        nonlocal number_of_checks

        if len(points_sub) == 0:
            if battery_underflow(route) == 0:
                time = needed_time(route)
                if time < min_time:
                    best_solution = [i.copy() for i in route]
                    min_time = time
            return
        number_of_checks += 1
        if number_of_checks % 10000 == 0:
            print("Number of checks:", number_of_checks)

        for i in range(len(route)):
            if check_battery_underflow(route[i]) < 0:
                return
            elif circle_in_charging_stations(route[i], charging_stations, len(points_sub)):
                return

        for i in range(len(points_sub)):
            for j in range(len(route)):
                route[j].append(points_sub[i])
                new_points_sub = points_sub.copy()
                new_points_sub.pop(i)
                brute_force_recursive(route, new_points_sub, number_of_UAVs)
                route[j].pop()

        for i in range(len(charging_stations)):
            for j in range(len(route)):
                route[j].append(charging_stations[i])
                new_points_sub = points_sub.copy()
                brute_force_recursive(route, new_points_sub, number_of_UAVs)
                route[j].pop()

    brute_force_recursive([[] for _ in range(number_of_UAVs)], points, number_of_UAVs)
    print("Solution:", best_solution)
    return best_solution