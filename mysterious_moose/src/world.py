import itertools

class Region:
    """Main class for region"""
    def __init__(self):
        self.name = ''
        self.detectability = 0


class Industry:
    """Specify stats for various industries"""

    def __init__(self, name, impact):
        self.name = ''
        self.impact = 0


chem_manu = Industry('Chemical Manufacturing', 30)
car_prod = Industry('Vehicle Production', 50)
powerplant = Industry('Power Plant', 70)



class World:
    def __init__(self):
        pass

    def distance_between(self, graph, region1, region2):
        shortest_path = self._find_shortest_path(graph, region1, region2)
        distance = sum(graph[region1][region2] for region1, region2 in self._pairwise(shortest_path))
        return distance

    def _find_shortest_path(self, graph, start, end, path=None):
        if not path:
            path = []
        path = path + [start]
        if start == end:
            return path
        if start not in graph:
            return None
        shortest = None
        for node in graph[start]:
            if node not in path:
                newpath = self._find_shortest_path(graph, node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest

    def _pairwise(self, iterable):
        """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
        a, b = itertools.tee(iterable)
        next(b, None)
        return zip(a, b)



DISTANCES = {
    'Canada': {'Greenland': 9, 'USA': 3},
    'USA': {'West Europe': 14, 'Mexico': 4},
    'Mexico': {'North Africa': 16, 'Peru': 4},
    'Peru': {'Brazil': 4, 'Argentina': 5},
    'Brazil': {'South Africa': 11},
    'Greenland': {'West Europe': 6},
    'West Europe': {'East Europe': 2, 'North Africa': 5},
    'North Africa': {'South Africa': 5},
    'South Africa': {'Madagascar': 3},
    'East Europe': {'Russia': 8, 'Middle East': 5},
    'Russia': {'China': 6},
    'Middle East': {'China': 6, 'India': 4},
    'China': {'Japan': 4},
    'India': {'Indonesia': 6},
    'Indonesia': {'Australia': 5},
    'Australia': {'New Zealand': 5},
}

