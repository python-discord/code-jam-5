import itertools


INDUSTRIES = ['Chemical Manufacturing', 'Vehicle Production', 'Power Plant']

INDUSTRY_TO_CO2 = {0: 30, 1: 50, 2: 70}


class Region:
    """Main class for region"""

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
        'USA': {'West Europe': 14, 'Mexico': 4, 'Cuba': 4, 'Canada': 9},
        'Cuba': {'Mexico': 2, 'USA': 4},
        'Mexico': {'North Africa': 16, 'Peru': 4, 'USA': 4, 'Cuba': 2},
        'Peru': {'Brazil': 4, 'Argentina': 5, 'Mexico': 4},
        'Brazil': {'South Africa': 11, 'Peru': 4},
        'Argentina': {'Peru': 5},
        'Greenland': {'West Europe': 6, 'Canada': 9},
        'West Europe': {'East Europe': 2, 'North Africa': 5, 'USA': 14, 'Greenland': 6},
        'North Africa': {'South Africa': 5, 'Mexico': 16, 'West Europe': 5},
        'South Africa': {'Madagascar': 3, 'Brazil': 11, 'North Africa': 5},
        'Madagascar': {'South Africa': 3},
        'East Europe': {'Russia': 8, 'Middle East': 5, 'West Europe': 2},
        'Russia': {'China': 6, 'East Europe': 8},
        'Middle East': {'China': 6, 'India': 4, 'East Europe': 5},
        'China': {'Japan': 4, 'Russia': 6, 'Middle East': 6},
        'Japan': {'China': 4},
        'India': {'Indonesia': 6, 'Middle East': 4},
        'Indonesia': {'Australia': 5, 'India': 6},
        'Australia': {'New Zealand': 5, 'Indonesia': 5},
        'New Zealand': {'Australia': 5},
    }

    def __init__(self):
        self.sea_level = 0
        self.co2_concentration = 300  # ppm
        self.temperature_rise = 0
        self.regions = self._load_regions()
        self._population = 0

    @property
    def population(self):
        population = 0
        for region in self.regions:
            population += self.regions[region].population

        self._population = population
        return population

    def _load_regions(self):
        regions = {}
        with open('../data/regions.txt', 'r') as region_file:
            for line in region_file:
                split_line = line.split('\t')
                name = split_line[0]
                average_elevation = split_line[1]
                population = int(split_line[2])
                regions[name] = Region(name, average_elevation, population)

        return regions

    def distance_between(self, region1, region2):
        region1_name = region1.name
        region2_name = region2.name
        shortest_path = self._find_shortest_path(region1_name, region2_name)
        distance = sum(
            self.DISTANCES[region1_name][region2_name]
            for region1_name, region2_name in self._pairwise(shortest_path)
        )
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

