from aiogram.dispatcher import FSMContext

from pkg.db.models.user import User


class ContextHelper:
    @staticmethod
    async def get_user(context: FSMContext) -> User:
        return await ContextHelper._get_context_by_name('user', context)

    @staticmethod
    async def add_user(user, context: FSMContext):
        await ContextHelper._set_context(user, 'user', context)

    @staticmethod
    async def add_some_data(data, context: FSMContext):
        await ContextHelper._set_context(data, 'data', context)

    @staticmethod
    async def get_some_data(context: FSMContext):
        return await ContextHelper._get_context_by_some_data('data', context)

    @staticmethod
    async def get_tg_id(context: FSMContext) -> User:
        return await ContextHelper._get_context_by_tg_id('telegram_id', context)

    @staticmethod
    async def add_tg_id(telegram_id, context: FSMContext):
        await ContextHelper._set_context(telegram_id, 'telegram_id', context)

    @staticmethod
    async def _set_context(data: ..., key: str, context: FSMContext) -> None:
        async with context.proxy() as context:
            context[key] = data

    @staticmethod
    async def _get_context_by_name(name: str, context: FSMContext) -> ...:
        context = await context.get_data(name)
        if context is not None:
            return context.get(name)
        raise ValueError(f'Data for key: [{name}] is not found.')

    @staticmethod
    async def _get_context_by_tg_id(tg_id: str, context: FSMContext) -> ...:
        context = await context.get_data(tg_id)
        if context is not None:
            return context.get(tg_id)
        raise ValueError(f'Data for key: [{tg_id}] is not found.')

    @staticmethod
    async def _get_context_by_some_data(data, context: FSMContext) -> ...:
        context = await context.get_data(data)
        if context is not None:
            return context.get(data)
        raise ValueError(f'Data for key: [{data}] is not found.')
