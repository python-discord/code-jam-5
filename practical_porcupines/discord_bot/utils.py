import re


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

    # If difference_obj is not a aiohttp response object
    if difference_obj is dict:
        error_code = difference_obj["status"]
        return f"ERROR {error_code}: API not responding!"

    decoded_obj = await difference_obj.text()  # Decode

    try:
        return decoded_obj["body"]["wl_difference"]  # Return difference part
    except:
        return "ERROR 1001: API returning wrong values!"


def check_date(date):
    """
    > Gets date
    - String: Date
    < Bool: Valid
    x Bool: Invalid
    """

    date_pattern = (
        "(19[0-9]{2}|2[0-9]{3})((:((0[1-9]|1[012]):"  # year & month
        "([123]0|[012][1-9]|31))(:([01][0-9]|2[0-3]):"  # day and hour
        "([0-5][0-9]):([0-5][0-9]))?)?)?"  # minute and second
    )

    return True if re.match(date_pattern, date) else False
