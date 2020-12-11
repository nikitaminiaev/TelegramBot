from aiogram import Bot, Dispatcher, executor, types
import main


@main.dp.message_handler()
async def check_news(message, url: str, subscription: str, parse_method):
    # news = parse_method()
    # await main.insert_news(message, news, url, subscription)
    await main.bot.send_message(message.chat.id, 'проверка')
    # main.dp.пуе



if __name__ == '__main__':
    # executor.start_polling(main.dp, skip_updates=True)
    check_news()