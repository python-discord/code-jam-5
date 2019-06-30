import datetime


class DatesOutOfRange(BaseException):
    """
    For when dates are out of range
    """

    pass


class ApiReturnBad(BaseException):
    """
    When API is retuning incorrect values
    """

    pass


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
            # All clear
            return difference_obj["body"]["wl_difference"]
        elif difference_obj["meta"]["status"] == 1002:
            # Dates out of range
            raise DatesOutOfRange()

    # API returning bad values
    raise ApiReturnBad()
