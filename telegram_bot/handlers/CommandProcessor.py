from aiogram.dispatcher import FSMContext


class CommandProcessor:

    def __init__(self):
        self.strategies = {}

    def add_strategy(self, command, strategy):
        self.strategies[command] = strategy

    async def process(self, command, message, state: FSMContext):
        strategy = self.strategies.get(command)
        if strategy:
            await strategy.execute(message, state)
        else:
            await message.answer("Команда не распознана")

    def get_commands(self):
        return [comand for comand in self.strategies.keys()]
