import configparser
import os

from lib.debugging.log import write_log
from lib.debugging.subdirectory import Subdirectory

script_path = os.path.abspath(__file__)
config_file_path = os.path.join(script_path, '../../../config.ini')

config = configparser.ConfigParser()
config.read(config_file_path)


def get_config(section: str, option: str) -> str:
    if os.path.exists(config_file_path):
        write_log(f"get_config(): Configuration file {config_file_path} could not be found", Subdirectory.CONFIG)
    else:
        try:
            return config.get(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError) as err:
            write_log(f"get_config(): {err}", Subdirectory.CONFIG)


def change_config(section: str, option: str, value: str) -> None:
    if os.path.exists(config_file_path):
        write_log(f"change_config(): Configuration file {config_file_path} could not be found", Subdirectory.CONFIG)
    else:
        try:
            config.set(section, option, value)
        except (configparser.NoSectionError, configparser.NoOptionError) as err:
            write_log(f"change_config(): {err}", Subdirectory.CONFIG)


def write_config():
    if os.path.exists(config_file_path):
        write_log(f"write_config(): Configuration file {config_file_path} could not be found", Subdirectory.CONFIG)
    else:
        with open('config.ini', 'w') as config_file:
            config.write(config_file)
