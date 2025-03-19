import logging
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import asyncio
import os


API_TOKEN = '8048673552:AAEP09_Nx3zRoEApaK9FHs2HdXovSEVpSOk'
ACCESS_KEY = '98ce7a4dd8ffd8f84e634290aad04170'
API_URL = "https://api.exchangerate.host/convert"

# Botni sozlash
logging.basicConfig(level=logging.INFO)
bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Pastki tugmachalar (doimiy tugmalar)
def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/start"), KeyboardButton(text="/clear"), KeyboardButton(text="/history")]
        ],
        resize_keyboard=True
    )
    return keyboard

# Til tanlash tugmalari
def get_language_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="\ud83c\uddfa\ud83c\uddff O'zbek", callback_data='lang_uz')],
        [InlineKeyboardButton(text="\ud83c\uddec\ud83c\udde7 English", callback_data='lang_en')],
        [InlineKeyboardButton(text="\ud83c\uddf7\ud83c\uddfa Русский", callback_data='lang_ru')],
        [InlineKeyboardButton(text="\ud83c\uddf0\ud83c\uddf7 한국어", callback_data='lang_ko')]
    ])
    return keyboard

# Valyutalar ro'yxati
currencies = ["USD", "EUR", "RUB", "UZS", "KRW", "GBP", "CNY", "JPY", "KZT", "CHF", "CAD", "AUD", "TRY", "INR", "SGD", "HKD", "BRL", "MXN"]


def get_currency_keyboard():
    keyboard = InlineKeyboardBuilder()
    for currency in currencies:
        keyboard.button(text=currency, callback_data=f'currency_{currency}')
    keyboard.adjust(3)
    return keyboard.as_markup()

# Foydalanuvchi ma'lumotlari
user_languages = {}
user_currencies = {}
user_history = {}

# Start komandasi
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Tilni tanlang / Choose a language / Выберите язык / 언어를 선택하세요:",
        reply_markup=get_language_keyboard()
    )

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
