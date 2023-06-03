from lib.interfaces.mediator.responsemediator import ResponseMediator


class Component:
    def __init__(self, mediator: ResponseMediator = None) -> None:
        self._mediator = mediator

    @property
    def mediator(self) -> ResponseMediator:
        return self._mediator

    @mediator.setter
    def mediator(self, mediator: ResponseMediator) -> None:
        self._mediator = mediator
