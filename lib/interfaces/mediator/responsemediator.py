from abc import ABC


class ResponseMediator(ABC):
    _response = None

    @property
    def response(self) -> str | None:
        return self._response

    @response.setter
    def response(self, text: str | None) -> None:
        self._response = text
