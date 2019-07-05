import asyncio

from faithful_fleas.utils import sql_func as sql


async def setup_sql():
    """A function that creates the location table in the database."""

    sql_code = """CREATE TABLE locations(
                discordID INTEGER,
                latitude REAL,
                longitude REAL
        )"""

    result = await sql.database_update(sql_code)
    print(result)

# async def setup_sql():
#     """A function that creates the location table in the database."""
#
#     sql_code = "SELECT * FROM locations"
#     values = (100234567823529, 11.135323, 30.320035)
#
#     result = await sql.database_query(sql_code)
#     print(result)


loop = asyncio.get_event_loop()
loop.run_until_complete(setup_sql())

