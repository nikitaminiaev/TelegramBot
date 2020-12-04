import os
import db
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
                           parse_mode='html',
                           reply_markup=markup)
    if not db.isset_user(message.from_user.id):
        db.insert('users', {'id': message.from_user.id, 'name': message.from_user.first_name})
    await bot.send_message(message.chat.id, 'Выберите категории которые хотите отслеживать')


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")


@dp.message_handler()
async def say(message: types.Message):
    parser = Parser()
    if message.chat.type == 'private':
        if message.text == 'Нанотех':
            db.update('users', str(message.from_user.id), {'subscriptions_nano': 1})
            await method_name(message, Parser.URL_MECHATRONICS, str({'subscription': 'stop_nano', 'user_id': str(message.from_user.id)}), parser.parse_mechatronics)
        elif message.text == 'ИИ':
            db.update('users', str(message.from_user.id), {'subscriptions_ai': 1})
            await method_name(message, Parser.URL_GOOGLE_BLOG, str({'subscription': 'stop_ai', 'user_id': str(message.from_user.id)}), parser.parse_google_blog)
        else:
            await bot.send_message(message.chat.id, 'Общайтесь кнопками')

# TODO
# сделать подписку в колбеке, как и отписку, разделить  методы. Подобрать названия метода
async def method_name(message, url: str, callback_data: str, parse_method):
    await bot.send_message(message.chat.id, 'отслеживаемые страницы: ' + '\n' + url + '\n')
    item = types.InlineKeyboardButton("Прекратить отслеживаение?", callback_data=callback_data)
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(item)
    await bot.send_message(message.chat.id, 'последняя новость: ' + '\n' + parse_method() + '\n',
                           reply_markup=markup)


@dp.callback_query_handler(lambda call: True)
async def callback_inline(call):
    try:
        if call.message:
            call.data = eval(call.data)
            if call.data['subscription'] == 'stop_nano':
                db.update('users', call.data['user_id'], {'subscriptions_nano': 0})
            elif call.data['subscription'] == 'stop_ai':
                db.update('users', call.data['user_id'], {'subscriptions_ai': 0})
            await bot.edit_message_text(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        text="Отслеживание прекращено",
                                        reply_markup=None)
            #
            # await bot.answer_callback_query(callback_query_id=call.id,
            #                                 show_alert=False,
            #                                 text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!")

    except Exception as e:
        print(repr(e))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
