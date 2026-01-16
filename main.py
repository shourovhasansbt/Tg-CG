import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from openai import OpenAI

# লগিং সেটআপ (ডিবাগিং এর জন্য)
logging.basicConfig(level=logging.INFO)

# --- কনফিগারেশন ---
# গিটহাবে কোড আপলোড করার সময় এখানে সরাসরি Key লিখবেন না।
# Koyeb এর Settings > Environment Variables এ গিয়ে এই নামগুলো দিয়ে Key পেস্ট করবেন।
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# চেক করা হচ্ছে Key গুলো ঠিকমতো লোড হয়েছে কিনা
if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    print("Error: TELEGRAM_TOKEN or OPENAI_API_KEY not found!")
    exit(1)

# OpenAI ক্লায়েন্ট সেটআপ
client = OpenAI(api_key=OPENAI_API_KEY)

# টেলিগ্রাম বট এবং ডিসপ্যাচার সেটআপ
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# --- হ্যান্ডলার ফাংশন ---

# /start কমান্ড দিলে কি হবে
@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.answer(f"হ্যালো {message.from_user.full_name}! আমি আপনার AI অ্যাসিস্ট্যান্ট। আমাকে কিছু জিজ্ঞাসা করুন।")

# যেকোনো টেক্সট মেসেজ আসলে কি হবে
@dp.message()
async def chat_gpt_response(message: types.Message):
    user_text = message.text
    
    # ইউজারকে জানানো যে টাইপ করা হচ্ছে (User Experience ভালো করার জন্য)
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    try:
        # OpenAI তে রিকোয়েস্ট পাঠানো
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # অথবা "gpt-3.5-turbo" ব্যবহার করতে পারেন খরচ কমাতে
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_text}
            ]
        )
        
        gpt_reply = response.choices[0].message.content
        
        # টেলিগ্রামে রিপ্লাই পাঠানো
        await message.answer(gpt_reply)

    except Exception as e:
        logging.error(f"Error: {e}")
        await message.answer("দুঃখিত, কোনো একটি সমস্যা হয়েছে। কিছুক্ষণ পর আবার চেষ্টা করুন।")

# --- মেইন ফাংশন ---
async def main():
    print("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
