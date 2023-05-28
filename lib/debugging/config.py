import configparser

config = configparser.ConfigParser()
config.read('config.ini')


def get_config(section: str, option: str) -> str:
    return config.get(section, option)


def change_config(section: str, option: str, value: str) -> None:
    config.set(section, option, value)


def write_config():
    with open('config.ini', 'w') as config_file:
        config.write(config_file)
