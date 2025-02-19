import logging
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import asyncio

# Bot va Dispatcher sozlamalari
API_TOKEN = "8048673552:AAEP09_Nx3zRoEApaK9FHs2HdXovSEVpSOk"
ACCESS_KEY = "98ce7a4dd8ffd8f84e634290aad04170"
API_URL = "https://api.exchangerate.host/convert"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Klaviatura tugmalari
def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="/start"), KeyboardButton(text="/clear"), KeyboardButton(text="/history")]],
        resize_keyboard=True
    )

def get_language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data='lang_uz')],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data='lang_en')],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data='lang_ru')],
        [InlineKeyboardButton(text="🇰🇷 한국어", callback_data='lang_ko')]
    ])

currencies = ["USD", "EUR", "RUB", "UZS", "GBP", "CNY", "JPY", "KZT", "CHF", "CAD", "AUD", "TRY", "INR", "SGD", "HKD", "BRL", "MXN", "NOK"]

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

# /start komandasi
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Tilni tanlang / Choose a language / Выберите язык / 언어를 선택하세요:",
        reply_markup=get_language_keyboard()
    )

# Tilni tanlash
@dp.callback_query(lambda c: c.data.startswith('lang_'))
async def language_selection(callback: types.CallbackQuery):
    lang_code = callback.data.split('_')[1]
    user_languages[callback.from_user.id] = lang_code
    messages = {
        'uz': "Valyutani tanlang:",
        'en': "Choose your currency:",
        'ru': "Выберите валюту:",
        'ko': "통화를 선택하세요:"
    }
    await callback.message.answer(messages[lang_code], reply_markup=get_currency_keyboard())
    await callback.answer()

# Valyuta tanlash
@dp.callback_query(lambda c: c.data.startswith('currency_'))
async def currency_selection(callback: types.CallbackQuery):
    currency = callback.data.split('_')[1]
    user_currencies[callback.from_user.id] = currency
    lang = user_languages.get(callback.from_user.id, 'uz')
    messages = {
        'uz': f"Siz {currency} ni tanladingiz. Miqdorni kiriting (masalan: 100 {currency} to UZS)",
        'en': f"You have selected {currency}. Enter the amount (e.g., 100 {currency} to UZS)",
        'ru': f"Вы выбрали {currency}. Введите сумму (например: 100 {currency} to UZS)",
        'ko': f"{currency}를 선택하셨습니다. 금액을 입력하세요 (예: 100 {currency} to UZS)"
    }
    await callback.message.answer(messages[lang])
    await callback.answer()

# Valyuta konvertatsiyasi
@dp.message()
async def convert(message: types.Message):
    lang = user_languages.get(message.from_user.id, 'uz')
    try:
        text = message.text.strip().split()
        if len(text) < 4 or text[2].lower() != 'to':
            raise ValueError("Invalid format")

        amount = float(text[0])
        from_currency = text[1].upper()
        to_currency = text[3].upper()

        async with aiohttp.ClientSession() as session:
            async with session.get(
                API_URL,
                params={"from": from_currency, "to": to_currency, "amount": amount, "access_key": ACCESS_KEY},
            ) as response:
                data = await response.json()
                if data.get("success"):
                    result = data.get("result")
                    user_history.setdefault(message.from_user.id, []).append(f"{amount} {from_currency} -> {result:.2f} {to_currency}")
                    messages = {
                        'uz': f"{amount} {from_currency} ≈ {result:.2f} {to_currency}",
                        'en': f"{amount} {from_currency} ≈ {result:.2f} {to_currency}",
                        'ru': f"{amount} {from_currency} ≈ {result:.2f} {to_currency}",
                        'ko': f"{amount} {from_currency} ≈ {result:.2f} {to_currency}"
                    }
                    await message.answer(messages[lang])
                else:
                    await message.answer("Xatolik: Valyuta kurslarini olishning imkoni bo‘lmadi.")
    except Exception as e:
        await message.answer("Xato: Iltimos, to‘g‘ri formatda so‘rov yuboring.")
        logging.error(f"Xatolik: {e}")

# /clear komandasi
@dp.message(Command("clear"))
async def clear(message: types.Message):
    user_languages.pop(message.from_user.id, None)
    user_currencies.pop(message.from_user.id, None)
    user_history.pop(message.from_user.id, None)
    await message.answer("Ma'lumotlaringiz tozalandi. /start buyrug'ini bosing.", reply_markup=get_main_keyboard())

# /history komandasi
@dp.message(Command("history"))
async def history(message: types.Message):
    history = user_history.get(message.from_user.id, [])
    await message.answer("\n".join(history) if history else "Siz hali hech qanday konvertatsiya qilmadingiz.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
