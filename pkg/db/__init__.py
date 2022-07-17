import sqlite3
from .db_connect_sqlite import connect_to_db


@connect_to_db
def create_database(cur: sqlite3.Cursor):
    cur.executescript('''
            /*  Table Users  */
        CREATE TABLE IF NOT EXISTS "users" (
            "user_id"	INTEGER NOT NULL UNIQUE,
            "telegram_id"   INTEGER UNIQUE,
            "surname"	TEXT,
            "name"	TEXT,
            "patronymic"	TEXT,
            "gender"	TEXT,
            "photo"	BLOB,
            "email"	TEXT,
            "git"	TEXT,
            "behance"   TEXT,
            "tg_login"	TEXT,
            "desired_department"	INTEGER,
            "skills"	TEXT,
            "goals"	TEXT,
            "lead_description"	TEXT,
            "join_time"	TEXT,
            "is_moderator"	INTEGER DEFAULT 0,
            "is_approved"	INTEGER DEFAULT 0,
            PRIMARY KEY("user_id" AUTOINCREMENT));

        CREATE UNIQUE INDEX IF NOT EXISTS "user_id_index" ON "users" (
            "user_id"
        );

        /*  Table Department  */
        CREATE TABLE IF NOT EXISTS "departments" (
            "department_id"	INTEGER NOT NULL UNIQUE,
            "department"	TEXT NOT NULL,
            "team_lead"	TEXT,
            PRIMARY KEY("department_id" AUTOINCREMENT));


        CREATE UNIQUE INDEX IF NOT EXISTS "department_id_index" ON "departments" (
            "department_id");
        ''')


create_database()
