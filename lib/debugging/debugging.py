from abc import ABC

from lib.debugging.config import *
from lib.debugging.log import write_log
from lib.debugging.subdirectory import Subdirectory


class Debugging(ABC):
    debugging: bool = False
    option: Subdirectory

    def __init__(self, option: Subdirectory):
        value = config.get('debugging', option.value)
        if value == "True":
            self.debugging = True
        self.option = option

    def set_debugging(self, value: bool) -> None:
        self.debugging = value
        change_config('debugging', self.option.value, str(value))
        write_config()

    def is_debugging(self) -> bool:
        return self.debugging

    def log(self, content):
        if self.is_debugging():
            write_log(content, self.option)
