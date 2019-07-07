import discord
from discord.ext import commands
from practical_porcupines.utils import (  # fmt: off
    ApiReturnBad,
    ConfigBot,
    PredictionNotImplamentedError,
    DateFormatError,
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
        result, is_prediction = await get_difference(date_1, date_2)
    except ApiReturnBad:
        embed = embed_generator(
            "Error!",
            "The API is not returning the expected values. "
            "This usually occures in testing w/ dummy endpoint",
            0xA31523,
            discord,
        )
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
                "Misc error!",
                "There was a misc error when sending/getting data from the "
                "api and serializing it! The error goes as follows:"
                f"\n\n*{e}*",
                0xA31523,
                discord,
            )
        )

        return
    else:
        embed_color = 0x3BA315
        embed_desc_text = (
            f"The water level between {date_1} and {date_2} has been "
            f"caluclated sucessfully! The result is **{round(result, 5)}mm**."
        )

        if is_prediction:
            embed_color = 0xa3a315
            embed_desc_text += (
                "\n\n***NOTE:*** *This is a prediction and may not "
                "be accurate. We use data from Early 1993 to Feburary "
                "2019.*"
            )

        embed = embed_generator(
            "Result",
            embed_desc_text,
            embed_color,
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
        "code jam, with the theme of Global Warming. This web-portal "
        "connects to an api (that you are most likely running on your "
        "computer right now (If you are, it may be here)! It gets 2 dates, "
        "as seen on the home page and calculates the difference between the "
        "GMWL (Global Mean Water Level) in mm."
        "\n\n"
        "To save database space and show off, we have a large dataset that "
        "has been interpolated to give you precise times of the GMWL. There "
        "is also a simple prediction algorithm that was going to be machine "
        "learning but there was not enough time to test unforunatly."
    )

    await ctx.send(  # fmt: off
        embed=embed_generator("About", about_text, 0x9E15A3, discord)
    )
