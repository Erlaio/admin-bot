import random

from pkg.db.user_func import get_tg_id_if_moderator


class ModeratorUtils:
    BLACK_LIST = []

    async def get_random_moder(self):
        moderator_id_list = await get_tg_id_if_moderator()
        moderator_id = random.choice(moderator_id_list)
        self.BLACK_LIST.append(moderator_id)

        if len(moderator_id_list) == len(self.BLACK_LIST):
            self.BLACK_LIST = []

        return moderator_id
