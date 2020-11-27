import os
import aiohttp
from parser import Parser
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    a = load_dotenv(dotenv_path)
token = os.getenv('TOKEN')
bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Нанотех')
    item2 = types.KeyboardButton('ИИ')
    markup.add(item1, item2)

    await bot.send_message(message.chat.id,
                           "Добро пожаловать, {0.first_name}!\nЯ - <b>{1}</b>, бот-парсер новостных сайтов по темам.".format(
                               message.from_user,
                               bot.get('first_name')),
                           parse_mode='html', reply_markup=markup)
    await bot.send_message(message.chat.id, 'Выберите категории которые хотите отслеживать')


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")


@dp.message_handler()
async def say(message: types.Message):
    parser = Parser()
    if message.chat.type == 'private':
        if message.text == 'Нанотех':
            await bot.send_message(message.chat.id, 'отслеживаемые страницы: ' + '\n' + Parser.URL_MECHATRONICS + '\n')
            await bot.send_message(message.chat.id, 'последняя новость: ' + '\n' + parser.parse_mechatronics() + '\n')
            # await bot.send_message(message.chat.id, str(random.randint(0, 100)))
            item = types.InlineKeyboardButton("Прекратить отслеживаение", callback_data='stop')
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(item)
        elif message.text == 'ИИ':
            await bot.send_message(message.chat.id, 'отслеживаемые страницы: ' + '\n' + Parser.URL_GOOGLE_BLOG + '\n')
            await bot.send_message(message.chat.id, 'последняя новость: ' + '\n' + parser.parse_google_blog() + '\n')
            markup = types.InlineKeyboardMarkup(row_width=1)
            item = types.InlineKeyboardButton("Прекратить отслеживаение", callback_data='stop')
            # item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')
            markup.add(item)
            # await bot.send_message(message.chat.id, 'Отлично, сам как?', reply_markup=markup)
        else:
            await bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')


@dp.callback_query_handler(lambda call: True)
async def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                await bot.send_message(call.message.chat.id, 'Вот и отличненько')
            elif call.data == 'bad':
                await bot.send_message(call.message.chat.id, 'Бывает')

            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text="",
                                        reply_markup=None)

            await bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                            text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!")

    except Exception as e:
        print(repr(e))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
