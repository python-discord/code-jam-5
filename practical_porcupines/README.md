# practical-porcupines Documentation

## Dataset Acknowledgement

*GSFC. 2017. Global Mean Sea Level Trend from Integrated Multi-Mission Ocean Altimeters TOPEX/Poseidon, Jason-1, OSTM/Jason-2 Version 4.2 Ver. 4.2 PO.DAAC, CA, USA. Dataset accessed [2019-06-30] at [http://dx.doi.org/10.5067/GMSLM-TJ42](http://dx.doi.org/10.5067/GMSLM-TJ42).*

## Human-friendly Overview

Hello welcome to the Practical Pourcupine project, made for the 5th [Python Discord](https://pythondiscord.com/) code jam! The theme of this code-jam was about climate change, as you can see from the top-level README.md, found [here](https://github.com/scOwez/code-jam-5/blob/master/README.md).

We have 3 "mini-projects" (3 different projects that *could* be in seperate repos but due to the code jam, are all housed under one roof). We have the `flask_api`; this is the api part of our web-based project. This API gets a request and uses interpolation and when needed, machine learning to either predict or state the change in the global water level.

The two other "mini-projects" are the ones sending and handling the returns, one is called `discord_bot` & it is a Discord Bot (duh)! The other is a web-portal (`flask_webportal`) made using flask and a small bit of bootstrap for the css, allowing users to send requests over a website if it where in production. This is similar to the discord_bot but showcases another, more flexible usecase for this api.

### Technical side

Alright, onto the more technical side:

We have an api (named `flask_api`), a webportal (named `flask_webportal`) and a discord bot (named `discord_bot`). The api recives 2 dates formatted using (mainly) `%Y-%m-%d %T` formatting (UNIX). An example of this is: `2019-07-02 14:33:59` (at the time of writing). This would look like: `The 59th second of the 33rd minute of the 14th hour of the 2nd of July, 2019` if said in speech. Please note that the API can accept other dates, this formatting is just the preferred way :)

**Once it has 2 dates, the `core` uses either historical data from a function we calculated using interpolation or predicts the future changes using *Machine Learning*.**

Once it has those, the `core` returns those (it's one large frontend function) and the api (remember `flask_api`) returns the difference in water level between them two dates in millimeters, as either a prediction or as an accurate difference from histroical data.

Say I put in somewhere in 1950 and somewhere in 2019, it would give me somewhere in the region of 20000mm but it'd be as accurate as it could, interpolating the points in-between the years, couples with machine learning to predict before the dataset that we selected to give a precise value.

Once it sends out this return, we have a simple discord bot and webportal (webportal = a small website connected to the api, `flask_api`) that you can see the results on. For the discord bot (`discord_bot` in files), you could put 1950 and 2000 in like so: `?gmwl 1950 2000` and it would return an answer.

Below is the outline of what the dependancies do:

- `pipenv`: Package manager
- `flask`: Web Framework for flask_api and flask_webportal
- `discord.py`: Python bindings/api for discord_bot
- `flask-sqlalchemy`: Database abstraction for flask_api core maths (storing data on GMWL)
- `flask-restful`: Consistant RESTful API building for flask_api
- `aiohttp`: Asyncronous requests for discord_bot to prevent any "freezing" of it
- `requests`: Syncronous, easy to use api requests for flask_webportal to contact flask_api.
- `flake8`: Linter specfic for `code-jam-5` (required for review)
- `black`: Developer-used autolinter for sake of standardized clarity

### Mini-project Notice

***Please note that `discord_bot` or `flask_webportal` communicate **only** though the api, not just calling a shared function. The only shared infomation between these 3 projects is a config as not to collide with each others hosting and 2 exeptions that are 2x `class ExceptionName: pass`. Therefore in 10 minutes, you could easily seperate these 3 mini-projects into seperate repositories.***

## Quickstart (Please read this section to start up the application)

1. Please edit `CLIENT_TOKEN` from the `.env` file inside of the base folder, next to `Pipfile` to the bot's token
2. Install pipenv with `pip install pipenv` (NOTE: May be `pip3` on Linux)
3. Enter pipenv's shell with `pipenv shell`
4. When in the pipenv shell, run `python -m practical_porcupines flask-api` to start the api
5. To start the webportal, **open a new terminal** and repeat step 3 & 4 with `flask-webportal` instead of `flask-api`
6. To start the discord bot, **open a new terminal** and repeat step 3 & 4 with `discord-bot` instead of `flask-api`. Make sure you have step 1 set properly for this one

## Development Notes

### General Notes

- NOTE: If you are on Windows, please use `set` instead of `export`
- When connecting to the api (`flask_api`), it is favourable to use the `%Y-%m-%d %T` time formatting (UNIX annotations with `%`). An example of this is: `2019-06-29 23:02:05` (at the time of writing). This would look like: `The 5th second of the 2nd minute of the 23rd hour of the 29th of June 2019` if said in speech. The api can use other times but it is best to standardize with this method. Despite this, here are some of the other methods you can use: `%Y:%m:%d:%H:%M:%S`, `%H:%M:%S %d.%m.%Y`, `%m/%d/%Y %H:%M:%S`, `%d.%m.%Y`, `%m/%d/%Y`, `%Y-%m-%d %H:%M:%S`
- Autoformat using `black` and try to do a final sweep with the custom `flake8` rulings.
- Document everything in docstrings. `>` means overview of passing in, `<` means overview of returning, `x` is the execption handling and `-` are the argument specifics (use these like bullet points with them symbols).

### API Error codes

- `400`: API was given a bad date format (`DateFormatError()`)
- `1001`: API returning wrong values (usually happens in debugging when hooked upto a dummy api)
- `1002`: Date is out of range of dataset. *NOTE: This http code is decrept but should stay for the sake of legacy*.

### API schema

#### API Response

##### API Response Schema

```none
{
    [STRING: META]: {
        [KEY: STATUS CODE]: [INT: STATUS],
        [ARRAY: DATES]: {
            [STRING: 1ST DATE ARG],
            [STRING: 2ND DATE ARG]
        }
        [KEY: TIME SENT]: [STRING: TIME SENT]
    }
    [KEY: BODY]: {
        [KEY: IS_PREDICTION]: [BOOL: YAY OR NAY]
        [KEY: WATER_LEVEL]: [FLOAT: DIFFERENCE]
    }
}
```

##### API Response Example

```json
{
    "meta": {
        "status_code": 200,
        "dates": {
            "date_1": "1995-02-10 13:14:00",
            "date_2": "2019-06-29 23:27:45"
        },
        "time_sent": "2019-06-29 11:52:30"
    },
    "body": {
        "is_prediction": false,
        "wl_difference": 20.9
    }
}
```

#### API Ingress

##### API Ingress Schema

```none
{
    [STRING: DATE_1]: [STRING: DATE],
    [STRING: DATE_2]: [STRING: DATE]
}
```

#### API Ingress Example

```json
{
    "date_1": "1995-02-10 13:14:00",
    "date_2": "2019-06-29 23:27:45"
}
```

## Old `File-by-file Overview`

**NOTE: This is not used anymore as it was a pain to update.**

\- *scOwez, 2019/07/02*

```md
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

##### `practical_porcupines/discord_bot/api.py`

Contains the basic aiohttp linking to the database. **Note: could be merged with `practical_porcupines/discord_bot/utils.py`**

##### `practical_porcupines/discord_bot/utils.py`

Contains the discord_bot utils with items like decoding the api response and handeling general errors. Also includes a nifty embed generator

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

Uses the `requests` library to hook onto the flask_api mini-project depending on the unified hostname/ports set in `config.toml`

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

### `config.toml`

Stores unified infomation on all projects, edit this for a custom configuration but *please do not use the same ports unless you want an unstable time*

### `LICENSE`

The MIT license file

### `Pipfile`

Stores the human-readable pipenv configurations to use and lock.

### `Pipfile.lock`

The computer-readable (I guess) json file for locking pipenv

### `README.md`

The basic `README.md` for the project, describing what to do and what **not** to do. Best not to change this.
```
