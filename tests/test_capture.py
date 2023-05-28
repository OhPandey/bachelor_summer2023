import unittest
from unittest import mock

from cv2 import VideoCapture

from lib.threads.capturing import Capturing
from lib.threads.processing import Processing


class TestCapture(unittest.TestCase):

    def setUp(self):
        self.capturing = Capturing(1)

    def test_first(self):
        # Testing the runtime
        self.capturing.start()
        self.assertTrue(self.capturing.is_running())
        self.capturing.stop()
        self.assertFalse(self.capturing.is_running())

    def test_second(self):
        # Testing the capture
        self.assertIsInstance(self.capturing._capture, VideoCapture)
        self.assertTrue(self.capturing._capture.isOpened())

    def test_third(self):
        # Testing the processing
        self.capturing.add_processing(mock.Mock(spec=Processing))
        self.assertTrue(self.capturing._has_processing())
        self.assertIsInstance(self.capturing._processing, Processing)
