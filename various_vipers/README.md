# Documentation for your team's project

To do: Add documentation of your project here.

## Requirements

Requires python 3.6+ (with pip)

## Setup

To prepare for development, run commands (from this directory):

```
pip install pipenv
pipenv install --dev
pipenv run precommit
```

## Troubleshooting

1) `ERROR: Could not find a version that matches black`

Your Pipenv lock file might be corrupt, try running command:

`pipenv lock --pre --clear`
