import unittest

from tests.test_capture import TestCapture
from tests.test_processing import TestProcessing
from tests.test_student import TestStudent
from tests.test_students import TestStudents

if __name__ == '__main__':
    suite = unittest.TestSuite()

    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestStudent))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestStudents))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestProcessing))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCapture))

    unittest.TextTestRunner().run(suite)
