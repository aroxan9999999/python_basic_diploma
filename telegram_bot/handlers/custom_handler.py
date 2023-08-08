from aiogram.dispatcher import FSMContext

from states.user_states import UserState
from .command_strategies import CommandStrategy, Message


class CustomCommandStrategy(CommandStrategy):

    async def execute(self, message: Message, state: FSMContext):
        await message.answer("Введите услугу/товар, диапазон и количество единиц:")
        user_state = UserState(state)
        search_type = await user_state.set_search_type('custom')
        await state.update_data(salesDesc='salesDesc')
        await user_state.waiting_for_service.set()
