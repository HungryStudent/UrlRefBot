from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ContentTypes
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram import Bot

import keyboards as kb
from config import *
import logging
import utils
import texts
import db

logging.getLogger("vkbottle").setLevel(logging.CRITICAL)
logging.getLogger("aiogram").setLevel(logging.INFO)

stor = MemoryStorage()
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=stor)


class CardState(StatesGroup):
    enter_card = State()


async def on_startup(_):
    db.start()


@dp.message_handler(lambda m: m.from_user.id in admin_ids, commands="update")
async def update_sheet(message: Message):
    await utils.update_stat()
    await message.answer("Таблица обновлена!")


@dp.message_handler(content_types="video")
async def send_file_id(message: Message):
    print(message.video.file_id)


@dp.message_handler(commands='start')
async def start_message(message: Message):
    user = db.get_user(message.from_user.id)
    if user is None:
        await message.answer(texts.hello, reply_markup=kb.contact)
    else:
        await message.answer(texts.menu, reply_markup=kb.menu)


@dp.message_handler(content_types=ContentTypes.CONTACT)
async def add_user(message: Message):
    url = await utils.gen_url(message.from_user.id)
    db.add_user(message.from_user.id, url, message.contact.phone_number)
    msg = await message.answer("Загрузка...", reply_markup=kb.ReplyKeyboardRemove())
    await message.answer(texts.menu, reply_markup=kb.menu)
    await msg.delete()


@dp.callback_query_handler(state="*", text="to_menu")
async def to_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer(texts.menu, reply_markup=kb.menu)
    await call.message.delete()


@dp.callback_query_handler(text="ref_page")
async def get_ref_url(call: CallbackQuery):
    ref_url = "https://vk.cc/" + db.get_key(call.from_user.id)
    await call.message.answer(texts.ref.format(ref_url=ref_url), reply_markup=kb.to_menu)
    await call.message.delete()


@dp.callback_query_handler(text="profile_page")
async def my_profile(call: CallbackQuery):
    key = db.get_key(call.from_user.id)
    ref_count = await utils.get_url_stat(key)
    user_stat = await utils.get_user_stat(call.from_user.id)
    await call.message.edit_text(
        texts.profile.format(username=call.from_user.username, ref_count=ref_count, reqs=user_stat["reqs"],
                             sells=user_stat["sells"], ready_out=user_stat["ready_out"], out=user_stat["out"]),
        reply_markup=kb.profile)


@dp.callback_query_handler(text="out_money_page")
async def out_money(call: CallbackQuery):
    user_stat = await utils.get_user_stat(call.from_user.id)
    money = user_stat["ready_out"]
    if money > 0:
        await call.message.edit_text(texts.enter_card, reply_markup=kb.to_menu)
        await CardState.enter_card.set()
    else:
        ref_url = "https://vk.cc/" + db.get_key(call.from_user.id)
        await call.message.edit_text(texts.no_money.format(ref_url=ref_url), reply_markup=kb.to_menu)


@dp.message_handler(state=CardState.enter_card)
async def request_out_money(message: Message, state: FSMContext):
    card = message.text
    await state.finish()
    await message.answer(texts.request_out_money, reply_markup=kb.to_menu)
    await message.bot.send_message(helper_chat_id,
                                   texts.request_out_money_for_helper.format(username=message.from_user.username,
                                                                             card=card))
    db.append_out(message.from_user.id, 12)


@dp.callback_query_handler(text="faq_page")
async def faq(call: CallbackQuery):
    await call.message.edit_text(texts.faq, reply_markup=kb.to_menu)


@dp.callback_query_handler(text="support_page")
async def support(call: CallbackQuery):
    await call.message.edit_text(texts.support, reply_markup=kb.support)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
