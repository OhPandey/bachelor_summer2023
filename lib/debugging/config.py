import configparser
import os

# Absolute pathing
script_path = os.path.abspath(__file__)
config_file_path = os.path.join(script_path, '../../../config.ini')

config = configparser.ConfigParser()
config.read(config_file_path)


def get_config(section: str, option: str) -> str:
    return config.get(section, option)


def change_config(section: str, option: str, value: str) -> None:
    config.set(section, option, value)


def write_config():
    with open('config.ini', 'w') as config_file:
        config.write(config_file)
