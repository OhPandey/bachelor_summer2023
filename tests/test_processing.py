import unittest
from unittest import mock

import numpy

from lib.data.student import Student
from lib.detectors.detector import Detector
from lib.threads.processing import Processing


class TestProcess(unittest.TestCase):
    def setUp(self):
        mock_students = mock.Mock(spec=Student)
        self.process = Processing(mock_students, 30)

    def test_first(self):
        # Testing the runtime
        self.process.start()
        self.assertTrue(self.process.is_running())
        self.process.stop()
        self.assertFalse(self.process.is_running())

    def test_second(self):
        # Testing adding to a buffer
        mock_frame = mock.Mock(spec=numpy)
        for e in range(65):
            self.process.add_queue(mock_frame)

        self.assertTrue(self.process.is_main_buffer_full())

        # Testing clearing buffer
        self.process.flush()
        self.assertEqual(len(self.process.main_buffer), 0)

    def test_third(self):
        # Testing detector
        mock_frame = mock.Mock(spec=numpy)
        self.assertIsInstance(self.process.get_detection(mock_frame), Detector)
