from configparser import ConfigParser
from pathlib import Path
from typing import Literal


class Config:
    """
    work with config.ini
    """
    path = Path("app_data", "config.ini")

    def get_value(self,
                  section: Literal["bot", "spam", "accounts", "reply", "spam_ban"],
                  key: Literal["token", "report_time", "alert", "add_admin_to_contacts",
                               "check_pause", "cutoff", "timeout",
                               "connection_retries", "server", "connect_group",
                               "speed_x", "dating", "group_chats_limit",
                               "mask_bot", "mask_site", "replace_after"]
                  ) -> str:
        """
        Get a value from a config.ini file
        """
        try:
            path = Path("app_data", "config.ini")
            config = ConfigParser()
            config.read(path)
            return config[section][key].strip()
        except KeyError as ex:
            raise KeyError(f"Отсутствует ключ {ex} в config.ini")

    def get_list_values(
            self,
            section: Literal["bot", "spam", "chats", "accounts"],
            key: Literal["admin_ids", "message_pause", "little_join_pause",
                         "big_join_pause", "little_leave_pause",
                         "big_leave_pause", "admin_usernames", "check_connection",
                         "terminate_sessions"]
    ) -> list[str]:
        """
        Get a list values from a config.ini file. ',' - is separator
        """
        try:
            path = Path("app_data", "config.ini")
            config = ConfigParser()
            config.read(path)
            return [i.strip() for i in config[section][key].split(",")]
        except KeyError as ex:
            raise KeyError(f"Отсутствует ключ {ex} в config.ini")
