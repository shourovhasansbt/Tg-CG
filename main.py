import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import google.generativeai as genai

# লগিং
logging.basicConfig(level=logging.INFO)

# --- কনফিগারেশন (সরাসরি বসানো হলো) ---

# তোমার টেলিগ্রাম টোকেন
TELEGRAM_TOKEN = "8535188730:AAFxl7kqLD2Bxben8pgAB8ddIauJHHtqddk"

# তোমার জেমিনি কি (Key)
GEMINI_API_KEY = "AIzaSyAx-Bl39LfGi5TvHOUdlftqemPKilqYKJw"

# Gemini সেটআপ
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Gemini Config Error: {e}")

# টেলিগ্রাম বট সেটআপ
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.answer(f"হ্যালো! আমি রেডি। আমাকে প্রশ্ন করুন।")

@dp.message()
async def gemini_response(message: types.Message):
    # টাইপিং স্ট্যাটাস
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    try:
        # Gemini কে প্রশ্ন করা
        response = model.generate_content(message.text)
        
        # উত্তর পাঠানো
        if response.text:
            await message.answer(response.text)
        else:
            await message.answer("কোনো উত্তর পাওয়া যায়নি।")

    except Exception as e:
        # এরর হলে মেসেজ দিবে
        await message.answer(f"Error: {str(e)}")

async def main():
    print("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
