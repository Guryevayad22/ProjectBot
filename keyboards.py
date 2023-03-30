from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

btn_english = KeyboardButton('English')
btn_russian = KeyboardButton('Русский')

markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(btn_russian, btn_english)

btn_occupied_rus = KeyboardButton('Занятые')
btn_free_rus = KeyboardButton('Свободные')
btn_all_rus = KeyboardButton('Все')

markup_rus = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup_rus.row(btn_occupied_rus, btn_free_rus, btn_all_rus)

btn_occupied_en = KeyboardButton('Occupied')
btn_free_en = KeyboardButton('Free')
btn_all_en = KeyboardButton('All')

markup_en = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup_en.row(btn_occupied_en, btn_free_en, btn_all_en)
