from netCDF4 import Dataset
import numpy as np


def get_variables_from_nc_file(nc_file_name):
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
    with Dataset(nc_file_name, mode="r") as nc_file:
        lon = nc_file.variables["longitude"][:]
        lat = nc_file.variables["latitude"][:]
        dates = nc_file.variables["time"][:]
        temps = nc_file.variables["temperature"][:]
        temps_unit = nc_file.variables["temperature"].units
        return lon, lat, dates, temps, temps_unit


def find_nearest_index(array, value):
    """
        Finds the index of array element which is the most similar to the param value.
        :return: int representing the index in the passed array.
    """
    array = np.asarray(array)
    index = (np.abs(array - value)).argmin()
    return index

