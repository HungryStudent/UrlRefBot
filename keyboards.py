from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData

accept_out = CallbackData("accept_out", "out_id")
cancel_out = CallbackData("cancel_out", "out_id")

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

in_cancel = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('Отмена', callback_data="cancel"))

profile = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('Вывести деньги', callback_data="out_money_page"),
                                                InlineKeyboardButton('Назад в меню', callback_data="to_menu"))

send_type = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('Текст', callback_data="send_text"),
                                                  InlineKeyboardButton('Фото', callback_data="send_photo"))


def get_admin_out(out_id):
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton('✅Подтвердить вывод', callback_data=accept_out.new(out_id)),
        InlineKeyboardButton('❌Отказать в выводе', callback_data=cancel_out.new(out_id)))
