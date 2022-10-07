from contextlib import asynccontextmanager

import asyncpg

from pkg.settings import settings


@asynccontextmanager
async def connect_to_db():
    try:
        conn = await asyncpg.connect(
            host=settings.POSTGRES_HOSTNAME,
            database=settings.POSTGRES_DATABASE,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            port=settings.POSTGRES_PORT)

        yield conn
        await conn.close()

    except Exception as ex:
        print(ex)
