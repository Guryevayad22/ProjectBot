from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import token

bot = Bot(token=token)
dp = Dispatcher(bot)