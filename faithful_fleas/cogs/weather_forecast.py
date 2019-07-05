import logging
import os
import time

import aiohttp

import discord
from discord.ext import commands

from faithful_fleas.utils import sql_func as sql


logger = logging.getLogger(__name__)


class WeatherForecast(commands.Cog):
    """A cog for weather forecast"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='location', invoke_without_command=True)
    async def location(self, ctx):
        """Commands that can be used to get access to weather forecast.Start off by using 'set'."""
        await ctx.send_help("location")

    @location.command(name="set", aliases=['add', 'register'])
    async def set_user_location(self, ctx, latitude: float, longitude: float):
        """
        Register your location with the bot to access weather forecast.

        Use any one of the following websites to get your location co-ordinates:
        - https://www.latlong.net/
        - https://www.maps.ie/coordinates.html
        """

        check = await self.check_existance(ctx.author.id)
        if check:
            return await ctx.send("You have already registered!")

        sql_code = "INSERT INTO locations VALUES(?, ?, ?)"
        values = (ctx.author.id, latitude, longitude)
        result = await sql.database_update(sql_code, values)

        if result is True:
            return await ctx.send("Location registered!")
        else:
            return await ctx.send("Looks like there was an error!Location could not be registered.")

    @location.command(name="remove", aliases=["del"])
    async def remove_user_location(self, ctx):
        """Unregister your location with the bot."""

        check = await self.check_existance(ctx.author.id)
        if not check:
            return await ctx.send("You have not registered!")

        user_id = ctx.author.id
        sql_code = "DELETE FROM locations WHERE discordID = ?"
        values = (user_id, )
        result = await sql.database_update(sql_code, values)

        if result is True:
            return await ctx.send("Location removed!")
        else:
            return await ctx.send("Looks like there was an error! Location could not be removed.")

    @staticmethod
    async def check_existance(author_id):
        """This function checks whether the user_id is present in the database."""

        sql_code = "SELECT * FROM locations where discordID = ?"
        value = (author_id, )
        check_result = await sql.database_query(sql_code, value)
        print(check_result)
        if check_result:
            return True
        else:
            return False

    @commands.command(name='forecast')
    async def forecast(self, ctx, forecast_type: str):
        """
        A weather forecast command.

        Parameters to be passed :
        -forecast_type
            Forecast type are divided into 2:
            - Hourly.
            - Daily.
        """
        sql_code = "SELECT * FROM locations where discordID = ?"
        value = (ctx.author.id, )
        result = await sql.database_query(sql_code, value)
        key = os.environ.get("DARKSKY_KEY")
        latitude = result[0][1]
        longitude = result[0][2]
        exclude = ['daily', 'hourly', 'currently', 'flags']
        exclude.remove(forecast_type)
        if time:
            url = f"https://api.darksky.net/forecast/{key}/" \
                  f"{latitude}, {longitude}, {time}?exclude={exclude}"
        else:
            url = f"https://api.darksky.net/forecast/{key}/" \
                  f"{latitude}, {longitude}?exclude={exclude}"
        data = await self.fetch(url)
        await self.build_embed(ctx, forecast_type, data)

    async def fetch(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                return data

    @staticmethod
    async def build_embed(ctx, forecast_type, data):
        """A function which makes the embed depending on the forecast type."""

        embed = discord.Embed(colour=discord.Colour.orange())
        embed.title = f"Weather Forecast\nType: {forecast_type}"
        embed.set_footer(text="The weather forecast data has been taken from Dark Sky API.")

        # The variable names are taken in accordance with the

        if forecast_type == 'daily':
            daily = data['daily']
            current_week_summery = daily['summary']
            today_data = daily['data'][0]
            today_summery = today_data['summary']

            precip_intensity_max_time = time.strftime(
                '%H:%M:%S',
                time.localtime(today_data['precipIntensityMaxTime']))

            temperature_high = today_data['temperatureHigh']

            temperature_high_time = time.strftime(
                '%H:%M:%S',
                time.localtime(today_data['temperatureHighTime']))

            embed.description = f"**This Week**: {current_week_summery}\n"
            embed.description += f"**Today**: {today_summery}\n"
            embed.description += f"**Maximum Precipitation** at {precip_intensity_max_time}\n"
            embed.description += f"**Maximum Temperature**: {temperature_high}°F at" \
                                 f" {temperature_high_time}"
            return await ctx.send(embed=embed)

        elif forecast_type == 'currently':
            currently = data['currently']
            summary = currently['summary']
            temperature = currently['temperature']
            precip_intensity = currently['precipIntensity']
            embed.description = f"**Today**: {summary}\n"
            embed.description += f"**Temperature**: {temperature}°F\n"
            embed.description += f"**Precipitation Intensity**: {precip_intensity} mm/hour"
            return await ctx.send(embed=embed)


def setup(bot):
    """Cog load function."""

    bot.add_cog(WeatherForecast(bot))
    logger.info("WeatherForecast cog loaded.")
