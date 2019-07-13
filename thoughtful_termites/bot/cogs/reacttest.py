import asyncio
import discord
import random
import time

from discord.ext import commands


class ReactTest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reacttest(self, ctx):
        """
        Test you reaction speed! Hit the emoji when the embed turns green
        """
        # check if reaction is same reaction and reacter is author
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '\N{OCTAGONAL SIGN}'

        embed = discord.Embed(colour=0x0000ff)
        embed.set_author(
            name="Press the reaction when the embed turns green", icon_url=ctx.author.avatar_url
        )
        send = await ctx.send(embed=embed)
        await send.add_reaction('\N{OCTAGONAL SIGN}')
        # random delay time
        delaytime = random.randint(10, 30) / 10
        # cheating or worked ok
        while True:
            try:
                # wait for check. timeout is random delay time.
                # If check returns true then they cheated
                await self.bot.wait_for('reaction_add', check=check, timeout=delaytime)
                e = discord.Embed(colour=0xff0000)
                e.set_author(name="No Cheating!",
                             icon_url='https://cdn.shopify.com/s/files/1/1061/1924/products/'
                                      'Very_Angry_Emoji_7f7bb8df-d9dc-'
                                      '4cda-b79f-5453e764d4ea_large.png?v=1480481058')
                await send.edit(embed=embed)
            except asyncio.TimeoutError:
                break
                # continue

        e = discord.Embed(colour=0x00ff00)
        e.set_author(name="GO!", icon_url=ctx.author.avatar_url)
        # start timer
        start = time.perf_counter()
        await send.edit(embed=e)
        while True:
            try:
                # wait for reaction add. timeout 3 seconds
                await self.bot.wait_for('reaction_add', check=check, timeout=3.0)
                # finish timer
                end = time.perf_counter()
                # subtract bot latency coz that's not fair to factor in my slowness.
                # still has delay from when start to finish
                #  check which is apparantly for some a lot and annoying
                dif = round((end - start - self.bot.latency), 4)
                # didnt cheat

                # reaction time
                desc = f'**{dif}** seconds'

                e = discord.Embed(colour=0x0000ff)
                e.set_author(name="Your reaction time is....", icon_url=ctx.author.avatar_url)
                e.description = desc
                # send results
                await send.edit(embed=e)
                break
            # took longer than 3 sec
            except asyncio.TimeoutError:
                e = discord.Embed(colour=0xff0000)
                e.set_author(name="You took too long!", icon_url=ctx.author.avatar_url)
                await send.edit(embed=e)
                break


def setup(bot):
    bot.add_cog(ReactTest(bot))
