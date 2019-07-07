import json
import random

import discord

from datetime import datetime

from discord.ext import commands

CROP_DATA_LOCATION = './resources/crop_data.json'


def readable_time(delta_seconds):
    """Returns a human-readable string for delta seconds.
    """
    hours, remainder = divmod(int(delta_seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)

    if days:
        fmt = '{d}d {h}hr {m}min {s}sec'
    elif hours:
        fmt = '{h}hr {m}min {s}sec'
    else:
        fmt = '{m}min {s}sec'

    return fmt.format(d=days, h=hours, m=minutes, s=seconds)


def requires_account():
    """Command check to ensure the user has registered an account with the bot to play FarmerTown.
    """
    async def pred(ctx):
        db_stats = await ctx.db.get_farmertown(ctx.author.id)
        if not db_stats:
            raise commands.CheckFailure('Account not found! '
                                        'Please register with `>farmertown create`')
        ctx.db_stats = db_stats
        return True
    return commands.check(pred)


def cooldown_check():
    """Command check to ensure the user only calls specific commands every 12 hours.
    """
    async def pred(ctx):
        if not ctx.db_stats.last_used:
            await ctx.db_stats.update_last_used()
            return True

        delta = datetime.now() - ctx.db_stats.last_used
        if delta.total_seconds() < 43200:  # 12 hours
            raise commands.CheckFailure(f'You\'re on cooldown! Please wait another '
                                        f'{readable_time(43200 - delta.total_seconds())}.')
        await ctx.db_stats.update_last_used()
        ctx.db_stats = ctx.db_stats
        return True
    return commands.check(pred)


class CropConverter(commands.Converter):
    """Custom converter to convert a string to `CropDataEntry` object or raise error.
    """
    async def convert(self, ctx, argument):
        crop_data = ctx.cog.crop_data
        crop = crop_data.get_entry(name=argument.lower())
        if not crop:
            raise commands.BadArgument('Crop not found.')
        return crop


class CropData:
    """Represents a class containing all CropDataEntries.

    Parameters
    ------------
    data: :class:`dict`: The raw crop data as loaded from json file.
    db: :class:`GoalDB`: The DB instance loaded on the bot.
    """
    __slots__ = ('data', 'db')

    def __init__(self, data, db):
        self.data = data
        self.db = db

    @property
    def iterentries(self):
        """Iterable of CropDataEntries.
        """
        return (CropDataEntry(n, self.db) for n in self.data)

    @property
    def entries(self):
        """Returns a list of CropDataEntries.
        """
        return list(self.iterentries)
        # this way of creating the list, by calling list(iter comp)
        # is fastest than multiple other methods, including normal list-comps.
        # we can also use the iter in other methods such as get_entry, to improve performance.

    def get_entry(self, **attrs):
        """Returns the first :class:`CropDataEntry` that meets the attributes passed.

        An example of this looks like:

        .. code-block:: python3

            entry = CropData.get_entry(name='wheat')

        This search implements the :func:`~discord.utils.get` function
        """
        return discord.utils.get(self.iterentries, **attrs)


class CropDataEntry:
    """Represents a crop data entry.

    Parameters
    ------------
    data: :class:`dict`: The raw crop data as loaded from json file.
    db: :class:`GoalDB`: The DB instance loaded on the bot.

    Attributes
    -------------
    name: str
        The crop name
    price: int
        The crop price
    drought_risk: float
        The risk of crop being affected by drought
    average_germination: float
        The average germination rate of the crop
    sale_value: int
        The sale value of the crop
    """
    __slots__ = ('data', 'db', 'name', 'price', 'drought_risk', 'average_germination', 'sale_value')

    def __init__(self, data, db):
        self.data = data
        self.db = db
        get = data.get
        # loading `get` into a throwaway variable provides faster lookup and therefor faster object
        # creation than accessing it through dot notation every time.

        self.name = get('name')
        self.price = get('price')
        self.drought_risk = get('drought_risk')
        self.average_germination = get('average_germination')
        self.sale_value = get('sale_value')


class FarmerTown(commands.Cog):
    """Play a game of FarmerTown! Try and get the largest profit possible, and don't go bankrupt...
    """
    def __init__(self, bot):
        self.bot = bot

        with open(CROP_DATA_LOCATION) as fp:
            self.raw_crop_data = json.load(fp)

        self.crop_data = CropData(self.raw_crop_data, bot.db)

    async def cog_command_error(self, ctx, error):
        if isinstance(error, (commands.BadArgument, commands.MissingRequiredArgument,
                              commands.CheckFailure)):
            await ctx.send(str(error))

        try:
            await ctx.db_stats.remove_last_used()
        except AttributeError:
            # command wasn't decorated with `@requires_account`
            pass

    @commands.group(invoke_without_command=True)
    async def farmertown(self, ctx):
        """Play a game of FarmerTown with the bot.
        This game is complex - read carefully!

        • You can sow a crop every 12 hours
        • You can get the results of that crop 12 hours later
        • Each crop has differing levels of drought risk, and germination rates.
            Generally, the higher the risk, the higher the profit.
        • The aim of the game is to get the most money.
        • If a drought occurs, the germination rate is 0, and the profit is 0. Costs are the same.
        • Costs are calculated by the raw cost of the crop * the tonnes put in
        • Profit is calculated by the sale price * tonnes put in * germination rate.

        How to get started:
        • Create an account with `>farmertown create`
        • See a list of crops to plant with `>farmertown croplist`
        • Sow a crop with `>farmertown sow CROP_NAME_HERE`
        • Wait 12 hours
        • Find the results of the crop and add this to your bank balance with `>farmertown results`
        • Repeat!
        • Check your balance with `>farmertown balance`
        """
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @farmertown.command()
    async def cropinfo(self, ctx, *, crop: CropConverter = None):
        """Get cropinfo for all crops or a specific crop

        Parameters
        --------------
        • crop: the name of the crop to get info for. If none, gets info for all crops.

        Aliases
        ----------
        • `>farmertown cropinfo` (default)
        • `>farmertown crops`
        • `>farmertown crop`

        Examples
        -------------
        • `>farmertown cropinfo wheat`
        • `>farmertown cropinfo barley`
        • `>farmertown crops`
        """
        if crop:
            entries = [crop.data]
        else:
            entries = self.raw_crop_data
        e = discord.Embed(colour=self.bot.colour,
                          title='Crop Info',
                          timestamp=datetime.utcnow()
                          )
        for n in entries:
            fmt = f"• Price: ${n['price']}\n" \
                  f"• Sale Value: ${n['sale_value']}\n" \
                  f"• Drought Risk: {n['drought_risk']}%\n" \
                  f"• Average Germination Rate: {n['average_germination']}%"
            e.add_field(name=n['name'],
                        value=fmt,
                        inline=False)
        await ctx.send(embed=e)

    @farmertown.command(name='create')
    async def farmertown_create(self, ctx):
        """Create an account with FarmerTown.
        The bot will walk you through the process.
        """
        current_stats = await ctx.db.get_farmertown(ctx.author.id)
        if current_stats:
            return await ctx.send(f'You already have a farm claimed, {current_stats.farmer_name}!')

        def check(mes):
            return mes.channel == ctx.channel and mes.author == ctx.author

        await ctx.send('Please send the name of your farmer. '
                       'If you want to be called `Farmer John`, just send `John`. '
                       'Please keep it to less than 20 characters.')
        message = await self.bot.wait_for('message', check=check)
        if not len(message.content) < 20:
            return await ctx.send('Failed. Please run the command again '
                                  'and use a name less than 20 characters.')
        await ctx.db.create_farm(ctx.author.id, f'Farmer {message.content}')
        await ctx.send('All Done \N{WHITE HEAVY CHECK MARK}')

    @farmertown.command(name='balance')
    @requires_account()
    async def farmertown_balance(self, ctx):
        """Get your FarmerTown balance.
        You must have a FarmerTown account to use this command.
        """
        current_stats = ctx.db_stats
        e = discord.Embed(colour=self.bot.colour,
                          title=f'{current_stats.farmer_name}\'s Current Balance',
                          timestamp=datetime.utcnow()
                          )
        # e.add_field(name='Cash',
        #             value=f'${current_stats.cash}',
        #             inline=False
        #             )
        # e.add_field(name='Debt',
        #             value=f'${current_stats.debt}',
        #             inline=False
        #             )
        # e.add_field(name='Bank Balance',
        #             value=f'${current_stats.bank}',
        #             inline=False
        #             )
        e.add_field(name='Total',
                    value=f'${current_stats.cash}',
                    inline=False)
        await ctx.send(embed=e)

    @farmertown.command(name='sow')
    @requires_account()
    @cooldown_check()
    async def farmertown_sow(self, ctx, *, crop: CropConverter):
        """Sow a crop... will your risk pay the reward?

        Parameters
        -------------
        • crop: The name of the crop to sow. Find these with `>farmertown cropinfo`

        You must have a FarmerTown account to use this game.
        You can only use this command once every 12 hours."""
        def check(mes):
            return mes.channel == ctx.channel and mes.author == ctx.author

        await ctx.send(f'How many tonne of {crop.name} would you like to plant? '
                       f'Must be less than 20.')
        m = await self.bot.wait_for('message', check=check)
        try:
            quantity = int(m.content)
        except ValueError:
            await ctx.db_stats.remove_last_used()
            return await ctx.send('That was not a number! Please try the command again...')
        if quantity > 20:
            await ctx.db_stats.remove_last_used()
            return await ctx.send('Please try the command again with a number less than 20.')

        drought = random.choices(population=[True, False],
                                 weights=[crop.drought_risk, 1 - crop.drought_risk]
                                 )
        if drought is True:
            await ctx.db_stats.new_decision(crop_name=crop.name, drought=True, germination=0,
                                            profit=0, loss=crop.price * quantity
                                            )

        germ_rate = random.choices(population=[i for i in range(100)],
                                   weights=[i**(crop.average_germination / 10) for i in range(100)]
                                   )[0] / 100

        await ctx.db_stats.new_decision(crop_name=crop.name, drought=False, germination=germ_rate,
                                        profit=(germ_rate * quantity * crop.sale_value),
                                        loss=(crop.price * quantity)
                                        )
        await ctx.send('Crop has been sown! Please check back in 12 hours to see how it grew.')

    @farmertown.command(name='results')
    @requires_account()
    @cooldown_check()
    async def farmertown_results(self, ctx):
        """Get the results of your last crop.
        You must have a FarmerTown account to use this command.
        You can only use this command once every 12 hours.
        """
        last_decision = await ctx.db_stats.last_decision()
        crop = self.crop_data.get_entry(name=last_decision.crop_name)
        amount_sown = last_decision.loss / crop.price

        fmt = f'Decision: You planted {amount_sown} tonne of {crop.name}. ' \
              f'It had the following stats:\n' \
              f'• Cost: ${crop.price}\n' \
              f'• Sale Value: ${crop.sale_value}\n' \
              f'• Drought Risk: {crop.drought_risk}%\n' \
              f'• Average Germination: {crop.average_germination}\n'

        e = discord.Embed(colour=self.bot.colour,
                          title=f'Last Decision: {last_decision.crop_name}',
                          description=fmt,
                          timestamp=datetime.utcnow()
                          )
        e.add_field(name='Drought',
                    value=str(True if last_decision.drought else False),
                    inline=False
                    )
        e.add_field(name='Germination',
                    value=f'{last_decision.germination}%',
                    inline=False)
        e.add_field(name='Profit',
                    value=f'${last_decision.profit}',
                    inline=False)
        e.add_field(name='Costs/Loss',
                    value=f'${last_decision.loss}',
                    inline=False)
        e.add_field(name='Total Earnings',
                    value=f'${last_decision.profit - last_decision.loss}',
                    inline=False)
        await ctx.send(embed=e)
        await ctx.db_stats.update_accounts()


def setup(bot):
    bot.add_cog(FarmerTown(bot))
