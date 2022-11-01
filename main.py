from pathlib import Path

from telebot.types import Message
from loguru import logger

from bot import bot, admins
from logger import set_logger
from combinator import combinate_text


def main() -> None:
    set_logger()
    try:
        bot.infinity_polling()
        logger.info("Script is finished")
    except KeyError as ex:
        logger.warning(ex)
    except Exception as ex:
        logger.warning(f"{type(ex)}: {ex}")


@bot.message_handler(commands=["start"])
def send_start_message(message: Message) -> None:
    if message.chat.id in admins:
        try:
            bot.send_message(message.chat.id,
                             'Send me blocks of text with separor "~"')
        except Exception as ex:
            logger.warning(f"Bot: {type(ex)} {ex}")


@bot.message_handler()
def send_combinated_text(message: Message) -> None:
    if message.chat.id in admins:
        try:
            bot.send_message(message.chat.id,'In progress')
            combinate_text(message.text)
            _send_document(message)
        except Exception as ex:
            logger.warning(f"{type(ex)} {ex}")


def _send_document(message: Message) -> None:
    path = Path("generated.txt")
    if path.is_file():
        file = open(path, "rb")
        bot.send_document(message.chat.id, document=file)
        file.close()
    else:
        bot.send_message(message.chat.id, "File not found")


if __name__ == "__main__":
    main()
