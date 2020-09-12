import re
import unittest

from selenium_auth import YandexAuth


class YandexAuthTester(unittest.TestCase):
    login = ''
    correct_password = ''
    incorrect_password = ''

    def validate_login(self):
        # проверка на отсутствие недопустимых символов в логине:
        self.assertTrue(re.match(r'[a-zA-Z-_]?[@]', YandexAuthTester.login))

    def test_correct_data(self):
        correct_user_data = YandexAuth(YandexAuthTester.login, YandexAuthTester.correct_password)
        # проверка на правильные логин и пароль:
        self.assertIn('welcome', correct_user_data.input_login())
        self.assertIn('profile', correct_user_data.input_password())
        correct_user_data.close_browser()

    def test_incorrect_data(self):
        incorrect_user_data = YandexAuth(YandexAuthTester.login, YandexAuthTester.incorrect_password)
        # проверка на правильный логин и неправильный пароль:
        self.assertIn('welcome', incorrect_user_data.input_login())
        self.assertNotIn('profile', incorrect_user_data.input_password())
        incorrect_user_data.close_browser()


if __name__ == '__main__':
    unittest.main()
