# Various Vipers | saving the earth

(Python Discord code jam 5 submission)


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

## Troubleshooting

1) `ERROR: Could not find a version that matches black`

Your Pipenv lock file might be corrupt, try running command:

```
$ pipenv lock --pre --clear
```
