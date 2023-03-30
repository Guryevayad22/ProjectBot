from aiogram import Bot, types, executor
from aiogram.dispatcher import Dispatcher
from config import token
from keyboards import markup, markup_rus, markup_en

bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(message.text, reply_markup=markup)


@dp.message_handler(content_types=types.ContentType.TEXT)
async def reply(message: types.Message):
    if message.text == 'Русский':
        await message.answer('Держи', reply_markup=markup_rus)
    elif message.text == 'English':
        await message.answer('Лови аптечку', reply_markup=markup_en)


@dp.message_handler(content_types=types.ContentType.TEXT)
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
