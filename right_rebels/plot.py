from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plot
from netCDF4 import Dataset
import numpy as np
import time
import os

PLOTS_DIR = "plots/"
NC_FILE_NAME = "Complete_TMAX_LatLong1.nc"


def file_checks():
    # Temporal checks, change later
    if not os.path.isfile(NC_FILE_NAME):
        print(f"{NC_FILE_NAME} file not found, exiting")
        return False
    if os.path.isdir(f"/{PLOTS_DIR}"):
        print(f"{PLOTS_DIR} directory not found, exiting")
        return False
    return True


def get_map_format():
    """
    https://matplotlib.org/basemap/api/basemap_api.html
    Returns:
        Basemap: Constructed world basemap
    """
    world_map = Basemap(projection="cyl", llcrnrlat=-90, urcrnrlat=90,
                        llcrnrlon=-180, urcrnrlon=180, resolution="c")
    draw_map_details(world_map)
    return world_map


def draw_map_details(world_map):
    world_map.drawcoastlines(linewidth=0.6)
    world_map.drawcountries(linewidth=0.3)


def get_variables_from_nc_file():
    """
        Nc file source: http://berkeleyearth.org/data/
        These represent variables from the .nc file:
        longitude
            Shape: 360
            Precision: 0.5
            Output: [-179.5 -178.5 -177.5 ... 0 .... 177.5  178.5  179.5]
        latitude
            Shape: 180
            Precision 0.5
            Output: [-89.5 -88.5 -87.5 .. 0 ... 87.5  88.5  89.5]
        time
            Shape: 2033
            Output: [1850.04166667, 1850.125 ... 2019.29166667, 2019.375]
            Output type: Data format is decimal with year and fraction of
            year reported, with each value corresponding to the midpoint
            of the respective month.
        land_mask
            Shape:(180, 360),
            Output: [[1. 1. 1. ... 1. 1. 1.] ... [0. 0. 0. ... 0. 0. 0.]]
            For each grid cell, the fraction of the cell which corresponds
            to land (as opposed to ocean or other large water bodies).
        temperature
            Shape:(2033, 180, 360)
            Format: [[time][latitude][longitude]]
            Units: Degrees C
    """
    with Dataset(NC_FILE_NAME, mode="r") as nc_file:
        lon = nc_file.variables["longitude"][:]
        lat = nc_file.variables["latitude"][:]
        dates = nc_file.variables["time"][:]
        temps = nc_file.variables["temperature"][:]
        temps_unit = nc_file.variables["temperature"].units
        return lon, lat, dates, temps, temps_unit


def main(start, end):
    longitudes, latitudes, dates, temperatures, temperature_unit = get_variables_from_nc_file()
    world_map = get_map_format()
    color_map = plot.get_cmap("jet")  # https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html

    for count, date_index in enumerate(range(start, end)):
        print(f"Processing image {count + 1}/{end-start}")
        start_time = time.time()

        plot.figure(count)
        date = dates[date_index]
        color_mesh = world_map.pcolormesh(longitudes, latitudes, np.squeeze(temperatures[date_index]), cmap=color_map)
        color_bar = world_map.colorbar(color_mesh, location="bottom", pad="10%")
        color_bar.set_label(temperature_unit)
        draw_map_details(world_map)
        plot.title(f"Plot for {date}")
        # This scales the plot to -4,4 making those 2 mark "extremes", but if we have a change bigger than 4
        # we won't be able to see it other than it being extra red (aka we won't know if it's +5 or +15)
        plot.clim(-4, 4)
        # bbox_inches="tight" remove whitespace around the image
        file_path = f"{PLOTS_DIR}{count}_{date}.png"
        plot.savefig(file_path, dpi=150, bbox_inches="tight")

        print(f"Took {time.time() - start_time:.2f}s for image {count + 1}")

    print("Done")


if __name__ == "__main__":
    if file_checks():
        main(2000, 2010)
