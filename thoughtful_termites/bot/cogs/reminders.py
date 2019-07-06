import asyncio
import datetime
import discord

from discord.ext import commands

from ...shared.goal_db.reminder_day import day_to_int as reminder_days


class ReminderTimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        """Custom converter for the `>reminders` group command.

        This function does the following lookups:

            1. By day (`Monday`, `Tuesday`, `Wednesday` etc.)
            2. By Goal ID (1, 2, 5, 10 etc.)
            3. By goal name (`Ride Bike`, `Drink Water`, etc.)

        Returns
        ---------
        reminder : :class:`list` of :class:`~Reminder`: The reminder being requested.
        """
        if argument in reminder_days.keys():
            # it's a day of week
            reminder = await ctx.db.get_reminders_on_day_async(argument)
            if not reminder:
                raise commands.BadArgument(f'No reminders found on {argument}.')
            return list(reminder)

        try:
            # it's a goal ID
            goal_id = int(argument)

            reminder = await ctx.db.get_reminder_by_goal_id_async(goal_id)
            if not reminder:
                raise commands.BadArgument('Goal ID not found.')
            return [reminder]
        except ValueError:
            pass

        reminder = await ctx.db.get_reminder_by_goal_name_async(argument)
        if not reminder:
            raise commands.BadArgument('Goal name not found.')
        return [reminder]


class Reminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._reminder_task = bot.loop.create_task(self.wait_for_reminders)

    async def cog_command_error(self, ctx, error):
        """Send errors to the user if a bad argument has been passed.
        """
        if isinstance(error, commands.BadArgument):
            return await ctx.send(str(error))

    async def get_next_reminder(self):
        """A helper method to get the next occuring reminder.

        Returns
        --------
        reminder: :class:`~Reminder` - this also has a `delta` attribute: time delta until called.
        """
        next_reminder = await self.bot.db.get_next_reminder_async()
        now = datetime.datetime.now()

        days = now.day - int(next_reminder.day)
        hours = now.hour - int(next_reminder.time)
        delta = datetime.timedelta(days=days, hours=hours)
        next_reminder.delta = delta

        return next_reminder

    async def wait_for_reminders(self):
        """Background to handle and dispatch reminders.

        This function finds the next occuring reminder and sleeps until then,
        dispatches a done callback event, and repeats the process.
        """
        try:
            while not self.bot.is_closed():
                reminder = await self.get_next_reminder()
                seconds = reminder.delta.total_seconds()

                if seconds > 0:
                    await asyncio.sleep(seconds)

                self.bot.dispatch('on_reminder_complete', reminder)
        except asyncio.CancelledError:
            raise
        except Exception:
            self._reminder_task.cancel()
            self._reminder_task = self.bot.loop.create_task(self.wait_for_reminders)

    @commands.Cog.listener()
    async def on_reminder_complete(self, reminder):
        """Done callback that is called when a reminder is complete.

        Parameters
        ---------------
        reminder : :class:`~Reminder` - The reminder to call.
        """
        channel = self.bot.channel
        goal = reminder.goal
        now = datetime.datetime.now()

        fmt = f"Reminder: Your Goal is Complete!\n{goal.desc}"
        time = datetime.datetime(year=now.year, month=now.month, day=reminder.day, hour=reminder.time)

        e = discord.Embed(colour=self.bot.colour,
                          title=goal.name,
                          description=fmt,
                          timestamp=time)
        e.set_author(name=str(self.bot.owner), icon_url=self.bot.owner.avatar_url)
        e.set_footer(text="Goal Set")
        await channel.send(embed=e, content=self.bot.owner.mention)

    @commands.group(invoke_without_command=True, aliases=['reminder'])
    async def reminders(self, ctx, *, to_get: ReminderTimeConverter = None):
        """Get all reminders with given parameters.

        Parameters
        -----------------
        Pass in any of the following:

            • Day of the week: `Sunday`, `Monday`, `Thursday` etc. to get reminders for that day.
            • Goal ID: eg. `1`, `5`, etc: to get reminders for that goal
            • Goal Name: eg. `Drive Less`
            • Pass in nothing to get all reminders.

        Examples
        ------------
        • `>reminders`
        • `>reminders Monday`
        • `>reminders Drive Less`
        • `>reminders 5`

        Aliases
        --------------
        • `>reminders` (primary)
        • `>reminder`
        """
        if ctx.invoked_subcommand is not None:
            return
        await ctx.invoke(self.reminders_list, to_get=to_get)
        # TODO: `>reminder create`, `>reminder delete`

    @reminders.command(name='list')
    async def reminders_list(self, ctx, *, to_get: ReminderTimeConverter = None):
        """Get all reminders with given parameters.

        Parameters
        -----------------
        Pass in any of the following:

            • Day of the week: `Sunday`, `Monday`, `Thursday` etc. to get reminders for that day.
            • Goal ID: eg. `1`, `5`, etc: to get reminders for that goal
            • Goal Name: eg. `Drive Less`
            • Pass in nothing to get all reminders.

        Examples
        ------------
        • `>reminders`
        • `>reminders Monday`
        • `>reminders Drive Less`
        • `>reminders 5`

        Aliases
        --------------
        • `>reminders list` (primary)
        • `>reminder list`
        """
        if not to_get:
            to_get = list(self.bot.db.get_reminders())

        fmt = '\n'.join(f'• {i}. {n.goal.name} -- {str(n.day)} {str(n.time)}' for i, n in enumerate(to_get))
        e = discord.Embed(colour=self.bot.colour,
                          title='Reminders',
                          description=fmt,
                          timestamp=datetime.datetime.now())
        e.set_author(name=str(self.bot.owner), icon_url=self.bot.owner.avatar_url)
        await ctx.send(embed=e)

    @reminders.command(name='view')
    async def reminders_view(self, ctx, reminder_id: int):
        """View a reminder with given ID.

        Parameters
        -----------------
        Pass in any of the following:

            • Reminder ID: integer ID of the reminder.

        Examples
        ------------
        • `>reminders view 1`
        • `>reminder view 10`

        Aliases
        --------------
        • `>reminders view` (primary)
        • `>reminder view`
        """
        reminder = await self.bot.db.get_reminder_by_id_async(reminder_id)
        if not reminder:
            raise commands.BadArgument('Reminder ID not found.')

        fmt = f'• {reminder.goal.name} -- {str(reminder.day)} {str(reminder.time)}'
        e = discord.Embed(colour=self.bot.colour,
                          title=f'Reminder ID: {reminder_id}',
                          description=fmt,
                          timestamp=datetime.datetime.now())
        e.set_author(name=str(self.bot.owner), icon_url=self.bot.owner.avatar_url)
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Reminders(bot))
