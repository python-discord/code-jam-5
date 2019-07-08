# Documentation: CorruptClimate

## Description

CorruptClimate is a global warming simulator.

While not being truly realistic, it shows how dangerous climate change is.

## Requirements

Requires python 3.6.7+ (and pip)

## Setup

Firstly, change your directory to `corrupt_cats`:

```
$ cd <code_jam_root>/corrupt_cats
```

Secondly, install all required dependencies:

```
$ pip install -r requirements.txt
```

And, lastly, run the app:

```
$ python -m start
```

## Notes

* Game takes ~10-15 seconds to load, because of "random generation" (shuffling) of country islands.

* The background ambient might be too loud, just lower your device's volume in that case.

(I highly recommend to playtest the volume of `/corrupt_cats/game/sounds/bg_ambient.wav` before running the app)

## How to play

There are no controls, really. As it was stated, CorruptClimate is a simulator.

Just run it and have fun watching humanity disappear -.-)/

## Simulator explanation

Each country has it's own start temperature.

At start, country.cfc is equal to zero, and country.industry_level is random number between 1 and 2

Country's parameters start changing according to the following:

```python
country.cfc = country.cfc + country.industry_level * (country.temperature/10 + sqrt(abs(country.population))/100)
# country.cfc is rounded to integer

country.temperature = country.temperature + sqrt(country.cfc)/150
# country.temperature is rounded to first two digits after floating point

k = abs(a*b/10)
# k is rounded to integer

country.population = country.population + x
# where x is (-50k) if country.temperature-country.start_temperature > 40, and (k) otherwise.
```

So, according to formulas, you can see, that population is growing until difference between temperature and start_temperature is less than 40,

And then the population starts decreasing quite fast

If you really think there is a bug, see `In case any problems...` section below.

## Quick file index

`main.py` - contains main code of the project

`config.json`, `setup.json` - config files, it is not recommended to touch them

`ui/classes.py` - contains code of NSprite

`sounds`, `sprites`, `pixel_font.ttf` - assets for the project


`core/accidents.py` - contains code of different Accidents

`core/constants.py` - contains constants used in the project

`core/country.py` - includes code or Country class

`core/temperature.py` - sets up structure of Temperature class

`core/utils/functions.py` - has all functions that are needed (or not needed) in the project

`core/utils/lists.py` - has lists used in Country name generation

`core/utils/name_gen.py` - generates random names for Country objects

## In case any bugs/problems appear...

If you are recieving an error, or you think you have found a bug, please contact `NeKitGuyPro[DSS]#1110` on Discord or `NeKitDSS` on GitHub

## Credits

### Music

`bg_ambient.wav` from [freesound.org](https://freesound.org/)

### Event

Big thanks to all organisators from [pythondiscord.com](https://pythondiscord.com/) <3
