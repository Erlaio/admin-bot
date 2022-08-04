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
    async def _set_context(data: ..., key: str, context: FSMContext) -> None:
        async with context.proxy() as context:
            context[key] = data

    @staticmethod
    async def _get_context_by_name(name: str, context: FSMContext) -> ...:
        context = await context.get_data(name)
        if context is not None:
            return context.get(name)
        raise ValueError(f'Data for key: [{name}] is not found.')
