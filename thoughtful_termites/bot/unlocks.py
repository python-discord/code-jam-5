from discord.ext import commands


def has_unlocked(name):
    async def pred(ctx):
        unlock = ctx.db.get_unlock_by_name(name)

        if not unlock.is_unlocked:
            raise commands.CheckFailure(unlock_message(name))
        return True

    return commands.check(pred)


def unlock_message(name):
    return f"You have not unlocked the game {name} yet, please try again later."
