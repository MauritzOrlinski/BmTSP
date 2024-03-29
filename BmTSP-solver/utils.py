import random
from Problemmodel import battery_cost, Point, include_percent_all_points


def random_partition(k, iterable):
  results = [[] for i in range(k)]
  for value in iterable:
    x = random.randrange(k)
    results[x].append(value)
  return results


def remove_charging_stations(gene):
    for i in range(len(gene)):
        gene[i] = [j for j in gene[i] if not j.is_charging_station]
    return gene


def insert_closest_charging_stations(gene, charging_stations):
    if battery_underflow(gene) < 0:
        return gene
    for i in range(len(gene) - 1):
        battery = 100

        j = 0
        while j < len(gene[i]) - 1:
            battery_next = battery - battery_cost(gene[i][j], gene[i][j + 1])
            if battery_next < 0:
                gene[i].insert(j + 1, closest_charingstation(gene[i][j], charging_stations))
                battery = 100
            else:
                battery = battery_next
            j += 1
    return gene


def battery_underflow(gene):
    underflow = 0
    for i in gene:
        if len(i) == 0:
            continue
        battery = 100
        for j in range(len(i)):
            battery -= battery_cost(i[j], i[(j + 1)%len(i)])
            if battery < 0:
                underflow += battery
            if i[(j + 1)%len(i)].is_charging_station:
                battery = 100
    return underflow


def needed_time_path(route):
    if len(route) <= 1:
        return 0
    time = 0
    for i in range(len(route)):
        time += route[i].dist(route[i-1])
    return time

def needed_time(gene):
    k = []
    for i in gene:
        time = 0
        if len(i) == 0:
            continue
        for j in range(len(i) - 1):
            time += i[j].dist(i[j + 1])
        time += i[-1].dist(i[0])
        k.append(time)
    return 0 if len(k) == 0 else max(k)

def closest_charingstation(point, charging_stations):
    return min(charging_stations, key=lambda x: -point.dist(x))
