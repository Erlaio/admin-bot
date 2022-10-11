import asyncio
import datetime
import random
from typing import List

from pydantic import parse_obj_as

from pkg.db.db_connect import connect_to_db
from pkg.db.models.user import User


async def add_new_user(data: User):
    async with connect_to_db() as conn:
        join_time = datetime.date.today()
        await conn.execute(
            'INSERT INTO users (telegram_id, surname, name, patronymic, gender,'
            'photo, email, git, behance, tg_login, desired_department, skills, '
            'goals, city, source_of_knowledge, lead_description, join_time, '
            'is_moderator, is_approved) '
            'VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, '
            '$14, $15, $16, $17, $18, $19);',
            data.telegram_id,
            data.surname,
            data.name,
            data.patronymic,
            data.gender,
            data.photo,
            data.email,
            data.git,
            data.behance,
            data.tg_login,
            data.desired_department,
            data.skills,
            data.goals,
            data.city,
            data.source_of_knowledge,
            data.lead_description,
            join_time,
            data.is_moderator,
            data.is_approved)


async def get_user_by_id(user_id: int) -> User:
    async with connect_to_db() as conn:
        rec = await conn.fetchrow(
            'SELECT '
            'user_id, telegram_id, surname, name, patronymic, gender, photo, email, git, '
            'behance, tg_login, desired_department, skills, goals, city, source_of_knowledge,'
            'lead_description, join_time, is_moderator, is_approved '
            'FROM users ' 
            'WHERE user_id = $1;',
            user_id
        )
        data = parse_obj_as(User, rec)
        return data


async def get_user_by_tg_login(tg_login: str) -> User:
    async with connect_to_db() as conn:
        rec = await conn.fetchrow(
            'SELECT '
            'user_id, telegram_id, surname, name, patronymic, gender, photo, email, git, '
            'behance, tg_login, desired_department, skills, goals, city, source_of_knowledge,'
            'lead_description, join_time, is_moderator, is_approved '
            'FROM users '
            'WHERE tg_login = $1;',
            tg_login
        )
        data = parse_obj_as(User, rec)
        return data


async def get_user_by_tg_id(tg_id: int) -> User or None:
    async with connect_to_db() as conn:
        rec = await conn.fetchrow(
            'SELECT '
            'user_id, telegram_id, surname, name, patronymic, gender, photo, email, git, '
            'behance, tg_login, desired_department, skills, goals, city, source_of_knowledge,'
            'lead_description, join_time, is_moderator, is_approved '
            'FROM users '
            'WHERE telegram_id = $1;',
            tg_id
        )
        if rec is None:
            return None
        data = parse_obj_as(User, rec)
        return data


async def get_all_users() -> List[User]:
    async with connect_to_db() as conn:
        rec = await conn.fetch('SELECT * FROM users;')
        result = parse_obj_as(List[User], rec)
        return result


async def delete_user_by_id(user_id: int):
    async with connect_to_db() as conn:
        await conn.execute(
            'DELETE FROM users '
            'WHERE user_id = $1;',
            user_id
        )


async def delete_user_by_tg_id(telegram_id: int):
    async with connect_to_db() as conn:
        await conn.execute(
            'DELETE FROM users '
            'WHERE telegram_id = $1;',
            telegram_id
        )


async def update_user_status(telegram_id: int, is_moder: int = 1,
                             approved: int = 1):
    async with connect_to_db() as conn:
        await conn.execute(
            'UPDATE users '
            'SET is_moderator = $1, is_approved = $2 '
            'WHERE telegram_id = $3;',
            is_moder,
            approved,
            telegram_id
        )


async def update_user_by_id(user_id: int, data: User):
    async with connect_to_db() as conn:
        await conn.execute(
            'UPDATE users '
            'SET telegram_id=$1, surname=$2, name=$3, patronymic=$4, gender=$5,'
            'photo=$6, email=$7, git=$8, behance=$9, tg_login=$10,'
            'desired_department=$11, skills=$12, goals=$13, city=$14,'
            'source_of_knowledge=$15, lead_description=$16, join_time=$17,'
            'is_moderator=$18, is_approved=$19 '
            'WHERE user_id = $20;',
            data.telegram_id,
            data.surname,
            data.name,
            data.patronymic,
            data.gender,
            data.photo,
            data.email,
            data.git,
            data.behance,
            data.tg_login,
            data.desired_department,
            data.skills,
            data.goals,
            data.city,
            data.source_of_knowledge,
            data.lead_description,
            data.join_time,
            data.is_moderator,
            data.is_approved,
            user_id
        )


async def update_user_by_telegram_id(telegram_id: int, data: User):
    async with connect_to_db() as conn:
        await conn.execute(
            'UPDATE users '
            'SET telegram_id=$1, surname=$2, name=$3,'
            'patronymic=$4, gender=$5, photo=$6, email=$7, git=$8, behance=$9,'
            'tg_login=$10, desired_department=$11, skills=$12, goals=$13,'
            'city=$14, source_of_knowledge=$15, lead_description=$16,'
            'join_time=$17, is_moderator=$18, is_approved=$19 '
            'WHERE telegram_id = $20;',
            data.telegram_id,
            data.surname,
            data.name,
            data.patronymic,
            data.gender,
            data.photo,
            data.email,
            data.git,
            data.behance,
            data.tg_login,
            data.desired_department,
            data.skills,
            data.goals,
            data.city,
            data.source_of_knowledge,
            data.lead_description,
            data.join_time,
            data.is_moderator,
            data.is_approved,
            telegram_id
        )


async def update_user_by_department(user_id: int, data: User):
    async with connect_to_db() as conn:
        await conn.execute(
            'UPDATE users '
            'SET telegram_id=$1, surname=$2, name=$3,'
            'patronymic=$4, gender=$5, photo=$6, email=$7, git=$8, behance=$9,'
            'tg_login=$10, desired_department=$11, skills=$12, goals=$13,'
            'city=$14, source_of_knowledge=$15, lead_description=$16,'
            'join_time=$17, is_moderator=$18, is_approved=$19 '
            'WHERE user_id = $20;',
            data.telegram_id,
            data.surname,
            data.name,
            data.patronymic,
            data.gender,
            data.photo,
            data.email,
            data.git,
            data.behance,
            data.tg_login,
            data.desired_department,
            data.skills,
            data.goals,
            data.city,
            data.source_of_knowledge,
            data.lead_description,
            data.join_time,
            data.is_moderator,
            data.is_approved,
            user_id
        )


async def update_lead_description(telegram_id: int, description: str):
    async with connect_to_db() as conn:
        await conn.execute(
            'UPDATE users '
            'SET lead_description = $1 '
            'WHERE telegram_id = $2;',
            description,
            telegram_id
        )


async def get_users_from_department(department_id: int) -> List[User]:
    async with connect_to_db() as conn:
        rec = await conn.fetch(
            'SELECT '
            'user_id, telegram_id, surname, name, patronymic, gender, photo, email, git, '
            'behance, tg_login, desired_department, skills, goals, city, source_of_knowledge,'
            'lead_description, join_time, is_moderator, is_approved '
            'FROM users '
            'WHERE desired_department = $1;',
            department_id
        )
    result = parse_obj_as(List[User], rec)
    return result


async def get_users_from_department_name(department_name: str) -> List[User]:
    async with connect_to_db() as conn:
        rec = await conn.fetch(
            'SELECT '
            'user_id, telegram_id, surname, name, patronymic, gender, photo, email, git, '
            'behance, tg_login, desired_department, skills, goals, city, source_of_knowledge,'
            'lead_description, join_time, is_moderator, is_approved '
            'FROM users '
            'WHERE desired_department = $1;',
            department_name
        )
    result = parse_obj_as(List[User], rec)
    return result


async def get_tg_id_if_moderator(is_moder: int = 1) -> List[int]:
    async with connect_to_db() as conn:
        records = await conn.fetch(
            'SELECT '
            'user_id, telegram_id, surname, name, patronymic, gender, photo, email, git, '
            'behance, tg_login, desired_department, skills, goals, city, source_of_knowledge,'
            'lead_description, join_time, is_moderator, is_approved '
            'FROM users '
            'WHERE is_moderator = $1;',
            is_moder
        )
    return [rec[1] for rec in records]


async def update_user_department(old_name: str, new_name: str):
    async with connect_to_db() as conn:
        await conn.execute(
            'SELECT '
            'user_id, telegram_id, surname, name, patronymic, gender, photo, email, git, '
            'behance, tg_login, desired_department, skills, goals, city, source_of_knowledge,'
            'lead_description, join_time, is_moderator, is_approved '
            'FROM users '
            'SET desired_department = $1 '
            'WHERE desired_department = $2;',
            new_name,
            old_name
        )


async def get_unapproved_users(unapproved: int = 0) -> List[User]:
    async with connect_to_db() as conn:
        rec = await conn.fetch(
            'SELECT '
            'user_id, telegram_id, surname, name, patronymic, gender, photo, email, git, '
            'behance, tg_login, desired_department, skills, goals, city, source_of_knowledge,'
            'lead_description, join_time, is_moderator, is_approved '
            'FROM users '
            'WHERE is_approved = $1;',
            unapproved
        )
    result = parse_obj_as(List[User], rec)
    return result


async def update_user_approve(telegram_id: int, approved: int = 1):
    async with connect_to_db() as conn:
        await conn.execute(
            'UPDATE users '
            'SET is_approved = $1 '
            'WHERE telegram_id = $2;',
            approved,
            telegram_id
        )


async def get_random_moder(is_moder: int = 1) -> User:
    async with connect_to_db() as conn:
        rec = await conn.fetchrow(
            'SELECT '
            'user_id, telegram_id, surname, name, patronymic, gender, photo, email, git, '
            'behance, tg_login, desired_department, skills, goals, city, source_of_knowledge,'
            'lead_description, join_time, is_moderator, is_approved '
            'FROM users '
            'WHERE is_moderator = $1;',
            is_moder
        )
    result = parse_obj_as(List[User], rec)
    return random.choice(result)


async def update_field_value(telegram_id: int, field: str, value):
    async with connect_to_db() as conn:
        await conn.execute(
            'UPDATE users '
            f'SET {field} = $1'
            'WHERE telegram_id = $2;',
            value,
            telegram_id
        )


if __name__ == '__main__':
    pass
