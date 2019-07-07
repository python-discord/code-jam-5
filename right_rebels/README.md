# Right Rebels - World Temperature Map

Air surface temperature anomaly world map plotter - plot and visually see the temperature change ranging from 1850 - 2019.

## Requirements

You need Python 3.5 or later.

In Ubuntu, Mint and Debian you can install Python 3 like this:

    $ sudo apt-get install python3 python3-pip

For other Linux flavors, macOS and Windows, packages are available at

  http://www.python.org/getit/

## Usage

```bash
$ cd right_rebels
$ pip install -r requirements.txt
$ python main.py
```

Sometimes the `basemap` library will not come included with `matplotlib` so:

For windows users, install it from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#basemap) and be sure to select the version suited for you Python version:
- for example `cp35` means CPython 3.5, `win32` is for 32 bit Python while `amd64` is for 64 bit.

For linux users, install `libgeos` and install from [here](https://github.com/matplotlib/basemap/archive/master.zip)

## What is it?

We're using a user-friendly GUI to visually show the air surface temperature anomaly data from 1850 to 2019.

Our temperature map shows the increase/decrease of temperature at a global scale on a per-month basis (or a custom interval).
The color scheme, interval, start date and end date are all configurable.
Once you've plotted the data the images can be found in `data/plots` , however upon closing the program they are removed.
This way you can get the plotted data from the app without bloating your hard drive.
There are more options like playing and settings but more on that in [Example usage](##example-usage)


##### What is a temperature anomaly?

Global surface temperature anomalies are a description of how the overall average temperature of the surface of the Earth deviates from what is expected.

##### What can the temperature anomaly be used for?

A positive anomaly indicates that the observed temperature was warmer than the reference value, 
while a negative anomaly indicates that the observed temperature was cooler than the reference value.

##### Why use anomalies?

By showing whether temperatures are below or above normal, anomalies describe how climate is changing 
over larger areas more clearly than absolute temperatures. A certain absolute temperature may be normal 
in one region of the globe, it could be above average in another. 
Anomalies remove this uncertainty in what is "normal" and present data that shows how temperature is 
deviating locally.

##### Meaning?

The world has been showing a frightening abundance of positive anomalies in the past decade, which means the 
world is getting warmer.

## Example usage

Select start date from the left and end date from the right side of the screen.
Press `Plot`, the plotting will take some time depending on the step interval and selected year range.
You can stop the plotting at any time.

After that you can move the slider to move trough
generated images or just click `Play` to play automatically. You can also press buttons
`<--` and `-->` to move trough images in 1 year interval (also possible with hot-key ctrl+left/right arrow key).

There are configurable setting too when you click the `Preferences` button.

You can set the playback speed which will slow down or speed up the animation from `Play` button.

Step value means the interval of the plotter, 12 will result in only each year to be plotted
while 1 will plot each month (from the selected year range). To better see the changes in world map
temperature the value of 12 is recommended.

Color map is just how the data will be colored on the map. Most of them are similar,
blue represent negative temperature anomaly while the red represent positive.

## Authors

* **[martmists](https://github.com/martmists)** - *Team leader*
* **[Numerlor](https://github.com/Numerlor)** - *Frontend, refactoring*
* **[Braindead](https://github.com/albertopoljak)** - *Backend, refactoring*

## License

This project is licensed under the GPLv3 License - see the [LICENSE.md](LICENSE.md) file for details

Data temperature set file source [berkeleyearth.org](http://berkeleyearth.org/data/)