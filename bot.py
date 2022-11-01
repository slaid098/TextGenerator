from asyncio.log import logger
from telebot import TeleBot

from config import Config


def get_bot() -> TeleBot:
    return TeleBot(token=_get_token(), parse_mode='html')


def _get_token() -> str:
    return Config().get_value("bot", "token")


def get_admins() -> list[str]:
    list_str_ids = Config().get_split_values("admins", "admins")
    return [int(i) for i in list_str_ids]


def send_progress(bot: TeleBot, chat_ids: list[int], progress: int,
                  number_combinations: int) -> None:
    for admin in chat_ids:
        try:
            bot.send_message(
                admin, f"Combinated: {progress} from {number_combinations}")
        except Exception as ex:
            logger.warning(f'{type(ex)} {ex}')


bot = get_bot()
admins = get_admins()
