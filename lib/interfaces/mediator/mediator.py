from abc import ABC, abstractmethod


class Mediator(ABC):

    @abstractmethod
    def update(self, event: int, frame=None) -> None:
        pass
