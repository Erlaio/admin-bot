import asyncio

import aiosqlite
from .db_connect import connect_to_db


async def create_database():
    async with connect_to_db() as conn:
        await conn.execute('''
            /*  Table Users  */
        CREATE TABLE IF NOT EXISTS "users" (
            user_id	SERIAL NOT NULL UNIQUE,
            telegram_id INT UNIQUE,
            surname	TEXT,
            name	TEXT,
            patronymic	TEXT,
            gender	TEXT,
            photo BYTEA,
            email	TEXT,
            git	TEXT,
            behance   TEXT,
            tg_login	TEXT,
            desired_department	TEXT,
            skills	TEXT,
            goals	TEXT,
            city TEXT,
            source_of_knowledge TEXT,
            lead_description	TEXT,
            join_time	DATE,
            is_moderator	INTEGER DEFAULT 0,
            is_approved	INTEGER DEFAULT 0);

        CREATE UNIQUE INDEX IF NOT EXISTS "user_id_index" ON "users" (
            "user_id"
        );

        /*  Table Department  */
        CREATE TABLE IF NOT EXISTS "departments" (
            department_id	SERIAL NOT NULL UNIQUE,
            department	TEXT NOT NULL,
            team_lead	TEXT);

        CREATE UNIQUE INDEX IF NOT EXISTS "department_id_index" ON 
        "departments" (
        "department_id");

        /*  Table Projects  */
        CREATE TABLE IF NOT EXISTS "projects" (
            "project_id" SERIAL NOT NULL UNIQUE,
            "project_name" TEXT NOT NULL,
            "team_lead" TEXT);

        CREATE UNIQUE INDEX IF NOT EXISTS "project_id_index" ON "projects" (
            "project_id");
        ''')


# if __name__ == '__main__':
#     asyncio.run(create_database())
