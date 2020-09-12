import unittest
from folder_creator import create_folder


class FolderCreatorTester(unittest.TestCase):
    def setUp(self) -> None:
        self.folder_creator = create_folder

    def test_code(self):
        # ожидаем, что код ответа будет начинаться на "2"
        # если код ответа другой, проверка возвращает False и печатает код
        code = create_folder('test')
        self.assertTrue(str(code).startswith('2'), f'что-то пошло не так! код ответа: {code}')


if __name__ == '__main__':
    unittest.main()
