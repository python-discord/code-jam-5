import random
import math
import warnings

from mysterious_moose.src.world import World, world_regions, earth

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


def simulate_world_changes(world, virus):
    industry_impacts = {0: 30, 1: 50, 2: 70}  # co2 impacts as given by industry id
    # calculate sea level rises
    initial_sea_level = world.sea_level
    sea_level_rise = (world.co2_concentration - 300) * 0.02
    world.sea_level += sea_level_rise

    for region in world.regions:
        # assume population is evenly distributed between 1m and average elevation
        region.population -= math.ceil(((world.co2_concentration-300) * region.initial_population) / 7000000000)
        if region.population <= 0:
            region.population = 0
            region.destroyed = 1

    world.temperature_rise += (world.co2_concentration - 300) * 0.05

    for region in virus.affected_regions:
        world.co2_concentration += virus.impact * industry_impacts[virus.industry] * 0.001

    return world


def simulate_virus_changes(world, virus):

    # each infected region will attempt to infect another region, this region may already be infected
    for region in virus.affected_regions:
        target = random.choice(world_regions)
        if virus.virulence > random.randint(0, World.shortest_distance(region, target)):
            virus.affected_regions.append(target)

    # based on detectability each region has a random chance of stopping the virus
    for region in virus.affected_regions:
        if virus.detectability < random.randint(0, len(virus.affected_regions)):
            virus.affected_regions.remove(region)

    return virus

def simulate_turn(world, virus):
    world = simulate_world_changes(world, virus)
    virus = simulate_virus_changes(world, virus)
    return [world, virus]


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
