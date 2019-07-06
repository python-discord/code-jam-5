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

    def __init__(self, name, elevation, population):
        self.name = name
        self.elevation = elevation
        self.population = population
        self.initial_population = population
        self.destroyed = 0


world_regions = ['USA', 'Canada', 'Mexico', 'Peru', 'Argentina', 'Brazil', 'West Europe', 'India', 'Australia',
           'North Africa', 'South Africa', 'East Europe', 'Madagascar', 'Indonesia', 'Japan', 'Middle East',
           'New Zealand', 'China', 'Greenland', 'Cuba']



class World:

    DISTANCES = {
        'Canada': {'Greenland': 9, 'USA': 3},
        'USA': {'West Europe': 14, 'Mexico': 4, 'Cuba': 4},
        'Cuba': {'Mexico': 2},
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

    def __init__(self):
        self.sea_level = 0
        self.co2_concentration = 300  # ppm
        self.temperature_rise = 0
        self.regions = self._load_regions()

    def _load_regions(self):
        regions = {}
        with open('data/regions.txt', 'r') as region_file:
            for line in region_file:
                split_line = line.split('\t')
                name = split_line[0]
                average_elevation = split_line[1]
                population = split_line[2]
                regions[name] = Region(name, average_elevation, population)

        return regions

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


earth = World()
