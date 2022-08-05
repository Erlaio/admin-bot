from pkg.db.user_func import delete_user_by_id
from loader import bot


async def delete_user(user_id, channels):
    for channel in channels:
        await bot.kick_chat_member(chat_id=channel, user_id=user_id)
    await delete_user_by_id(user_id)
