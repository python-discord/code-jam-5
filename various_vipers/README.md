﻿﻿<h2 align="center">Various Vipers | saving the earth</h2>
<p align="center">
  (Python Discord code jam 5 submission)<br>
  <img src="https://i.imgur.com/S14ouvw.png" width="256">
</p>

The climate change is a real danger to our planet, and if we don't help reduce the pollution, it will be destroyed. Your task is to save the earth!


This game is about you - completing tasks that will decrease the pollution. Try to do as many tasks as you can, while it is still not too late.


See `/docs` for more documentation.

## Requirements

Requires python 3.7+ (with pip)

## Setup (for development)

To prepare for development, run commands (from this directory):

```
$ pip install pipenv
$ pipenv install --dev
$ pipenv run precommit
```

## Setup

To run the game, you will need to install all the dependencies (in Pipfile).

Run commands (from this directory):

```
$ pip install pipenv
$ pipenv install
```

## Start Game

To start the game, simply run:

`$ pipenv run start`

## Notes

* The game is not optimized and will eat ~550 MB of RAM to hold cached images of sun and tiles.

> 361 images of sun (for each angle of rotation)

> 20 images for each tile on map (scaled by 2.5% each time)

* The sun looks "laggy" when spinning slowly, because it only rotates at a full 1 degree angle each time (instead of a smoothed floating point value angle).

## Troubleshooting

1) `ERROR: Could not find a version that matches black`

Your Pipenv lock file might be corrupt, try running command:


$ pipenv lock --pre --clear
<h2 align="center">Various Vipers | saving the earth</h2>
<p align="center">
  (Python Discord code jam 5 submission)<br>
  <img src="https://i.imgur.com/S14ouvw.png" width="256">
</p>

The climate change is a real danger to our planet, and if we don't help reduce the pollution, it will be destroyed. Your task is to save the earth!


This game is about you - completing tasks that will decrease the pollution. Try to do as many tasks as you can, while it is still not too late.


See `/docs` for more documentation.

## Requirements

Requires python 3.7+ (with pip)

## Setup (for development)

To prepare for development, run commands (from this directory):

```
$ pip install pipenv
$ pipenv install --dev
$ pipenv run precommit
```

## Setup

To run the game, you will need to install all the dependencies (in Pipfile).

Run commands (from this directory):

```
$ pip install pipenv
$ pipenv install
```

## Start Game

To start the game, simply run:

`$ pipenv run start`

## Notes

* The game is not optimized and will eat ~550 MB of RAM to hold cached images of sun and tiles.

> 361 images of sun (for each angle of rotation)

> 20 images for each tile on map (scaled by 2.5% each time)

* The sun looks "laggy" when spinning slowly, because it only rotates at a full 1 degree angle each time (instead of a smoothed floating point value angle).

## Troubleshooting

1) `ERROR: Could not find a version that matches black`

Your Pipenv lock file might be corrupt, try running command:


$ pipenv lock --pre --clear
## How to play

The global temperature is drastically increasing. Your mission is to save the Earth through completing tasks - saving the forests and mountains ice, building solar panels and decreasing the pollution.

#### Tasks
Every task is represented with a tile colored in the red spectrum.
There are indicators on the sides of the screen which guide you where are the tasks.
With completing each task you decrease the global temperature.
There are three different types of tasks.

1) **Cursor maze** - to begin you hover over starting position displayed as a square with image on it. After that the maze reveals itself and you should follow the path to the end point without touching the walls.

2) **Rock, paper, scissors** - some things are a question of luck. You have 1/3 chance of winning this task.

3) **Tic tac toe** - you are playing against the computer. If you make a tie it still counts as a win.

#### Controls
`A D or left arrow key and right arrow key` - to move on the surface of the Earth

`ESC` - to pause the game

`Mouse click` - to start a task









