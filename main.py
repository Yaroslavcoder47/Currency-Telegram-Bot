import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types
from config import (token, agent, url_investing_usd, url_investing_eu, url_investing_gbp)

bot = telebot.TeleBot(token)


class CurrencyUsd:
    DOLLAR_RUB = url_investing_usd
    headers = {'User-Agent': agent}

    def get_currency(self):
        full_page = requests.get(self.DOLLAR_RUB, headers=self.headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        convert = soup.findAll("span", {"class": "text-2xl"})
        return convert[0].text


class CurrencyGBP:
    POUND_RUB = url_investing_gbp
    headers = {'User-Agent': agent}

    def get_currency(self):
        full_page = requests.get(self.POUND_RUB, headers=self.headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        convert = soup.findAll("span", {"class": "text-2xl"})
        return convert[0].text


class CurrencyEu:
    EURO_RUB = url_investing_eu
    headers = {'User-Agent': agent}

    def get_currency(self):
        full_page = requests.get(self.EURO_RUB, headers=self.headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        convert = soup.findAll("span", {"class": "text-2xl"})
        return convert[0].text


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    rate_button = types.KeyboardButton('Currency rate💰')
    markup.add(rate_button)
    bot.send_message(message.chat.id, f"Hello <b>{message.from_user.first_name}</b>."
                                      f"This is a CurrencyBot which can help you to find current exchange rates!",
                     parse_mode="html", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_rate(message):
    if message.chat.type == 'private':
        if message.text == 'Currency rate💰':
            markup = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton("USD 💵", callback_data='usd')
            item2 = types.InlineKeyboardButton("EU 💶", callback_data='euro')
            item3 = types.InlineKeyboardButton("GBP 💷", callback_data='pound')

            markup.add(item1, item2, item3)

            bot.send_message(message.chat.id, f'💱<b>SELECT CURRENCY</b>💱', parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == 'usd':
            mess = CurrencyUsd().get_currency()
            bot.send_message(call.message.chat.id, f"1$ = {str(mess)} BYN", parse_mode='html')
        elif call.data == 'euro':
            mess = CurrencyEu().get_currency()
            bot.send_message(call.message.chat.id, f"1€ = {str(mess)} BYN", parse_mode='html')
        elif call.data == 'pound':
            mess = CurrencyGBP().get_currency()
            bot.send_message(call.message.chat.id, f"1£ = {str(mess)} BYN", parse_mode='html')


bot.polling(none_stop=True)
