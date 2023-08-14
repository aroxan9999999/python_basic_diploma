from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):
    waiting_for_service = State()
    waiting_for_quantity = State()
    waiting_for_diapason = State()
    waiting_for_country = State()
    waiting_for_city = State()
    waiting_for_search = State()
    waiting_for_history = State()

    def __init__(self, state: FSMContext):
        self.state = state

    async def set_search_type(self, search_type: str):
        await self.state.update_data(search_type=search_type)

    async def get_search_type(self):
        data = await self.state.get_data()
        return data.get("search_type")

    async def reset_search_type(self):
        await self.state.update_data(search_type=None)
