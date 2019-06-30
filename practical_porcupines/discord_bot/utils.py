import datetime


def embed_generator(title, desc, colour, discord):
    """
    This helper func generates a simple embed
    """

    embed = discord.Embed(color=colour)

    embed.add_field(name=title, value=desc)

    embed.set_footer(text=f"Jilk.pw Bot, {datetime.datetime.now()}")

    return embed


async def decode_diff_resp(difference_obj):
    """
    > Gets api response
    - difference_obj: aiohttp-made response object
    < Returns mm difference
    x Returns error message in place of mm
    """

    if "body" in difference_obj:
        if "wl_difference" in difference_obj["body"]:
            return difference_obj["body"]["wl_difference"]  # Return difference part

    return "ERROR 1001: API returning wrong values!"
