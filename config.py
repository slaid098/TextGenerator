from configparser import ConfigParser
from pathlib import Path
from typing import Literal


class Config:
    """
    work with config.ini
    """
    path = Path("config.ini")
    config = ConfigParser()
    config.read(path)
    
    def get_value(self,
                  section: Literal["bot"],
                  key: Literal["token"],
                  cache: bool = True) -> str:
        """
        Get a value from a .ini file
        """
        try:
            if not cache:
                path = Path("app_data", "config.ini")
                config = ConfigParser()
                config.read(path)
                return config[section][key]
            return (self.config[section][key]).strip()
        except KeyError as ex:
            raise KeyError(f"Отсутствует ключ {ex}")

    def get_split_values(self,
                         section: Literal["admins", ],
                         key: Literal["admins", "token"],
                         separator: str = ",",
                         cache: bool = True) -> list[str]:
        """
        Get a list of values from a .ini file using a separator
        """
        try:
            if not cache:
                path = Path("app_data", "config.ini")
                config = ConfigParser()
                config.read(path)
                list_values = (self.config[section][key]).split(separator)
                return (i.strip() for i in list_values)
            list_values = (self.config[section][key]).split(separator) 
            return (i.strip() for i in list_values)
        except KeyError as ex:
            raise KeyError(f"Key not found {ex}")