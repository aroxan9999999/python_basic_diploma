import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aliexpres_api import AliExpressAPI, ALIEXPRESS_API_KEY
from aliexpress_search_result import AliExpressSearchResult
from handlers.CommandProcessor import CommandProcessor
from handlers.custom_handler import CustomCommandStrategy
from handlers.low_handler import LowCommandStrategy
from handlers.history_handler import HistoryCommandStrategy
from handlers.start_handler import StartCommandStrategy
from handlers.high_handler import HighCommandStrategy
from states.user_states import UserState
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram import executor
from database.db_manager import db_manager

API_TOKEN = '6393996954:AAHUSu0buDwhLHGDOA6MHAz99HL6pY9ogL8'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
start_strategy = StartCommandStrategy(db_manager)
low_strategy = LowCommandStrategy()
high_strategy = HighCommandStrategy()
custom_strategy = CustomCommandStrategy()
history_strategy = HistoryCommandStrategy()

command_processor = CommandProcessor()
command_processor.add_strategy('start', start_strategy)
command_processor.add_strategy("low", low_strategy)
command_processor.add_strategy("high", high_strategy)
command_processor.add_strategy("custom", custom_strategy)
command_processor.add_strategy('history', history_strategy)

db = db_manager


@dp.message_handler(commands=command_processor.get_commands())
async def handle_command(message: Message, state: FSMContext):
    command = message.get_command()[1:]  # Убираем символ "/"
    await command_processor.process(command, message, state)


@dp.message_handler(lambda message: len(message.text) > 3 and not message.text.isdigit(),
                    state=UserState.waiting_for_service)
async def get_product(message: Message, state: FSMContext):
    product = message.text
    await message.answer("Введите количество единиц для вывода:")
    await UserState.waiting_for_quantity.set()

    await state.update_data(product=product)  # Сохраняем введенный продукт


from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command


# ...

@dp.message_handler(Command("start"))
async def start_search(message: types.Message):
    await message.answer("Давайте начнем поиск товаров! Введите ключевые слова для поиска.")


@dp.message_handler(Command("help"))
async def show_help(message: types.Message):
    help_text = (
        "Привет! Я бот для поиска товаров на AliExpress. Вот список доступных команд:\n"
        "/start - Начать новый поиск\n"
        "/help - Вывести эту справку\n"
        "/high - Показать товары с высокой ценой\n"
        "/low - Показать товары с низкой ценой\n"
        "/custom - Настроить параметры поиска\n"
    )
    await message.answer(help_text)


@dp.message_handler(lambda message: message.text.isdigit(), state=UserState.waiting_for_quantity)
async def get_count(message: Message, state: FSMContext):
    count = int(message.text)
    await state.update_data(count=count)
    await message.answer('Страна для поиска')
    await UserState.waiting_for_country.set()


@dp.message_handler(lambda message: len(message.text) > 3 and not message.text.isdigit(),
                    state=UserState.waiting_for_country)
async def get_country(message: Message, state: FSMContext):
    country = message.text
    await state.update_data(country=country)
    await message.answer('Ваш Город')
    await UserState.waiting_for_city.set()


@dp.message_handler(lambda message: message.text, state=UserState.waiting_for_city)
async def get_city(message: types.Message, state: FSMContext):
    search_button = KeyboardButton("Search")
    keyboard = ReplyKeyboardMarkup().add(search_button)
    city = message.text
    await state.update_data(city=city)
    if 'salesDesc' in await state.get_data():
        await message.answer('ведит едиапазон цен пример 10-50')
        await UserState.waiting_for_diapason.set()
    else:
        await message.answer('Press thпe Search button to start the search:', reply_markup=keyboard)
        await UserState.waiting_for_search.set()


@dp.message_handler(lambda message: len(message.text.split('-')) > 1, state=UserState.waiting_for_diapason)
async def get_diapason(message: types.Message, state: FSMContext):
    diapason = message.text.split('-')
    if not (diapason[0].isdigit() and diapason[1].isdigit() and int(diapason[0]) < int(diapason[1])):
        await UserState.waiting_for_diapason.set()
    startPrice, endPrice = int(diapason[0]), int(diapason[1])
    await state.update_data(endPrice=endPrice)
    await state.update_data(startPrice=startPrice)
    search_button = KeyboardButton("Search")
    keyboard = ReplyKeyboardMarkup().add(search_button)
    await message.answer('Press thпe Search button to start the search:', reply_markup=keyboard)
    await UserState.waiting_for_search.set()


async def send_search_results_message(search_result, message):
    total_results = search_result.get_total_results()
    items = search_result.get_items()

    if items:
        for item in items:
            item_id = item['itemId']
            title = item.get('title', '---')
            image_url = item['image']
            promotion_price = item.get('promotionPrice', 0)
            price = item.get('price') if item.get('price') else 0
            currency = search_result.settings['currency']
            item_url = item['itemUrl']
            if item_url.startswith("//"):
                item_url = "http:" + item_url
            if image_url.startswith("//"):
                image_url = "http:" + image_url
            print(item_url)
            caption = f"<a href='{item_url}'>{title}</a>\nPrice: {promotion_price} {currency}"
            photo = await bot.send_photo(message.chat.id, photo=image_url, caption=caption, parse_mode='HTML', )
            db.add_search_result(message.from_user.id, title, price, promotion_price, item_url, image=image_url)

        else:
            status_code = search_result.get_status_code()
            status_message = search_result.get_status_message()
            await message.answer(f"Status Code: {status_code}\nStatus Message: {status_message}")


@dp.message_handler(lambda message: message.text.lower() == "search", state=UserState.waiting_for_search)
async def start_search(message: types.Message, state: FSMContext):
    user_state = UserState(state)
    data = await state.get_data()
    aliexpres = AliExpressAPI(ALIEXPRESS_API_KEY)
    product = data['product']
    search_type = data['search_type']
    count = data['count']
    country = data['country']
    city = data['city']
    search_type = await user_state.get_search_type()
    if search_type == 'salesDesc':
        startPrice, endPrice = data['startPrice'], data['endPrice']
        result = aliexpres.search_items(query=product, region=country, sort=search_type, start_price=startPrice,
                                        end_price=endPrice)
    else:
        result = aliexpres.search_items(query=product, region=country, sort=search_type)
    search_result = AliExpressSearchResult(result, count)
    await send_search_results_message(search_result, message)
    await state.finish()


@dp.message_handler(lambda message: message.text.lower() == "/history", state=UserState.waiting_for_history)
async def history_command(message: types.Message, state: FSMContext):
    print('start history')
    user = db.get_user_by_id(message.from_user.id)
    if not user:
        await message.answer("User not found.")
        return

    search_results = db.get_search_results_by_user(user.id)
    if search_results:
        result_text = "<style>"
        with open("templates/styles.css", "r") as styles_file:
            result_text += styles_file.read()
        result_text += "</style>\n"

        for item in search_results:
            result_text += f'<div class="result-container">'
            result_text += f'<a href = {item.url}><div class="image"><img src="{item.image_url}" width="200" height="200"></div></a>'
            result_text += f'<div class="title">Title: {item.title}</div>'
            result_text += f'<div class="price">Price: {item.price}</div>'
            result_text += f'<div class="promotion-price">Promotion Price: {item.promotion_price}</div>'
            result_text += f'</div>'

        html_filename = f"templates/{user.username}_search_history.html"
        with open(html_filename, "w") as html_file:
            html_file.write(result_text)

        with open(html_filename, "rb") as html_file:
            await bot.send_document(message.chat.id, html_file)

        os.remove(html_filename)  # Удалить временный файл после отправки
    else:
        await message.answer("No search history found for your user.")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
