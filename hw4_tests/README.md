# Домашнее задание к лекции 4.«Tests»

### Задача №1 unit-tests
Из курса «Python: программирование на каждый день и сверхбыстрое прототипирование» необходимо протестировать программу по работе с бухгалтерией [Лекции 2.1](https://github.com/netology-code/py-homework-basic/tree/master/2.1.functions).
При наличии своего решения данной задачи можно использовать его или использовать предложенный код в директории scr текущего задания.

* Следует протестировать основные функции по получению информации о документах, добавлении и удалении элементов из словаря.
* Используйте fixture для загрузки данных в тестовый класс.

### Задача №2 Автотест API Яндекса
Проверим правильность работы Яндекс.Диск REST API. Написать тест, проверяющий создание папки на Диске.  
Используя библиотеку request напишите unit-test на верный ответ и возможные отрицательные тесты на ответы с ошибкой

Пример положительных тестов:
* Код ответа соответствует 200.
* Результат создания папки - папка появилась в списке файлов.

### Задача №3. Дополнительная (не обязательная)
Применив selenium, напишите unit-test для авторизации на Яндексе по url: https://passport.yandex.ru/auth/
