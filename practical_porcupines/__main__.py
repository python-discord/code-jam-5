import click
import asyncio
from practical_porcupines.utils import ConfigBase, ConfigApi, ConfigWebPortal, ConfigBot
from practical_porcupines.discord_bot import bot_client
from practical_porcupines.flask_api import flask_api_app
from practical_porcupines.flask_webportal import flask_webportal_app


@click.group()
def base_group():
    pass


@click.command()
def flask_webportal():
    """
    Runs the webportal mini-project (like the discord bot but on a website ui)
    """

    config_webportal = ConfigWebPortal()

    flask_webportal_app.run(
        host=config_webportal.API_DOMAIN,
        port=config_webportal.API_PORT,
        debug=ConfigBase().SHOULD_DEBUG,
    )


@click.command()
def discord_bot():
    """
    Runs the discord bot mini-project, displaying all from the flask_api mini-project
    """

    bot_client.run(ConfigBot().TOKEN)


@click.command()
def flask_api():
    """
    The core API of this project, RESTFUL and built with flask & flask-restful
    """

    config_api = ConfigApi()

    flask_api_app.run(
        host=config_api.API_DOMAIN,
        port=config_api.API_PORT,
        debug=ConfigBase().SHOULD_DEBUG,
    )


base_group.add_command(flask_api)
base_group.add_command(discord_bot)
base_group.add_command(flask_webportal)

if __name__ == "__main__":
    base_group()
