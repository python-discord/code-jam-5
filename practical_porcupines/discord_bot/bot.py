import discord
from discord.ext import commands
from practical_porcupines.utils import (  # fmt: off
    ApiReturnBad,
    ConfigBot,
    PredictionNotImplamentedError,
    DateFormatError,
    string_to_datetime,
)
from practical_porcupines.discord_bot.utils import embed_generator
from practical_porcupines.discord_bot.api import get_difference


config_bot = ConfigBot()

bot_client = commands.Bot(command_prefix=config_bot.PREFIX)


@bot_client.event
async def on_ready():
    """
    Runs when client boots
    """

    print(f"{bot_client.user.name} is online w/ id: '{bot_client.user.id}'!")


@bot_client.command()
async def gmwl(ctx, date_1, date_2):
    """
    Global Mean water level command

    > Inputs 2 dates
    - date_1: Beginning date
    - date_2: Ending date
    < Shows user gmwl difference
    """

    try:
        verified_date_1 = string_to_datetime(date_1)
        verified_date_2 = string_to_datetime(date_2)
    except PredictionNotImplamentedError:
        await ctx.send(
            embed=embed_generator(
                "Error!",
                f"The given dates ('{date_1}' and '{date_2}') "
                "are not in the dataset range (1993-01 - 2019-02) "
                "and predictions have not been implamented yet!",
                0xA31523,
                discord,
            )
        )

        return
    except DateFormatError:
        await ctx.send(
            embed=embed_generator(
                "Incorrect date formatting!",
                "You have inputted an incorrect syntax for the date!",
                0xA31523,
                discord,
            )
        )

        return
    except Exception as e:
        await ctx.send(
            embed=embed_generator(
                "Misc date!",
                "Got a misc error we can't handle for the `string_to_datetime` "
                "function! The exception follows below, please send it "
                "to the developers:"
                f"\n\n*{e}*",
                0xA31523,
                discord,
            )
        )

        return

    # IF invalid date
    if not (verified_date_1 or verified_date_2):
        await ctx.send(
            embed=embed_generator(
                "Invalid date!",
                "One of the dates you sent was invalid, please try again!",
                0xA31523,
                discord,
            )
        )
        return

    try:
        result = await get_difference(verified_date_1, verified_date_2)
    except ApiReturnBad:
        embed = embed_generator(
            "Error!",
            "The API is not returning the expected values. "
            "This usually occures in testing w/ dummy endpoint",
            0xA31523,
            discord,
        )
    else:
        embed = embed_generator(
            "Result",
            f"Operation completed sucsessfully, result is {result}mm",
            0x3BA315,
            discord,
        )

    await ctx.send(embed=embed)


@bot_client.command()
async def about(ctx):
    """
    < Shows general about for the project
    """

    about_text = (
        "Practical Porcupine is a project hacked together for the 5th Python "
        "code jam, with the theme of **Global Warming**. This web-portal "
        "connects to an api (that you are most likely running on your computer "
        "right now (If you are, it may be here!: <http://0.0.0.0:8080>)! It gets "
        "2 dates, as seen on the home page (usually <http://0.0.0.0:8081>) and "
        "calculates the difference between the GMWL (Global Mean Water Level) in mm."
        "\n\n"
        "To save database space and *show off*, we use data year by year, "
        "meaning that we pick a mean of each year from our data sources and "
        "store them. Once we have the mean of each year, we can interpolate "
        "that & get a prediction of what it would have been like at that "
        "specific second!"
    )

    await ctx.send(  # fmt: off
        embed=embed_generator("About", about_text, 0x9E15A3, discord)
    )
