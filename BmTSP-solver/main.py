from utils import needed_time, battery_underflow
from Problemmodel import Point
import random
import argparse
import matplotlib.pyplot as plt
from solve import solve
import time


def standard_main(x, y, n_points, m_charge, n_uavs, n_generations, n_population, left, mutation, crossover,
                  show_graph=False, save_graph=False):
    points = []
    charging_stations = []
    for i in range(n_points):
        points.append(Point(random.randint(0, x), random.randint(0, y)))

    for i in range(m_charge):
        charging_stations.append(Point(random.randint(0, x), random.randint(0, y), True))

    start_time = time.time()
    p = solve(points, charging_stations, n_uavs, n_population, left, mutation, crossover, n_generations)
    end_time = time.time()
    for i in range(len(p)):
        if (len(p[i]) == 0):
            continue
        p[i].append(p[i][0])

    plt.figure(figsize=(10, 10))
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.scatter([i.x for i in points], [i.y for i in points], color="red")
    plt.scatter([i.x for i in charging_stations], [i.y for i in charging_stations], color="blue")
    plt.title("Is Solution: " + ("no" if battery_underflow(p) < 0 else "yes") + ", Compute Time: " + "{:.2f} s".format(
        end_time - start_time), loc='left')
    for i in p:
        print([j.x for j in i], [j.y for j in i])
        plt.plot([j.x for j in i], [j.y for j in i])

    print("P:", p)
    print("best time", needed_time(p))
    print("unterschleif", battery_underflow(p))
    print("needed compute time: ", end_time - start_time)

    if save_graph:
        plt.savefig("graph.pdf")
        print("graph saved under: " + "graph.pdf")
    if show_graph:
        plt.show()




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--x', type=int, default=100, help='x size of the map')
    parser.add_argument('--y', type=int, default=100, help='y size of the map')
    parser.add_argument('--n_points', type=int, default=30, help='number of points')
    parser.add_argument('--m_charge', type=int, default=15, help='number of charging stations')
    parser.add_argument('--n_uavs', type=int, default=5, help='number of UAVs')
    parser.add_argument('--n_generations', type=int, default=30, help='number of generations')
    parser.add_argument('--n_population', type=int, default=1000, help='number of population')
    parser.add_argument('--leftp', type=float, default=0.3, help='left percent')
    parser.add_argument('--mutationp', type=float, default=0.3, help='mutation percent')
    parser.add_argument('--crossoverp', type=float, default=0.3, help='crossover percent')
    parser.add_argument('--show_graph', type=bool, default=False, help='show graph')
    parser.add_argument('--save_graph', type=bool, default=True, help='save graph')
    parser.add_argument('--iter', type=int, default=10, help='iterations')
    parser.add_argument('--start_gen', type=int, default=50, help='start generation')
    parser.add_argument('--end_gen', type=int, default=200, help='end generation')
    parser.add_argument('--step', type=int, default=10, help='step size')

    args = parser.parse_args()

    standard_main(args.x, args.y, args.n_points, args.m_charge, args.n_uavs, args.n_generations, args.n_population,
                  args.leftp, args.mutationp, args.crossoverp, args.show_graph, args.save_graph)
