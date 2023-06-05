from aiogram import Bot, types, executor  # библиотека для работы с телеграмными ботами
from aiogram.dispatcher import Dispatcher
from config import token
from keyboards import markup, markup_rus, markup_en

from utils import get_occupied_rooms, get_free_rooms, get_all_rooms, scheduler, on_startup, get_bookings

bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(message.text, reply_markup=markup)


@dp.message_handler(content_types=types.ContentType.TEXT)
async def reply(message: types.Message):
    if message.text == 'Русский':
        await message.answer('Русский язык', reply_markup=markup_rus)

    elif message.text == 'English':
        await message.answer('English language', reply_markup=markup_en)

    elif message.text == 'Занятые':
        rooms = get_occupied_rooms(get_bookings())
        answer = '\n'.join(rooms) if rooms else 'Все переговорки свободны'
        await message.answer(answer, reply_markup=markup_rus)

    elif message.text == 'Свободные':
        rooms = get_free_rooms(get_bookings())
        answer = '\n'.join(rooms) if rooms else 'Все переговорки заняты'
        await message.answer(answer, reply_markup=markup_rus)

    elif message.text == 'Все':
        rooms = get_all_rooms()
        answer = '\n'.join(rooms) if rooms else 'Что-то пошло не так'
        await message.answer(answer, reply_markup=markup_rus)

    elif message.text == 'Выбрать язык':
        await message.answer('Выбрать язык', reply_markup=markup)

    elif message.text == 'Occupied':
        rooms = get_occupied_rooms(get_bookings())
        answer = '\n'.join(rooms) if rooms else 'All meeting rooms are free'
        await message.answer(answer, reply_markup=markup_en)

    elif message.text == 'Free':
        rooms = get_free_rooms(get_bookings())
        answer = '\n'.join(rooms) if rooms else 'All meeting rooms are occupied'
        await message.answer(answer, reply_markup=markup_en)

    elif message.text == 'All':
        rooms = get_all_rooms()
        answer = '\n'.join(rooms) if rooms else 'Something went wrong'
        await message.answer(answer, reply_markup=markup_en)

    elif message.text == 'Choose language':
        await message.answer('Choose language', reply_markup=markup)


@dp.message_handler(content_types=types.ContentType.TEXT)
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
