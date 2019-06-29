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
pipenv run export API_SECRET_KEY=abc && python -m practical_porcupines flask-api &
```

Run the discord bot in the background where `x` is the bot's token:

```bash
pipenv run export CLIENT_TOKEN=x && python -m practical_porcupines discord-bot &
```

Run the web-portal in the background:

```bash
pipenv run python -m practical_porcupines flask-webportal
```

- Please navigate to 0.0.0.0:8081 (or whatever else is set in `config.json`) to visit the web-portal mini-project.
- If you would like to run the Discord Bot as an extra, please add the bot tokens (please read the `Running the Discord Bot` section for more info).

## Development Notes

- Using `%Y:%m:%d:%T` formatting (UNIX). An example of this is: `2019:06:29:23:02:05` (at the time of writing). This would look like: `The 5th second of the 2nd minute of the 23rd hour of the 29th of June 2019` if said in speech.
- Autoformat using `black` and try to do a final sweep with the custom `flake8` rulings.
- Document everything in docstrings. `>` means overview of passing in, `<` means overview of returning and `-` are the argument specifics (use these like bullet points with them symbols).

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
pipenv run python -m practical_porcupines flask-api
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
python -m practical_porcupines discord-bot
```

### Running the WebPortal/WebUi

To run the webportal, you can simply type the following into your terminal:

```bash
pipenv run python -m practical_porcupines flask-webportal
```

This will automatically start the flask webportal in debug mode (as this project is not intended for production use)

## Dependancy breakdown

- `pipenv`: Package manager
- `flask`: Web Framework for flask_api and flask_webportal
- `discord.py`: Python bindings/api for discord_bot
- `flask-sqlalchemy`: Database abstraction for flask_api core maths (storing data on GMWL)
- `flask-restful`: Consistant RESTful API building for flask_api
- `aiohttp`: Asyncronous requests for discord_bot to prevent any "freezing" of it
- `requests`: Syncronous, easy to use api requests for flask_webportal to contact flask_api. ***May not be used in favour of in-website javascript***
- `flake8`: Linter specfic for `code-jam-5` (required for review)
- `black`: Developer-used autolinter for sake of standardized clarity

## File-by-file Overview

All titles below are files or folders in a child-parent setup. *Please view this markdown in text format if the folders get too deep*. `x/` = folder, `x` = file.

### `practical_porcupines/`

Contains all of the mini-projects and the `cli.py` file to execute them.

#### `practical_porcupines/cli.py`

`cli.py` uses `click` to manage the commands to give an enriched experiance using this project. If you would like to see some examples of these in action, please view `Running the API` all the way up to `Running the WebPortal/WebUi`.

#### `practical_porcupines/utils.py`

`utils.py` contains a large `Config` class with various configs for all the mini-projects. All of them have been documented in-file with their respective [docstrings](https://pypi.org/project/docstring/).

#### `practical_porcupines/__init__.py`

An empty file to notify python that this is a module.

#### `practical_porcupines/__main__.py`

Simply imports the `base_group` from `cli.py` and runs it if python is running it directly (not a module call externally)

#### `practical_porcupines/discord_bot/`

Stores all the files for the Discord Bot mini-project. This mini-project is more of an extra to this, a nice-to-have if you have time to test.

##### `practical_porcupines/discord_bot/__init__.py`

Imports the bot object for easy access to `discord_bot` directly

##### `practical_porcupines/discord_bot/bot.py`

The main file for all of the bot. It does not use `discord.py cogs` but does use the reccomended `commands` method.

#### `practical_porcupines/flask_api/`

The api mini-project, storing the core of this project. It is a simple REST api built around a database, getting 2 times and returning the water level difference between the 2 over the api.

##### `practical_porcupines/flask_api/__init__.py`

Imports the flask objects for easy use importing

##### `practical_porcupines/flask_api/app.py`

Stores the flask app and general views/flask-restful responses. Also holds the `db` objecrt for `practical_porcupines/flask_api/models.py`

##### `practical_porcupines/flask_api/models.py`

Stores the `flask-sqlalchemy` tables (currently only 1) that contain the global water level differences & other items

##### `practical_porcupines/flask_api/difference_calc.py`

Stores the overlying logic behind the api, the calculator! It is one large object/function (not decided at the time of writing) that contains the mathmatical operations, hooking onto the `flask-sqlalchemy` made database

#### `practical_porcupines/flask_webportal/`

Contains the web-portal mini-project, the easiest to setup way to view the data from the flask_api mini-project.

##### `practical_porcupines/flask_webportal/__init__.py`

Imports the flask objects for easy use importing

##### `practical_porcupines/flask_webportal/app.py`

Stores the main logic for the webportal mini-project. Views and such

##### `practical_porcupines/flask_webportal/api.py`

Uses the `requests` library to hook onto the flask_api mini-project depending on the unified hostname/ports set in `config.json`

##### `practical_porcupines/flask_webportal/templates/x`

Stores all of the html templates

##### `practical_porcupines/flask_webportal/static/x`

Stores all static files (images, javascript, css) for the html templates shown above.

### `YOUR_TEAM_NAME/`

Stores nothing really due to a mistake made when making the `code-jam-5` project.

### `.flake8`

Some basic rights and wrongs for the `flake8` linter to follow

### `.gitignore`

Python-based gitignore with a couple of extra options added in

### `azure-pipelines.yml`

CI for project (can also be a webhook)

### `config.json`

Stores unified infomation on all projects, edit this for a custom configuration but *please do not use the same ports unless you want an unstable time*

### `LICENSE`

The MIT license file

### `Pipfile`

Stores the human-readable pipenv configurations to use and lock.

### `Pipfile.lock`

The computer-readable (I guess) json file for locking pipenv

### `README.md`

The basic `README.md` for the project, describing what to do and what **not** to do. Best not to change this.
