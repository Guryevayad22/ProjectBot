from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from config import token

bot = Bot(token=token)
dp = Dispatcher(bot)