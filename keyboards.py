from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData

contact = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("Отправить номер телефона", request_contact=True))

menu = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton('Получить реферальную ссылку', callback_data="ref_page"),
    InlineKeyboardButton('Мой профиль', callback_data="profile_page"),
    InlineKeyboardButton('FAQ', callback_data="faq_page"),
    InlineKeyboardButton('Поддержка', callback_data="support_page"))

support = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('FAQ', callback_data="faq_page"),
                                                InlineKeyboardButton('Назад в меню', callback_data="to_menu"))

to_menu = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('Назад в меню', callback_data="to_menu"))

profile = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('Вывести деньги', callback_data="out_money_page"),
                                                InlineKeyboardButton('Назад в меню', callback_data="to_menu"))
