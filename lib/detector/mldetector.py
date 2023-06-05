from lib.debugging.debugging import Debugging
from lib.detector.detector import Detector
from lib.utils.position import Position


class HMLDetector(Detector, Debugging):
    def card(self) -> Position | None:
        pass

    def _is_card(self):
        return s