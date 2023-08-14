from abc import ABC, abstractmethod
from aiogram.types import Message


class CommandStrategy(ABC):
    @abstractmethod
    async def execute(self, message: Message):
        pass
