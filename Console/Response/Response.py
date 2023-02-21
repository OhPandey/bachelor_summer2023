from datetime import datetime

from Console.Response.TextColor import TextColor


class Response:

    msg = ""

    def __consoleAI(self, textcolor):
        if textcolor is None:
            print(f"[{datetime.now().time()}] {self.msg}")
            return

        print(f"{textcolor}[{datetime.now().time()}] {self.msg} {TextColor.END}")

    # default messages

    def defaultWarning(self, msg: str = ""):
        self.msg = msg
        self.__consoleAI(TextColor.WARNING)

    def defaultError(self, msg: str = ""):
        self.msg = msg
        self.__consoleAI(TextColor.ERROR)

    def defaultGood(self, msg: str = ""):
        self.msg = msg
        self.__consoleAI(TextColor.OK)

    def defaultPrint(self, msg: str = ""):
        self.msg = msg
        self.__consoleAI(TextColor.DEFAULT)

    # pre-defined messages

    def missingArgumentWarning(self):
        self.msg = f"Missing argument(s), check syntax in help"
        self.__consoleAI(TextColor.WARNING)

    def internalError(self, msg: str = ""):
        self.msg = f"Internal Error: {msg}"
        self.__consoleAI(TextColor.ERROR)
