from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional, Generator
import datetime

from connect import VKConnect
from model import VKinderUser, SearchResult, SearchParams, ViewedUsers, session, create_tables, engine

vk = VKConnect.user_session.get_api()


@dataclass
class UserInfo:
    """
    Класс для работы с информацией пользователя
    """
    vk_id: int
    first_name: str
    last_name: str
    date_of_birth: str
    city_id: int
    city_title: str

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self

    def get_vk_link(self) -> str:
        """
        Формирует и возвращает ссылку на аккаунт пользователя ВК
        """
        return 'https://vk.com/id' + str(self.vk_id)

    def get_photo(self, n: int = 3) -> List[str]:
        """
        Возвращает список url на самые популярные фото пользователя из альбома профиля
        По умолчанию возвращает топ 3 фото
        """
        response = vk.photos.get(owner_id=self.vk_id, album_id='profile', count=1000, extended=1, photo_sizes=1)[
            'items']
        photos = [(i['likes']['count'], i['sizes'][-1]['url']) for i in response]
        photos = sorted(photos, reverse=True)
        return list(map(lambda x: x[1], photos))[:n]

    def get_full_name(self) -> str:
        """
        Возвращает строку с полным именем пользователя
        """
        return f'{self.first_name} {self.last_name}'

    def get_user_age(self) -> Optional[int]:
        """
        Вычисляет возраст от даты рождения и возвращает его
        Если дата рождения не указана полностью, возвращает None
        """
        try:
            day, month, year = map(int, self.date_of_birth.split('.'))
        except (ValueError, AttributeError):
            return None
        age = int((datetime.date.today() - datetime.date(year, month, day)).days / 365)
        return age


class VKinder:
    """
    Базовый класс для работы с запросами к vk api и бд приложения
    """

    def __init__(self, vk_id: int):
        self.vk_id = vk_id
        self.user_info = self.get_user_info()
        # идентификатор пользователя в таблице vkinder_user
        # переопределяется после срабатывания метода write_user_info('vkinder_user')
        self.id_User = None

    def get_user_info(self):
        """
        Собирает информацию о пользователе программы.
        На основе собранной информации создаёт объект класса UserInfo и возвращает его
        """
        # vk_sex_mapper = {1: 'female', 2: 'male'}
        response = vk.users.get(user_ids=self.vk_id, fields=['bdate', 'city'])[0]
        user_info = UserInfo(response['id'],
                             response['first_name'],
                             response['last_name'],
                             response['bdate'],
                             response['city']['id'],
                             response['city']['title'],
                             )
        return user_info

    def write_user_info(self, table: str) -> Optional[int]:
        """
        Пишет данные пользователя в таблицу vkinder_user если на вход передан параметр 'vkinder_user'
        Пишет данные найденных методом search_user пользователей в таблицу search_result если передан
        параметр 'search_result'
        """
        # выбираем необходимые поля таблицы для последующей записи:
        table_columns = list(filter(lambda x: not x.startswith('_') and x != 'id', VKinderUser.__dict__))

        # запись информации о пользователе в таблицу vkinder_user:
        if table == 'vkinder_user':
            # формируем словарь с данными для записи в таблицу vkinder_user:
            write_data = dict(zip(table_columns, self.user_info.__dict__.values()))
            add_record = VKinderUser(**write_data)
            session.add(add_record)
            session.commit()

            self.id_User = session.query(VKinderUser.id).filter(VKinderUser.vk_id == self.vk_id).first()[0]
            # возвращаем идентификатор пользователя из таблицы vkinder_user
            return self.id_User

        # запись информации о пользователях, полученных в результате метода search_user, в таблицу search_result:
        elif table == 'search_result':
            # список всех vk_id из таблицы search_result:
            existing_ids = session.query(SearchResult.vk_id).filter(SearchResult.id_User == self.id_User).all()
            existing_ids = list(map(lambda x: x[0], existing_ids))

            search_result = self.search_user()
            write_data = []
            for user in search_result:
                # если пользователь с таким vk_id уже есть в таблице, переходим на следующую итерацию:
                if user.vk_id in existing_ids:
                    continue
                else:
                    user_info = dict(zip(table_columns, user.__dict__.values()))
                    # рарсширяем словарь с данными для записи в search_result:
                    user_info.update({'id_User': self.id_User, 'search_date': datetime.datetime.today()})
                    write_data.append(SearchResult(**user_info))
            session.add_all(write_data)
            session.commit()

    def get_search_params(self, gender: int, age_from: int, age_to: int):
        """
        Пишет в таблицу search_params параметры поиска пользователей ВК
        """
        add_record = SearchParams(
            id_User=self.id_User, gender=gender, age_from=age_from, age_to=age_to, date=datetime.datetime.today())
        session.add(add_record)
        session.commit()

    def search_user(self) -> Generator:
        """
        Проводит поиск пользователей вк с параметрами, переданными в бд методом get_search_params
        Для каждого найденного пользователя создаёт объект класса UserInfo и возвращает генератор с объектами
        """
        gender, age_from, age_to, _ = session.query(SearchParams.gender, SearchParams.age_from, SearchParams.age_to,
                                                    SearchParams.date).order_by(SearchParams.id.desc()).first()

        users = vk.users.search(count=1000, city=self.user_info.city_id, sex=gender, age_from=age_from, age_to=age_to,
                                has_photo=1, fields=['id', 'bdate', 'city'])['items']
        for user in users:
            if not user['is_closed']:
                search_result = UserInfo(user['id'],
                                       user['first_name'],
                                       user['last_name'],
                                       user['bdate'] if 'bdate' in user.keys() else None,
                                       user['city']['id'] if 'city' in user.keys() else None,
                                       user['city']['title'] if 'city' in user.keys() else None
                                       )
                yield search_result

    def get_user_from_db(self) -> Tuple[str, str, List[str], int, int]:
        """
        Получает из таблицы search_result первую строку с пользователем, c полем viewed == False
        """
        # выбираем первую запись с непросмотренным пользователелм из search_result:
        user_from_db = session.query(SearchResult).filter(
            SearchResult.id_User == self.id_User and not SearchResult.viewed).limit(1).first()
        # на основе выбранных данных создаём объект класса UserInfo:
        id_search_result = user_from_db.__dict__['id']
        obj = self.create_user_object(user_from_db)
        with obj:
            # выбираем необходимые данные с помощью методов класса UserInfo:
            vk_link = obj.get_vk_link()
            full_name = obj.get_full_name()
            photo = obj.get_photo()
            age = obj.get_user_age() if obj.get_user_age() else None
            # при выходе из контекстного менеджера объект класса UserInfo удаляется

        return vk_link, full_name, photo, age, id_search_result

    @staticmethod
    def create_user_object(user_from_db):
        """
        Принимает на вход строку из таблицы search_result и на основе
        полученных данных  создаёт объект класса UserInfo
        """
        obj_attrs = dict(
            filter(lambda x: x[0] in ['vk_id', 'first_name', 'last_name', 'date_of_birth', 'city_id', 'city_title'],
                   user_from_db.__dict__.items()))
        return UserInfo(**obj_attrs)

    @staticmethod
    def set_user_status(id_search_result: int, status: int):
        """
        Присваивает найденному пользователю статус status, пишет результат в таблицу viewed_users
        Обновляет поле viewed в таблице search_result на True у записи пользователя с id_search_result
        """
        session.add(ViewedUsers(id_SearchResult=id_search_result, status=status))
        session.commit()

        update_viewed_column = session.query(SearchResult).filter(SearchResult.id == id_search_result).first()
        update_viewed_column.viewed = True
        session.commit()

    @staticmethod
    def change_user_status(id_search_result):
        """
        Меняет статус пользователя с id_search_result на противоположный:
        """
        viewed_user = session.query(ViewedUsers).filter(ViewedUsers.id_SearchResult == id_search_result).first()

        if viewed_user.status == 1:
            viewed_user.status = 0
        else:
            viewed_user.status = 1
        session.commit()

    def get_user_by_status(self, status: int):
        """
        Выбирает из бд пользователей со статусом status
        """
        users_from_db = session.query(SearchResult).join(ViewedUsers).filter(
            ViewedUsers.status == status, SearchResult.id_User == self.id_User).all()

        for user in users_from_db:
            id_search_result = user.__dict__['id']
            # на основе выбранных данных создаём объект класса UserInfo:
            user_obj = self.create_user_object(user)
            with user_obj:
                # выбираем необходимые данные с помощью методов класса UserInfo:
                vk_link = user_obj.get_vk_link()
                fullname = user_obj.get_full_name()
                age = user_obj.get_user_age()
                # при выходе из контекстного менеджера объект класса UserInfo удаляется
            yield vk_link, fullname, age, id_search_result

    # @staticmethod
    # def _get_countries() -> List[Dict[str, str]]:
    #     countries = []
    #     offset = 0
    #     while True:
    #         response = vk.database.getCountries(need_all=1, count=1000, offset=offset)
    #         if not response['items']:
    #             break
    #         else:
    #             countries.extend(response['items'])
    #             offset += 1000
    #     return countries
    #
    # @staticmethod
    # def _get_regions(countries):
    #     regions = []
    #     for country in countries:
    #         response = vk.database.getRegions(country_id=country['id'], count=1000)
    #         if response['count'] > 0:
    #             for region in response['items']:
    #                 regions.append({'id': region['id'], 'title': region['title'], 'country_id': country['id']})
    #     return regions
    #
    # @staticmethod
    # def _get_cities():
    #     cities = []
    #     offset = 0
    #
    #     response = vk.database.getCities(country_id=1, region_id=1077676, need_all=1,
    #                                      count=1000, offset=offset)
    #     for city in response['items']:
    #         print(city['id'], city['title'], city['area'], city['region'])
    #     return cities
    # for region in regions:
    #     if response['count']>1000:
    #         pass
    #     response = vk.database.getCities(country_id=region['country_id'], region_id=region['id'], need_all=1,
    #                                      count=1000, offset=offset)
    #     print(response)


if __name__ == '__main__':
    engine.connect().execute("""drop table search_result, search_params, vkinder_user, viewed_users;""")
    create_tables()

    user = VKinder(1)
    user.write_user_info('vkinder_user')
    user.get_search_params(1, 18, 20)
    user.write_user_info('search_result')
    # меняем критерии и выполняем повторный поиск:
    user.get_search_params(1, 18, 25)
    user.write_user_info('search_result')

    # устанавливаем статус для найденных пользователей:
    *_, id1 = user.get_user_from_db()
    user.set_user_status(id1, 0)

    *_, id2 = user.get_user_from_db()
    user.set_user_status(id2, 1)

    *_, id3 = user.get_user_from_db()
    user.set_user_status(id3, 0)

    *_, id4 = user.get_user_from_db()
    user.set_user_status(id4, 1)

    # выбираем пользователей по статусу:
    status0 = user.get_user_by_status(0)
    status1 = user.get_user_by_status(1)

    print('status = 0')
    for s0 in status0:
        print(s0)

    print('----------------------')

    print('status = 1')
    for s1 in status1:
        print(s1)

    # меняем статус у пользователей с id1 и id2
    user.change_user_status(id1)
    user.change_user_status(id2)

    print('\nпосле изменения статуса пользователей с id#1 и id#2:\n')

    status0 = user.get_user_by_status(0)
    status1 = user.get_user_by_status(1)

    print('status = 0')
    for s0 in status0:
        print(s0)

    print('----------------------')

    print('status = 1')
    for s1 in status1:
        print(s1)
