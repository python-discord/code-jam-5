import h5py
import numpy as np


def get_variables_from_nc_file(nc_file_name):
    """
        Nc file source: http://berkeleyearth.org/data/
        netCDF-4+ files are already using data model implementing HDF5
        as the storage layer. This means we don't have to load nc file variables
        in memory but can use h5py library to load them directly from file
        while still working with them as if they were in memory.

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
    # Don't close the connection since we need it to load data from disk
    h5py_file = h5py.File(nc_file_name, "r")
    lon = h5py_file["longitude"]
    lat = h5py_file["latitude"]
    dates = h5py_file["time"]
    temps = h5py_file["temperature"]
    temps_unit = "degree C"
    return lon, lat, dates, temps, temps_unit


def find_nearest_index(array, value):
    """
        Finds the index of array element which is the most similar to the param value.
        :return: int representing the index in the passed array.
    """
    array = np.asarray(array)
    index = (np.abs(array - value)).argmin()
    return index
