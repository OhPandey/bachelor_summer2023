import unittest
from lib.tests.studenttest import TestStudent
if __name__ == '__main__':
    suite = unittest.TestSuite()

    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestStudent))

    unittest.TextTestRunner().run(suite)
