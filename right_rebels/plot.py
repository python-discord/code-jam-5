import fnmatch
import os
import time

import matplotlib
import matplotlib.pyplot as plot
import numpy as np
from PyQt5 import QtCore
from mpl_toolkits.basemap import Basemap

import helpers

# Set matplotlib to not use tk while plotting
matplotlib.use('Agg')


class Plotter(QtCore.QThread):
    PLOTS_DIR = "plots/"
    NC_FILE_NAME = "Complete_TMAX_LatLong1.nc"
    LONGITUDES, LATITUDES, DATES, TEMPERATURES, TEMPERATURE_UNIT = helpers.get_variables_from_nc_file(NC_FILE_NAME)
    image_increment_signal = QtCore.pyqtSignal()
    status_signal = QtCore.pyqtSignal(str)

    def __init__(self, start_date, end_date, parent_window=None):
        super(Plotter, self).__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.stop_plot = False
        # https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html
        self.color_map = plot.get_cmap("seismic")
        self.world_map = Plotter.get_map_format()
        if parent_window is not None:
            parent_window.stop_plot_signal.connect(self.stop)

    def run(self):
        self.start_plotting(self.start_date, self.end_date)

    def stop(self):
        self.stop_plot = True

    def file_checks(self):
        if not os.path.isfile(self.NC_FILE_NAME):
            self.status_signal.emit(f"{self.NC_FILE_NAME} file not found, exiting")
            return False
        if os.path.isdir(f"/{self.PLOTS_DIR}"):
            self.status_signal.emit(f"{self.PLOTS_DIR} directory not found, exiting")
            return False
        return True

    @staticmethod
    def get_map_format():
        """
        Source:
            https://matplotlib.org/basemap/api/basemap_api.html
        Returns:
            Basemap: Constructed world basemap
        """
        world_map = Basemap(projection="cyl", llcrnrlat=-90, urcrnrlat=90,
                            llcrnrlon=-180, urcrnrlon=180, resolution="c")
        Plotter.draw_map_details(world_map)
        return world_map

    @staticmethod
    def draw_map_details(world_map):
        world_map.drawcoastlines(linewidth=0.6)
        world_map.drawcountries(linewidth=0.3)

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

    @staticmethod
    def clear_plots():
        file_names = os.listdir(Plotter.PLOTS_DIR)
        for file in fnmatch.filter(file_names, "plot*.png"):
            os.remove(os.path.join(Plotter.PLOTS_DIR, file))

    def start_plotting(self, start_date_decimal, end_date_decimal, step: int = 1):
        if not 0 < step <= 12:
            step = 1
        start_date_index = helpers.find_nearest_index(Plotter.DATES, start_date_decimal)
        end_date_index = helpers.find_nearest_index(Plotter.DATES, end_date_decimal)
        # end_date_index + 1 to make end_date inclusive
        for count, date_index in enumerate(range(start_date_index, end_date_index + 1, step)):
            if not self.stop_plot:
                self.status_signal.emit(f"Processing image {count + 1}/"
                                        f"{end_date_index - start_date_index}")
                start_time = time.time()
                self.create_plot(count, date_index)
                print(f"Took {time.time() - start_time:.2f}s for image {count + 1}")
                self.image_increment_signal.emit()
        self.status_signal.emit("")

    def create_plot(self, count, date_index):
        plot.figure(count)
        color_mesh = self.world_map.pcolormesh(Plotter.LONGITUDES, Plotter.LATITUDES,
                                               np.squeeze(Plotter.TEMPERATURES[date_index]),
                                               cmap=self.color_map)
        color_bar = self.world_map.colorbar(color_mesh, location="bottom", pad="10%")
        color_bar.set_label(Plotter.TEMPERATURE_UNIT)
        Plotter.draw_map_details(self.world_map)
        date = Plotter.get_display_date(Plotter.DATES[date_index])
        plot.title(f"Plot for {date}")
        # This scales the plot to -10,10 making those 2 mark "extremes"
        # but if we have a change bigger than 10
        # we won't be able to see it other than
        # it being extra red (aka we won't know if it's +11 or +15)
        plot.clim(-10, 10)
        file_path = f"{Plotter.PLOTS_DIR}plot{count}.png"
        # bbox_inches="tight" remove whitespace around the image
        # facecolor=(0.94, 0.94, 0.94) , background color of image
        plot.savefig(file_path, dpi=145, bbox_inches="tight", facecolor=(0.94, 0.94, 0.94))
        plot.close()


if __name__ == "__main__":
    p = Plotter(1994.125, 2000.7083333333333)
    p.start()
    while not p.isFinished():
        time.sleep(10)
