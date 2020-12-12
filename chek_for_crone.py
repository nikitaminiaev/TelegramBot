from aiogram import Bot, Dispatcher, executor, types
import main
import db
from parser import Parser


def send_message(message, url: str, subscription: str, parse_method):
    user = db.get_user()
    chat_id = user['chat_id']

    # news = parse_method()
    # await main.insert_news(message, news, url, subscription)
    await main.bot.send_message(chat_id, message)
    # main.dp.


def check_news(type_subscription: int):
    parser = Parser()
    if (type_subscription == db.NANO):
        return update_and_get_actual_news(parser.parse_mechatronics, db.NANO)
    elif (type_subscription == db.AI):
        return update_and_get_actual_news(parser.parse_google_blog, db.AI)


def update_and_get_actual_news(parse_method, type: int):
    actual_news = parse_method()
    if (not db.is_news_unique(actual_news)):
        db.update_news(type, actual_news)
        return actual_news


if __name__ == '__main__':
    # executor.start_polling(main.dp, skip_updates=True)
    send_message()
