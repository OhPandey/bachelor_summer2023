import configparser
import os

from lib.debugging.log import write_log
from lib.debugging.subdirectory import Subdirectory

script_path = os.path.abspath(__file__)
config_file_path = os.path.join(script_path, '../../../config.ini')

config = configparser.ConfigParser()
config.read(config_file_path)


def get_config(section: str, option: str) -> str:
    try:
        return config.get(section, option)
    except (configparser.NoSectionError, configparser.NoOptionError) as err:
        write_log(f"get_config(): {err}", Subdirectory.CONFIG)


def change_config(section: str, option: str, value: str) -> None:
    try:
        config.set(section, option, value)
    except (configparser.NoSectionError, configparser.NoOptionError) as err:
        write_log(f"change_config(): {err}", Subdirectory.CONFIG)


def write_config():
    with open('config.ini', 'w') as config_file:
        config.write(config_file)
