# Documentation: CorruptClimate

## Description

CorruptClimate is a global warming simulator.

While not being truly realistic, it shows how dangerous climate change is.

## Requirements

Requires python 3.6.7+ (and pip)

## Setup

Firstly, change your directory to `corrupt_cats`

```
$ cd <code_jam_root_level>/corrupt_cats
```

Secondly, install all required dependencies:

```
$ pip install -r requirements.txt
```

And, lastly, run the app:

```
python -m start
```

## Notes

* Game takes ~10-15 seconds to load, because of "random generation" (shuffling) of country islands.

> The background ambient might be too loud, just lower your device's volume in that case.

(I highly recommend to playtest the volume of `/corrupt_cats/game/sounds/bg_ambient.wav` before running the app)

## How to play

There are no controls, really. As it was stated, CorruptClimate is a simulator.

Just run it and have fun watching humanity disappear -.-)/

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

## In case any problems appear...

If you are recieving an error, contact `NeKitGuyPro[DSS]#1110` on Discord or `NeKitDSS` on GitHub

## Credits

### Music

`bg_ambient.wav` from [freesound.org](https://freesound.org/)

### Event

Big thanks to all organisators from [pythondiscord.com](https://pythondiscord.com/)