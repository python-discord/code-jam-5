import fnmatch
import os
import time

import matplotlib
import matplotlib.pyplot as plot
import numpy as np
from PyQt5 import QtCore
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset

# set matplotlib to not use tk while plotting
matplotlib.use('Agg')


class Plotter(QtCore.QThread):
    PLOTS_DIR = "plots/"
    NC_FILE_NAME = "Complete_TMAX_LatLong1.nc"
    image_increment_signal = QtCore.pyqtSignal()
    status_signal = QtCore.pyqtSignal(str)

    def __init__(self, start_date, end_date, parent_window=None):
        super(Plotter, self).__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.stop_plot = False
        if parent_window is not None:
            parent_window.stop_plot_signal.connect(self.stop)

    def run(self):
        self.main(self.start_date, self.end_date)

    def file_checks(self):
        # Temporal checks, change later
        if not os.path.isfile(self.NC_FILE_NAME):
            self.status_signal.emit(f"{self.NC_FILE_NAME} file not found, exiting")
            return False
        if os.path.isdir(f"/{self.PLOTS_DIR}"):
            self.status_signal.emit(f"{self.PLOTS_DIR} directory not found, exiting")
            return False
        return True

    def get_map_format(self):
        """
        https://matplotlib.org/basemap/api/basemap_api.html
        Returns:
            Basemap: Constructed world basemap
        """
        world_map = Basemap(projection="cyl", llcrnrlat=-90, urcrnrlat=90,
                            llcrnrlon=-180, urcrnrlon=180, resolution="c")
        self.draw_map_details(world_map)
        return world_map

    def draw_map_details(self, world_map):
        world_map.drawcoastlines(linewidth=0.6)
        world_map.drawcountries(linewidth=0.3)

    def get_variables_from_nc_file(self):
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
        with Dataset(self.NC_FILE_NAME, mode="r") as nc_file:
            self.status_signal.emit("Setting up worker")
            lon = nc_file.variables["longitude"][:]
            lat = nc_file.variables["latitude"][:]
            dates = nc_file.variables["time"][:]
            temps = nc_file.variables["temperature"][:]
            temps_unit = nc_file.variables["temperature"].units
            return lon, lat, dates, temps, temps_unit

    @staticmethod
    def find_nearest(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx

    @staticmethod
    def get_display_date(decimal_date):
        month = decimal_date % 1
        months = {"0.041": "January",
                  "0.125": "February",
                  "0.208": "March",
                  "0.291": "April",
                  "0.375": "May",
                  "0.458": "June",
                  "0.541": "July",
                  "0.625": "August",
                  "0.708": "September",
                  "0.791": "October",
                  "0.875": "November",
                  "0.958": "December"}
        return f"{months[str(month)[:5]]} {int(decimal_date)}"

    def clear_plots(self):
        filenames = os.listdir(self.PLOTS_DIR)
        for file in fnmatch.filter(filenames, "plot*.png"):
            os.remove(os.path.join(self.PLOTS_DIR, file))

    def stop(self):
        self.stop_plot = True

    def main(self, start, end):
        longitudes, latitudes, dates, temperatures, temperature_unit = self.get_variables_from_nc_file()
        world_map = self.get_map_format()
        # https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html
        color_map = plot.get_cmap("jet")

        # loop through months in range
        for count, date_index in enumerate(np.arange(start, end + 0.01, 0.08333333333)):
            if not self.stop_plot:
                self.status_signal.emit(f"Processing image {count + 1}/"
                                        f"{int((end - start) // 0.08333333333) + 1}")
                start_time = time.time()

                plot.figure(count)
                index = self.find_nearest(dates, date_index)
                date = dates[index]
                color_mesh = world_map.pcolormesh(longitudes, latitudes,
                                                  np.squeeze(temperatures[index]), cmap=color_map)
                color_bar = world_map.colorbar(color_mesh, location="bottom", pad="10%")
                color_bar.set_label(temperature_unit)
                self.draw_map_details(world_map)

                plot.title(f"Plot for {self.get_display_date(date)}")
                # This scales the plot to -4,6 making those 2 mark "extremes"
                # but if we have a change bigger than 4
                # we won't be able to see it other than
                # it being extra red (aka we won't know if it's +7 or +15)
                plot.clim(-4, 6)
                # bbox_inches="tight" remove whitespace around the image
                file_path = f"{self.PLOTS_DIR}plot{count}.png"
                plot.savefig(file_path, dpi=150, bbox_inches="tight", facecolor=(0.94, 0.94, 0.94))
                plot.close()
                print(f"Took {time.time() - start_time:.2f}s for image {count + 1}")
                self.image_increment_signal.emit()
        self.status_signal.emit("")


if __name__ == "__main__":
    p = Plotter(1994.125, 2000.7083333333333)
    p.start()
    while not p.isFinished():
        time.sleep(10)
