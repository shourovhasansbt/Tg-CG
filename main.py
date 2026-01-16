import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import google.generativeai as genai

# লগিং চালু করা
logging.basicConfig(level=logging.INFO)

# --- কনফিগারেশন ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# চেক করা হচ্ছে Key আছে কিনা
if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    print("Error: Keys not found!")
    exit(1)

# Gemini সেটআপ
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# টেলিগ্রাম বট সেটআপ
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# /start কমান্ড হ্যান্ডলার
@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.answer(f"হ্যালো! আমি এখন Google Gemini দিয়ে চলছি। আমাকে প্রশ্ন করুন।")

# যেকোনো মেসেজ হ্যান্ডলার
@dp.message()
async def gemini_response(message: types.Message):
    # টাইপিং দেখানো
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    try:
        # জেমিনিকে প্রশ্ন পাঠানো
        response = model.generate_content(message.text)
        
        # উত্তর পাঠানো
        if response.text:
            await message.answer(response.text)
        else:
            await message.answer("দুঃখিত, কোনো উত্তর পাওয়া যায়নি।")

    except Exception as e:
        logging.error(f"Error: {e}")
        await message.answer("একটু সমস্যা হয়েছে, আবার চেষ্টা করুন।")

# মেইন ফাংশন
async def main():
    print("Bot is running with Gemini...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
