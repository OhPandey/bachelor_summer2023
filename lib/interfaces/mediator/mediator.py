from abc import ABC, abstractmethod


class Mediator(ABC):

    @abstractmethod
    def set_response(self, text: str) -> None:
        pass
