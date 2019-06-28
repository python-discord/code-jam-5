# practical-porcupines Documentation

## Installing dependancies

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

### Running the API

To run the API, you can simply type the following into your terminal:

```bash
pipenv run python practical_porcupines/ flask_API
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
python practical_porcupines/ discord_bot
```

### Running the WebPortal/WebUi

To run the webportal, you can simply type the following into your terminal:

```bash
pipenv run python practical_porcupines/ flask_webportal
```

This will automatically start the flask webportal in debug mode (as this project is not intended for production use)
