import unittest
import ramorm

class FieldsTest(unittest.TestCase):

    def test_IntegerField(self):
        self.assertTrue(ramorm.IntegerField(default=1))


if __name__ == '__main__':
    unittest.main()