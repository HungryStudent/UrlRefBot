import re

import db
from config import site_url, vk_token
from vkbottle import API
from enum import Enum
import gspread


class SheetTypes(Enum):
    Leads = 0
    Users = 2


api = API(token=vk_token)

CREDENTIALS_FILE = 'creds.json'

gc = gspread.service_account(filename=CREDENTIALS_FILE)
sh = gc.open("Выгрузка amoCRM (2)")

leads_ws = sh.get_worksheet(SheetTypes.Leads.value)
users_ws = sh.get_worksheet(SheetTypes.Users.value)


async def gen_url(user_id):
    res = await api.utils.get_short_link(url=site_url.format(tg_id=user_id), private=False)
    return res.key


async def get_url_stat(key):
    res = await api.utils.get_link_stats(key=key, interval="forever")
    if not res.stats:
        return 0
    return res.stats[0].views


async def get_user_stat(user_id):
    amount_re = re.compile(r'utm_campaign=' + str(user_id))
    user_stat = {}
    refs = leads_ws.findall(amount_re)
    user_stat["reqs"] = len(refs)
    sells_count = 0
    balance = 0
    for ref in refs:
        ref_data = leads_ws.row_values(ref.row)
        try:
            if ref_data[3] == "Успех":
                sells_count += 1
                balance += int(ref_data[1])
        except IndexError:
            pass
        
    balance *= 0.2
    out = db.get_outs(user_id)
    ready_out = balance - db.get_ready_outs(user_id)
    if ready_out < 0:
        ready_out = 0
    user_stat["sells"] = sells_count
    user_stat["ready_out"] = ready_out
    user_stat["out"] = out
    return user_stat


async def get_reqs(user_id):
    amount_re = re.compile(r'utm_campaign=' + str(user_id))
    reqs = leads_ws.findall(amount_re)
    return len(reqs)


async def get_sells(user_id):
    amount_re = re.compile(r'utm_campaign=' + str(user_id))
    # amount_re = re.compile(r'utm_campaign=')
    sells = leads_ws.findall(amount_re)
    sells_count = 0
    for sell in sells:
        status = leads_ws.cell(sell.row, 8)
        if status.value == "Успех":
            sells_count += 1
    return sells_count


async def update_stat():
    users_ws.resize(rows=1)
    users = db.get_users()
    for user in users:
        user_stat = await get_user_stat(user[0])
        url = "https://vk.cc/" + user[1]
        ref_count = await get_url_stat(user[1])
        users_ws.append_row([user[0], user[2], url, ref_count, user_stat["reqs"], user_stat["sells"]])
