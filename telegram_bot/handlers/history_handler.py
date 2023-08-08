from aiogram.dispatcher import FSMContext
from states.user_states import UserState
from .command_strategies import CommandStrategy, Message


class HistoryCommandStrategy(CommandStrategy):
    async def execute(self, message: Message, state: FSMContext):
        user_state = UserState(state)
        await user_state.waiting_for_history.set()
