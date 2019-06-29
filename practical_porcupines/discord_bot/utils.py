def embed_generator(title, desc, colour, discord):
    """
    This helper func generates a simple embed
    """

    embed = discord.Embed(color=colour)

    embed.add_field(name=title, value=desc)

    embed.set_footer(text=f"Jilk.pw Bot, {datetime.datetime.now()}")

    return embed

def decode_diff_resp(difference_obj):
    """
    > Gets api response
    - difference_obj: aiohttp-made response object
    < Returns mm difference
    x Returns error message in place of mm
    """

    # If difference_obj is not a aiohttp response object
    if difference_obj is dict:
        error_code = difference_obj["status"]
        return f"ERROR {error_code}: API not responding!"

    # TODO test below
    # decoded_obj = await difference_obj.json()
    # return decoded_obj["body"]["wl_difference"]

    pass
