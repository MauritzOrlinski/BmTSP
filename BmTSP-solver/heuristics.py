import random
from Problemmodel import Point

class greedy:
    def __init__(self, points: list[Point], n):
        self.solution = []
        points = points.copy()
        random.shuffle(points)
        for i in range(n):
            self.solution.append([])
        while len(points) > 0:
            for i in range(n):
                if len(self.solution[i]) == 0:
                    self.solution[i].append(points.pop(0))
                else:
                    if len(points) == 0:
                        break
                    next_point = points[0]
                    min_dist = self.solution[i][-1].dist(next_point)
                    for point in points:
                        dist = self.solution[i][-1].dist(point)
                        if dist < min_dist:
                            min_dist = dist
                            next_point = point
                    self.solution[i].append(next_point)
                    points.remove(next_point)


