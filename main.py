from aiogram import Bot, types, executor  # библиотека для работы с телеграмными ботами
from aiogram.dispatcher import Dispatcher
from config import token
from keyboards import markup, markup_rus, markup_en
import asyncio  # библиотека для асинхронных действий, здесь нужна только для того, чтобы в фоне запустить
# функцию check_bookings
from utils import get_occupied_rooms, get_free_rooms, get_all_bookings, get_all_rooms

bot = Bot(token=token)
dp = Dispatcher(bot)

bookings = []


# каждые пять минут обращается к сервису, получая список бронирований
# сделано для того, чтобы бот не умирал при каждом сообщении, поскольку ответ от сервиса приходит секунд 20-30
async def check_bookings():
    global bookings
    while True:
        bookings = get_all_bookings()
        await asyncio.sleep(300)


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
        rooms = get_occupied_rooms(bookings)
        answer = ', '.join(rooms) if rooms else 'Все переговорки свободны'
        await message.answer(answer, reply_markup=markup_rus)

    elif message.text == 'Свободные':
        rooms = get_free_rooms(bookings)
        answer = ', '.join(rooms) if rooms else 'Все переговорки заняты'
        await message.answer(answer, reply_markup=markup_rus)

    elif message.text == 'Все':
        rooms = get_all_rooms()
        answer = ', '.join(rooms) if rooms else 'Что-то пошло не так'
        await message.answer(answer, reply_markup=markup_rus)

    elif message.text == 'Меню':
        await message.answer('Меню', reply_markup=markup)

    elif message.text == 'Occupied':
        rooms = get_occupied_rooms(bookings)
        answer = ', '.join(rooms) if rooms else 'All meeting rooms are free'
        await message.answer(answer, reply_markup=markup_en)

    elif message.text == 'Free':
        rooms = get_free_rooms(bookings)
        answer = ', '.join(rooms) if rooms else 'All meeting rooms are occupied'
        await message.answer(answer, reply_markup=markup_en)

    elif message.text == 'All':
        rooms = get_all_rooms()
        answer = ', '.join(rooms) if rooms else 'Something went wrong'
        await message.answer(answer, reply_markup=markup_en)

    elif message.text == 'Menu':
        await message.answer('Menu', reply_markup=markup)


@dp.message_handler(content_types=types.ContentType.TEXT)
async def echo(message: types.Message):
    await message.answer(message.text)


async def main():
    # собственно запуск функции в фоне
    await asyncio.create_task(check_bookings())
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
