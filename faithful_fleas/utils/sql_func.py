import logging

import aiosqlite


logger = logging.getLogger(__name__)


async def database_update(sql_code, values=()):
    """A function that updates/inserts value/s to the database."""

    try:
        async with aiosqlite.connect("faithful_fleas/bot.db") as db:

            logger.info("Database connection made successfully.")
            await db.execute(sql_code, values)
            await db.commit()
            logger.info(f"SQL code executed successfully"
                        f"SQL_CODE: {sql_code}"
                        f"Values: {values}")
            return True

    except Exception as e:

        logging.error(f"An error occured in DATABASE_QUERY method,"
                      f"ERROR :\n {str(e)}")
        return False


async def database_query(sql_code, values=()):
    """A function which can be used to query the database."""

    try:
        async with aiosqlite.connect("faithful_fleas/bot.db") as db:

            logger.info("Database connection made successfully.")

            async with db.execute(sql_code, values) as cursor:
                data = await cursor.fetchall()
                logger.info(f"SQL code executed successfully"
                            f"SQL_CODE: {sql_code}"
                            f"Values: {values}")

            return data

    except Exception as e:

        logging.error(f"An error occured in DATABASE_QUERY method,"
                      f"ERROR :\n {str(e)}")
