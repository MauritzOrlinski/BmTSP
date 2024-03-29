battery_consumption = 0.8


def battery_cost(a, b):
    return a.dist(b) * battery_consumption


class Point:
    def __init__(self, x, y, is_charging_station=False):
        self.x = x
        self.y = y
        self.is_charging_station = is_charging_station

    def dist(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


    def __repr__(self):
        return "Point({}, {})".format(self.x, self.y)

    def __eq__(self, other):
        if other is None or not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


def include_percent_all_points(gene, points):
    include_count = 0
    for i in points:
        included = False
        for j in gene:
            if i in j:
                include_count += 1
                included = True
                break
    return include_count/len(points)

