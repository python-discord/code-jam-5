import random
import math
import warnings

from src.world import World, world_regions, INDUSTRY_TO_CO2

VIRULENCE_FACTOR = 0.1

weather_event_types = ['flood', 'heatwave', 'wildfire']


# At the start of the game, sea level = 0
# Find out initial sea level
# Calculate sea level rise
# For each region, work out how many people died due to sea level rise (check pop >= 0)
# For each currently active virus, work out changes it makes to each region (calculate population changes first)


class WeatherEvent:
    def __init__(self, event_type="heatwave"):
        if not(event_type in weather_event_types):
            warnings.warn(str(event_type) + ' is not a recognised event type. Setting type to heatwave as default')
            event_type = "heatwave"

        if event_type == "heatwave":
            self.region = random.choice(world_regions)
            self.death_toll = random.randint(0, math.ceil(100 * (2 ** World.temperature_rise)))

        if event_type == "flood":
            self.region = random.choice(world_regions)
            self.death_toll = random.randint(0, math.ceil(1000 * (2 ** World.sea_level)))

        if event_type == "wildfire":
            self.region = random.choice(world_regions)
            self.death_toll = random.randint(0, math.ceil(10000 * (2 ** World.temperature_rise)))
            World.co2_concentation += 0.5


class PopulationChange:
    def __init__(self, world):
        self.regions = {}
        for region_name in world.regions:
            self.regions[region_name] = {"int_pop": world.regions[region_name].population,
                                    "fin_pop": 0,
                                    "percentage_change": 0}

    def __str__(self):
        """Prints the object in a human readable table format"""

        print("|Region              |Initial population  |Final population    |Percentage change   ")
        print("-------------------------------------------------------------------------------------")
        for region_name in self.regions:
            print("|" + region_name + " " * (20 - len(region_name)) +
                  "|" + str(self.regions[region_name]["int_pop"]) +
                  " " * (20 - len(str(self.regions[region_name]["int_pop"]))) +
                  "|" + str(self.regions[region_name]["fin_pop"]) +
                  " " * (20 - len(str(self.regions[region_name]["fin_pop"]))) +
                  "|" + str(self.regions[region_name]["percentage_change"])
                  )

    def set_final_population(self, region_name, fin_pop):
        int_pop = self.regions[region_name]["int_pop"]
        self.regions[region_name]["fin_pop"] = fin_pop

        if int_pop == 0:
            self.regions[region_name]["percentage_change"] = 0
        else:
            self.regions[region_name]["percentage_change"] = 100 * ((int_pop - fin_pop) / int_pop)


def simulate_world_changes(world, virus):
    """Simulates one turn of world changes, returning a modified world object"""
    industry_impacts = INDUSTRY_TO_CO2  # co2 impacts as given by industry id

    # implement virus affect on CO2
    for region in virus.affected_regions:
        world.co2_concentration += virus.impact * industry_impacts[virus.industry] * 0.001

    # calculate sea level rises
    initial_sea_level = world.sea_level
    sea_level_rise = (world.co2_concentration - 300) * 0.02
    world.sea_level += sea_level_rise

    population_change = PopulationChange(world)
    regions = world.regions.values()
    for region in regions:
        # assume population is evenly distributed between 1m and average elevation
        region.population -= math.ceil(((world.co2_concentration-300) * region.initial_population) / 7000000000)
        population_change.set_final_population(region.name, region.population)
        if region.population <= 0:
            region.population = 0
            region.destroyed = 1
            print(region.name + " has been wiped out")

    world.temperature_rise += (world.co2_concentration - 300) * 0.05



    return [world, population_change]


def simulate_virus_changes(world, virus):
    """Simulates one turn of a viruses spreading and being eliminated. Returns a modified virus object."""
    # each infected region will attempt to infect another region, this region may already be infected
    print(f'Let us see how far the virus spreads. Virus virulence is {virus.virulence} out of 100.')
    affected_regions_at_beginning_of_attack = virus.affected_regions.copy()
    for region in affected_regions_at_beginning_of_attack:
        print(f'Let us see how far the virus spreads from {region.name}.')
        for target in world.regions.values():
            if virus.virulence * VIRULENCE_FACTOR > random.randint(0, world.distance_between(region, target)):      # todo fix virulence to feel linked to factor
                if target in virus.affected_regions:
                    # country was already infected
                    continue
                else:
                    virus.affected_regions.append(target)
                    print(target.name + " is now infected with the virus!")
    print()

    # based on detectability each region has a random chance of stopping the virus
    print(f'Let us see which regions can kick the virus out. Virus detectability is {virus.detectability} out of 100.')
    affected_regions_at_beginning_of_defence = virus.affected_regions.copy()
    for region in affected_regions_at_beginning_of_defence:
        print(f'Let us see if {region.name} can kick the virus out.')
        if virus.detectability * 0.1 > random.randint(0, len(virus.affected_regions) + 10):
            virus.affected_regions.remove(region)
            print(region.name + " successfully got rid of the virus!")
        else:
            print(region.name + " could not get rid of the virus!")
        print()
    return virus


def simulate_turn(world, virus):
    """"Simulates one turn of world changes, returning a list comprising of a world and virus object"""
    print('-'*100)
    print('The turn is to begin.')
    print(
        'Currently infected regions at beginning of turn:',
        ', '.join([region.name for region in virus.affected_regions])
    )
    print()
    world_and_population_change = simulate_world_changes(world, virus)
    world = world_and_population_change[0]
    population_change = world_and_population_change[1]
    virus = simulate_virus_changes(world, virus)

    print('The turn has ended.')
    print('-'*100)
    if not virus.affected_regions:
        print('The virus has been wiped out!')
        return
    else:
        print(
            'Currently infected regions at end of turn:',
            ', '.join([region.name for region in virus.affected_regions])
        )
        print()
        return [world, virus, population_change]


# model extreme weather events
# def simulate_weather_events():
#
#    number_of_events = math.floor(random.randint(0, 21 + (earth.sea_level * earth.co2_concentration * 0.01)) / 20)
#    for i in range(number_of_events):
#        event = WeatherEvent(random.choice(weather_event_types))
#        earth.region[event.region].population -= event.death_toll
#        if earth.region[event.region].population <= 0:
#            earth.region[event.region].population = 0
#            earth.region[event.region].destroyed = 1
