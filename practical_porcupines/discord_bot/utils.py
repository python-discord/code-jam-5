import datetime


def embed_generator(title, desc, colour, discord):
    """
    This helper func generates a simple embed
    """

    embed = discord.Embed(color=colour)

    embed.add_field(name=title, value=desc)

    embed.set_footer(
        text=f"Practical-Porcupine Bot, {datetime.datetime.now()}"
    )

    return embed
