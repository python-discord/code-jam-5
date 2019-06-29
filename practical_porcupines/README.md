# practical-porcupines Documentation

## Quickstart (Please read this section to start up the application)

Install pipenv:

```bash
pip3 install pipenv
```

Install dependancies:

```bash
pipenv install
```

Make a totally secure secret key and run the api in the background:

```bash
pipenv run export API_SECRET_KEY=abc && practical_porcupines/ flask-api &
```

Run the discord bot in the background where `x` is the bot's token:

```bash
pipenv run export CLIENT_TOKEN=x && practical_porcupines/ discord-bot &
```

Run the web-portal in the background:

```bash
pipenv run practical_porcupines/ flask-webportal
```

- Please navigate to 0.0.0.0:8081 (or whatever else is set in `config.json`) to visit the web-portal mini-project.
- If you would like to run the Discord Bot as an extra, please add the bot tokens (please read the `Running the Discord Bot` section for more info).

## Installation

### Installing dependancies

This repo uses `pipenv` to install & easily manage dependancies. To install `pipenv`, please enter the following into a terminal:

```bash
pip3 install pipenv
```

*Please note that `pip3` can be replaced by `pip` depending on the operating system.*

After you have installed `pipenv`, you can cd into the base folder of this repository (the one where `.git/` is stored) and enter this command to install all dependancies:

```bash
pipenv install
```

Once you have all of the required dependancies installed, it is time to boot up a part of this repo. We use `click` to seperate our different mini-projects (An API, discord bot and web-portal/ui). Please select from the following items below to run that mini-project.

## Running individually

### Running the API

First, please enter the pipenv sandboxed shell with the following command

```bash
pipenv shell
```

When you are in this sandboxed enviroment, please set an enviroment variable for `API_SECRET_KEY`. *Please note that this will be different depending on the operating system used*. An example of this is below (Linux):

```bash
export API_SECRET_KEY=sk
```

Insert the secret key where `sk` is currently present. After you have completed this step, you may run the discord bot with the following command

To run the API, you can simply type the following into your terminal:

```bash
pipenv run python practical_porcupines/ flask-api
```

This will automatically start the flask API in debug mode (as this project is not intended for production use)

### Running the Discord Bot

You will first need to get the bot's token, to do this please follow [this](https://www.writebots.com/discord-bot-token/) tutorial. Once you have done that, please enter the pipenv sandboxed shell with the following command

```bash
pipenv shell
```

When you are in this sandboxed enviroment, please set an enviroment variable for `CLIENT_TOKEN`. *Please note that this will be different depending on the operating system used*. An example of this is below (Linux):

```bash
export CLIENT_TOKEN=ct
```

Insert the bot's token where `ct` is currently present. After you have completed this step, you may run the discord bot with the following command

```bash
python practical_porcupines/ discord-bot
```

### Running the WebPortal/WebUi

To run the webportal, you can simply type the following into your terminal:

```bash
pipenv run python practical_porcupines/ flask-webportal
```

This will automatically start the flask webportal in debug mode (as this project is not intended for production use)

## Documentation

All titles below are files or folders in a child-parent setup. *Please view this markdown in text format if the folders get too deep*. `x/` = folder, `x` = file.

### `practical_porcupines/`

Contains all of the mini-projects and the `cli.py` file to execute them.

#### `cli.py`

`cli.py` uses `click` to manage the commands to give an enriched experiance using this project. If you would like to see some examples of these in action, please view `Running the API` all the way up to `Running the WebPortal/WebUi`.

#### `utils.py`

`utils.py` contains a large `Config` class with various configs for all the mini-projects. All of them have been documented in-file with their respective [docstrings](https://pypi.org/project/docstring/).

#### `__init__.py`

An empty file to notify python that this is a module.

#### `__main__.py`

Simply imports the `base_group` from `cli.py` and runs it if python is running it directly (not a module call externally)
