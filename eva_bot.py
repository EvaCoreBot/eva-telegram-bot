import os
import logging
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import openai
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

logging.basicConfig(level=logging.INFO)

if TELEGRAM_TOKEN is None:
    raise ValueError("Missing TELEGRAM_TOKEN environment variable")
if OPENAI_API_KEY is None:
    raise ValueError("Missing OPENAI_API_KEY environment variable")

bot = Bot(token=TELEGRAM_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

openai.api_key = OPENAI_API_KEY

async def generate_response(prompt: str) -> str:
    try:
        response = await openai.ChatCompletion.acreate(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            n=1,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.exception("OpenAI API error")
        return "\u0418\u0437\u0432\u0438\u043d\u0438\u0442\u0435, \u043f\u0440\u043e\u0438\u0437\u043e\u0448\u043b\u0430 \u043e\u0448\u0438\u0431\u043a\u0430 \u043f\u0440\u0438 \u0433\u0435\u043d\u0435\u0440\u0430\u0446\u0438\u0438 \u043e\u0442\u0432\u0435\u0442\u0430."

@dp.message_handler()
async def handle_message(message: types.Message):
    user_text = message.text.strip()
    reply_text = await generate_response(user_text)
    await message.answer(reply_text)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
