import re

from aiogram import Bot, types, executor  # библиотека для работы с телеграмными ботами
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from config import token
from keyboards import markup, markup_rus, markup_en
from datetime import datetime, date
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text

from utils import get_occupied_rooms, get_free_rooms, get_all_rooms, scheduler, on_startup, get_bookings

bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())


class Choose(StatesGroup):
    free_rus = State()
    occupied_rus = State()
    free_en = State()
    occupied_en = State()
    default = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await Choose.default.set()
    await message.answer(message.text, reply_markup=markup)


@dp.message_handler(regexp='^[0-9][0-9]:[0-9][0-9]$', state=[Choose.occupied_en, Choose.occupied_rus])
async def search_occupied(message: types.Message, state: FSMContext):
    curr_state = await state.get_state()
    if curr_state == 'Choose:occupied_en':
        time_answer = 'Enter correct time'
        reply_markup = markup_en
        answer_text = 'All meeting rooms are occupied'
    else:
        time_answer = 'Укажите корректное время'
        reply_markup = markup_rus
        answer_text = 'Все переговорки заняты'

    match = re.search(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', message.text)
    check_match = re.search(r'^[0-9][0-9]:[0-9][0-9]$', message.text)
    if match:
        time_ = datetime.strptime(match.group(0), '%H:%M').time()
        date_ = date.today()
        search_time = datetime.combine(date_, time_)
        rooms = get_occupied_rooms(get_bookings(), search_time=search_time)
        answer = '\n'.join(rooms) if rooms else answer_text
        await Choose.default.set()
        await message.answer(answer, reply_markup=reply_markup)
    elif not match and check_match:
        await message.answer(time_answer, reply_markup=reply_markup)


@dp.message_handler(regexp='^[0-9][0-9]:[0-9][0-9]$', state=[Choose.free_rus, Choose.free_en])
async def search_free(message: types.Message, state: FSMContext):
    curr_state = await state.get_state()
    if curr_state == 'Choose:free_en':
        time_answer = 'Enter correct time'
        reply_markup = markup_en
        answer_text = 'All meeting rooms are free'
    else:
        time_answer = 'Укажите корректное время'
        reply_markup = markup_rus
        answer_text = 'Все переговорки свободны'

    match = re.search(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', message.text)
    check_match = re.search(r'^[0-9][0-9]:[0-9][0-9]$', message.text)
    if match:
        time_ = datetime.strptime(match.group(0), '%H:%M').time()
        date_ = date.today()
        search_time = datetime.combine(date_, time_)
        rooms = get_free_rooms(get_bookings(), search_time=search_time)
        answer = '\n'.join(rooms) if rooms else answer_text
        await message.answer(answer, reply_markup=reply_markup)
        await Choose.default.set()
    elif not match and check_match:
        await message.answer(time_answer, reply_markup=reply_markup)


@dp.message_handler(Text(equals='Русский'), state=Choose.default)
async def start(message: types.Message):
    await Choose.default.set()
    await message.answer('Русский язык', reply_markup=markup_rus)


@dp.message_handler(Text(equals='English'), state=Choose.default)
async def start(message: types.Message):
    await Choose.default.set()
    await message.answer('English language', reply_markup=markup_en)


@dp.message_handler(Text(equals='Занятые (сейчас)'), state=Choose.default)
async def start(message: types.Message):
    await Choose.default.set()
    rooms = get_occupied_rooms(get_bookings())
    answer = '\n'.join(rooms) if rooms else 'Все переговорки свободны'
    await message.answer(answer, reply_markup=markup_rus)


@dp.message_handler(Text(equals='Занятые (в указанное время)'), state=Choose.default)
async def start(message: types.Message):
    await Choose.occupied_rus.set()
    await message.answer('Укажите время в формате ЧЧ:ММ')


@dp.message_handler(Text(equals='Свободные (сейчас)'), state=Choose.default)
async def start(message: types.Message):
    await Choose.default.set()
    rooms = get_free_rooms(get_bookings())
    answer = '\n'.join(rooms) if rooms else 'Все переговорки заняты'
    await message.answer(answer, reply_markup=markup_rus)


@dp.message_handler(Text(equals='Свободные (в указанное время)'), state=Choose.default)
async def start(message: types.Message):
    await Choose.free_rus.set()
    await message.answer('Укажите время в формате ЧЧ:ММ')


@dp.message_handler(Text(equals='Все'), state=Choose.default)
async def start(message: types.Message):
    await Choose.default.set()
    rooms = get_all_rooms()
    answer = '\n'.join(rooms) if rooms else 'Что-то пошло не так'
    await message.answer(answer, reply_markup=markup_rus)


@dp.message_handler(Text(equals='Выбрать язык'), state='*')
async def start(message: types.Message):
    await Choose.default.set()
    await message.answer('Выбрать язык', reply_markup=markup)


@dp.message_handler(Text(equals='Occupied (now)'), state=Choose.default)
async def start(message: types.Message):
    await Choose.default.set()
    rooms = get_occupied_rooms(get_bookings())
    answer = '\n'.join(rooms) if rooms else 'All meeting rooms are free'
    await message.answer(answer, reply_markup=markup_en)


@dp.message_handler(Text(equals='Occupied (at specified time)'), state=Choose.default)
async def start(message: types.Message):
    await Choose.occupied_en.set()
    await message.answer('Enter time in HH:MM format')


@dp.message_handler(Text(equals='Free (now)'), state=Choose.default)
async def start(message: types.Message):
    await Choose.default.set()
    rooms = get_free_rooms(get_bookings())
    answer = '\n'.join(rooms) if rooms else 'All meeting rooms are occupied'
    await message.answer(answer, reply_markup=markup_en)


@dp.message_handler(Text(equals='Free (at specified time)'), state=Choose.default)
async def start(message: types.Message):
    await Choose.free_en.set()
    await message.answer('Enter time in HH:MM format')


@dp.message_handler(Text(equals='All'), state=Choose.default)
async def start(message: types.Message):
    await Choose.default.set()
    rooms = get_all_rooms()
    answer = '\n'.join(rooms) if rooms else 'Something went wrong'
    await message.answer(answer, reply_markup=markup_en)


@dp.message_handler(Text(equals='Choose language'), state=Choose.default)
async def start(message: types.Message):
    await message.answer('Choose language', reply_markup=markup)


if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
