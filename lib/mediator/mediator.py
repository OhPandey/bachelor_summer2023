from abc import ABC, abstractmethod


class Mediator(ABC):

    @abstractmethod
    def update(self, event: str) -> None:
        pass
