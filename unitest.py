import unittest
from datetime import datetime

class TestDateParsing(unittest.TestCase):
    def test_date_parsing(self):
        test_date_str = '2024-05-27 10:33:25'
        expected_date = datetime(2024, 5, 27, 10, 33, 25)
        parsed_date = datetime.strptime(test_date_str, "%Y-%m-%d %H:%M:%S")
        self.assertEqual(parsed_date, expected_date)

if __name__ == '__main__':
    unittest.main()
