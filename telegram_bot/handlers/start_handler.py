from aiogram.dispatcher import FSMContext
from .command_strategies import CommandStrategy, Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database.db_manager import DBManager


class StartCommandStrategy(CommandStrategy):
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager

    async def execute(self, message: Message, state: FSMContext):
        user = message.from_user
        user_id = user.id
        username = user.username if user.username else 'no username'
        first_name = user.first_name if user.first_name else 'no firstname'
        last_name = user.last_name
        registered_user = self.db_manager.get_user_by_id(user_id)
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton('/history'))
        keyboard.add(KeyboardButton('/low'))
        keyboard.add(KeyboardButton('/high'))
        keyboard.add(KeyboardButton('/custom'))
        if registered_user:
            await message.answer((f"Привет, {first_name} {last_name}!"), reply_markup=keyboard)
        else:
            await self.db_manager.add_user(user_id, username, first_name, last_name)
            await message.answer(f"Привет, {first_name} {last_name}! Вы успешно зарегистрированы.",
                                 reply_markup=keyboard)
