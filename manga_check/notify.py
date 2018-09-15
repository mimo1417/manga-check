"""
notify to telegram if there is new story
"""
import telegram
from manga_check import config


def notify(message):
    """
    Send to telegram

    Args:
        message (str): Description
    """
    bot = telegram.Bot(token=config.TELEGRAM_TOKEN)
    try:
        bot.send_message(chat_id=int(config.TELEGRAM_CHAT_ID), text=message)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
