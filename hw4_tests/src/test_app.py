import unittest
from itertools import chain
from unittest.mock import patch

import app


class AppTester(unittest.TestCase):

    test_doc_number = '10006'
    add_test_doc = ['999', 'passport', 'walter white', '1']

    def setUp(self) -> None:
        # обновляем directories и documents перед каждым тестом:
        app.directories, app.documents = app.update_date()

    def test_check_document_existence(self):
        self.assertTrue(app.check_document_existance('11-2'))
        self.assertFalse(app.check_document_existance('999'))
        self.assertFalse(app.check_document_existance(''))

    @patch('builtins.input', return_value=test_doc_number)
    def test_get_doc_owner_name(self, mock_input):
        doc_owner = [doc['name'] for doc in app.documents if doc['number'] == AppTester.test_doc_number][0]
        self.assertEqual(app.get_doc_owner_name(), doc_owner)

    def test_remove_doc_from_shelf(self):
        app.remove_doc_from_shelf('10006')
        docs = list(chain(app.directories.values()))
        self.assertNotIn('10006', docs)

    def test_add_new_shelf(self):
        # тест: вернула ли функция True или False в зависимости от входных данных:
        self.assertEqual(app.add_new_shelf('new_test_shelf'), ('new_test_shelf', True))
        self.assertEqual(app.add_new_shelf('1'), ('1', False))
        # тест: появился ли действительно новый элемент в directories
        self.assertIn('new_test_shelf', app.directories.keys())

    def test_append_doc_to_shelf(self):
        app.append_doc_to_shelf('new_test_doc', '3')
        self.assertIn('new_test_doc', app.directories['3'])

    @patch('builtins.input', return_value=test_doc_number)
    def test_delete_doc(self, mock_input):
        app.delete_doc()
        docs = [doc['number'] for doc in app.documents]
        self.assertNotIn(AppTester.test_doc_number, docs)

    @patch('builtins.input', return_value=test_doc_number)
    def test_get_doc_shelf(self, mock_input):
        for shelf, doc_list in app.directories.items():
            if AppTester.test_doc_number in doc_list:
                self.assertEqual(app.get_doc_shelf(), shelf)
                break

    def test_show_document_info(self):
        first_doc = f'{app.documents[0]["type"]} "{app.documents[0]["number"]}" "{app.documents[0]["name"]}"'
        last_doc = f'{app.documents[-1]["type"]} "{app.documents[-1]["number"]}" "{app.documents[-1]["name"]}"'
        self.assertEqual(app.show_document_info(app.documents[0]), first_doc)
        self.assertEqual(app.show_document_info(app.documents[-1]), last_doc)

    def test_show_all_docs_info(self):
        docs_from_documents = [f'{doc["type"]} "{doc["number"]}" "{doc["name"]}"' for doc in app.documents]
        self.assertEqual(app.show_all_docs_info(), docs_from_documents)

    @patch('builtins.input', side_effect=add_test_doc)
    def test_add_new_doc(self, mock_input):
        app.add_new_doc()
        doc_number, doc_type, doc_owner, shelf = AppTester.add_test_doc
        new_doc = {'type': doc_type, 'number': doc_number, 'name': doc_owner}
        self.assertIn(new_doc, app.documents)
        self.assertIn(shelf, app.directories)


if __name__ == '__main__':
    unittest.main()
