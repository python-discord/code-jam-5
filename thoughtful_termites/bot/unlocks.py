from thoughtful_termites.bot import ClimateBot


def has_unlocked(ctx: ClimateBot, name):
    unlock = ctx.db.get_unlock_by_name(name)
    return unlock.is_unlocked


def unlock_message(name):
    return f"You have not unlocked the game {name} yet, please try again later."
