from aiogram.utils.exceptions import NotEnoughRightsToRestrict
from pkg.db.user_func import delete_user_by_id
from loader import bot


async def delete_user(user_id, channels):
    for channel in channels:
        try:
            await bot.kick_chat_member(chat_id=channel, user_id=user_id)
        except NotEnoughRightsToRestrict as e:
            print(e)
    await delete_user_by_id(user_id)
