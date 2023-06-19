from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

btn_english = KeyboardButton('English')
btn_russian = KeyboardButton('Русский')

markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(btn_russian, btn_english)

btn_spec_time_occupied_rus = KeyboardButton('Занятые (в указанное время)')
btn_occupied_rus = KeyboardButton('Занятые (сейчас)')
btn_spec_time_free_rus = KeyboardButton('Свободные (в указанное время)')
btn_free_rus = KeyboardButton('Свободные (сейчас)')
btn_all_rus = KeyboardButton('Все')
btn_menu_rus = KeyboardButton('Выбрать язык')

markup_rus = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup_rus.row(btn_occupied_rus, btn_spec_time_occupied_rus)
markup_rus.row(btn_free_rus, btn_spec_time_free_rus)
markup_rus.row(btn_all_rus, btn_menu_rus)

btn_spec_time_occupied_en = KeyboardButton('Occupied (at specified time)')
btn_occupied_en = KeyboardButton('Occupied (now)')
btn_spec_time_free_en = KeyboardButton('Free (at specified time)')
btn_free_en = KeyboardButton('Free (now)')
btn_all_en = KeyboardButton('All')
btn_menu_en = KeyboardButton('Choose language')

markup_en = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup_en.row(btn_occupied_en, btn_spec_time_occupied_en)
markup_en.row(btn_free_en, btn_spec_time_free_en)
markup_en.row(btn_all_en, btn_menu_en)
