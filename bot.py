import os
import aiohttp
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    a = load_dotenv(dotenv_path)
token = os.getenv('TOKEN')
bot = Bot(token=token)
dp = Dispatcher(bot)
mapping = {
       'Вероника': 'Ути!!!',
       'Никита': 'Котя!!!',
       'Санек': 'харошь',
       'Александр': 'харошь',
       'Апрес': 'го в шахматы, я тебя дерну',
       }


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nКак тебя зовут?")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")


@dp.message_handler()
async def say(message: types.Message):
    if message.text in mapping:
        await message.answer(mapping[message.text])
    await bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
