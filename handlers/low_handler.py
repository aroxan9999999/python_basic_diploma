from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from handlers.command_strategies import CommandStrategy
from states.user_states import UserState


class LowCommandStrategy(CommandStrategy):

    async def execute(self, message: Message, state: FSMContext):
        await message.answer("Введите услугу/товар для поиска:")
        user_state = UserState(state)
        search_type = await user_state.set_search_type('priceDesc')
        await user_state.waiting_for_service.set()
