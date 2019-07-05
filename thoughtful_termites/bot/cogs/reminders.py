import asyncio
import datetime
import discord

from discord.ext import commands


class Reminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._reminder_task = bot.loop.create_task(self.wait_for_reminders)

    async def get_next_reminder_delta(self):
        next_reminder = await self.bot.db.get_next_reminder_async()
        now = datetime.datetime.now()

        days = now.day - int(next_reminder.day)
        hours = now.hour - int(next_reminder.time)
        delta = datetime.timedelta(days=days, hours=hours)
        next_reminder.delta = delta

        return next_reminder

    async def wait_for_reminders(self):
        try:
            while not self.bot.is_closed():
                reminder = await self.get_next_reminder_delta()
                seconds = reminder.delta.total_seconds()

                if seconds > 0:
                    await asyncio.sleep(seconds)

                await reminder.delete_async()
                self.bot.dispatch('on_reminder_complete', reminder)
        except asyncio.CancelledError:
            raise
        except Exception:
            self._reminder_task.cancel()
            self._reminder_task = self.bot.loop.create_task(self.wait_for_reminders)

    @commands.Cog.listener()
    async def on_reminder_complete(self, reminder):
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

    @commands.group()
    async def reminders(self, ctx):
        # TODO: See below
        # 1. `>reminders list` - all active reminders
        # 2. `>reminders delete` - delete active reminder
        # 3. `>reminders create` ?? create new reminder ??
        pass


def setup(bot):
    bot.add_cog(Reminders(bot))
