import logging
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
import asyncio

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

# Start komandasi
async def start(message: types.Message):
    await message.answer(
        "Assalomu alaikum! Men valyuta konvertatsiya botiman, namunaga qarab so'rov jo'nating\n"
        "Namuna: 100 USD to UZS"
    )

# Valyuta konvertatsiyasi
async def convert(message: types.Message):
    try:
        text = message.text.strip().split()
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
                    await message.answer(f"{amount} {from_currency} ≈ {result:.2f} {to_currency}")
                else:
                    await message.answer("Xato: Valyuta kurslarini olishning imkoni bo'lmadi.")
    except Exception as e:
        await message.answer("Xato: Iltimos, to'g'ri formatda so'rov yuboring.")
        logging.error(f"Xatolik: {e}")

# Handlerlarni ro‘yxatga olish
dp.message.register(start, Command("start"))
dp.message.register(convert)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
