import unittest
from lib.tests.test_student import TestStudent
from lib.tests.test_students import TestStudents

if __name__ == '__main__':
    suite = unittest.TestSuite()

    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestStudent))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestStudents))

    unittest.TextTestRunner().run(suite)
