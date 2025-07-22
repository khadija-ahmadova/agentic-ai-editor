import unittest
from functions.get_files_info import get_files_info

class TestGetFiles(unittest.TestCase):

    def test_get_file_info_cur_dir(self):
        result = get_files_info("calculator", ".")
        expected = """- pkg: file_size=4096 bytes, is_dir=True\n- tests.py: file_size=1330 bytes, is_dir=False\n- main.py: file_size=564 bytes, is_dir=False"""
        self.assertEqual(result, expected)

    def test_get_file_info_pkg(self):
        result = get_files_info("calculator", "pkg")
        expected = """- __pycache__: file_size=4096 bytes, is_dir=True\n- calculator.py: file_size=1737 bytes, is_dir=False\n- render.py: file_size=766 bytes, is_dir=False"""
        self.assertEqual(result, expected)

    def test_get_file_info_outside_work_dir(self):
        result = get_files_info("calculator", "/bin")
        expected = 'Error: Cannot list "/bin" as it is outside the permitted working directory'
        self.assertEqual(result, expected)

    def test_get_file_info_outside_work_dir_2(self):
        result = get_files_info("calculator", "../")
        expected = 'Error: Cannot list "../" as it is outside the permitted working directory'
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()

