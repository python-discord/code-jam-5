import itertools


class Industry:
    """Specify stats for various industries"""

    def __init__(self, name, impact):
        self.name = name
        self.impact = impact


class Region:
    """Main class for region"""

    INDUSTRIES = {
        'chem_manu': Industry('Chemical Manufacturing', 30),
        'car_prod': Industry('Vehicle Production', 50),
        'powerplant': Industry('Power Plant', 70),
    }

    def __init__(self, name, detectability, destroyed=0):
        self.name = name
        self.detectability = detectability
        self.destroyed = destroyed


class World:

    REGIONS = {
        'Canada': Region('Canada', 70),
        'USA': Region('USA', 90),
        'Mexico': Region('Mexico', 30),
        'Peru': Region('Peru', 20),
        'Brazil': Region('Brazil', 30),
        'Greenland': Region('Greenland', 10),
        'West Europe': Region('West Europe', 80),
        'North Africa': Region('North Africa', 10),
        'South Africa': Region('South Africa', 20),
        'East Europe': Region('East Europe', 40),
        'Russia': Region('Russia', 80),
        'Middle East': Region('Middle East', 40),
        'China': Region('China', 90),
        'India': Region('India', 50),
        'Indonesia': Region('Indonesia', 50),
        'Australia': Region('Australia', 70),
        'New Zealand': Region('New Zealand', 60),
    }

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

    def distance_between(self, region1, region2):
        shortest_path = self._find_shortest_path(region1, region2)
        distance = sum(self.DISTANCES[region1][region2] for region1, region2 in self._pairwise(shortest_path))
        return distance

    def _find_shortest_path(self, start, end, path=None):
        if not path:
            path = []
        path = path + [start]
        if start == end:
            return path
        if start not in self.DISTANCES:
            return None
        shortest = None
        for node in self.DISTANCES[start]:
            if node not in path:
                newpath = self._find_shortest_path(node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest

    def _pairwise(self, iterable):
        """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
        a, b = itertools.tee(iterable)
        next(b, None)
        return zip(a, b)



