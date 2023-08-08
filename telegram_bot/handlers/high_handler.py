from states.user_states import UserState
from .command_strategies import CommandStrategy, Message
from aiogram.dispatcher import FSMContext


class HighCommandStrategy(CommandStrategy):
    async def execute(self, message: Message, state: FSMContext):
        await message.answer("Введите услугу/товар для поиска:")
        user_state = UserState(state)
        search_type = await user_state.set_search_type('priceAsc')
        await user_state.waiting_for_service.set()
