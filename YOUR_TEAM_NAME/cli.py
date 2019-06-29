import click
from discord_bot import bot_client
from flask_api import flask_api_app
from flask_webportal import flask_webportal_app


@click.group()
def base_group():
    pass


@click.command()
def flask_webportal():
    """
    Runs the webportal mini-project (like the discord bot but on a website ui)
    """

    pass


@click.command()
def discord_bot():
    """
    Runs the discord bot mini-project, displaying all from the flask_api mini-project
    """

    pass


@click.command()
def flask_api():
    """
    The core API of this project, RESTFUL and built with flask & flask-restful
    """

    pass


base_group.add_command(flask_api)
base_group.add_command(discord_bot)
base_group.add_command(flask_webportal)
