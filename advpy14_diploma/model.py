from sqlalchemy import Integer, String, Date, Boolean, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from connect import BDConnect

Base = declarative_base()
engine = BDConnect.engine

session = BDConnect.session


class VKinderUser(Base):
    __tablename__ = 'vkinder_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    vk_id = Column(Integer)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(String)
    city_id = Column(Integer)
    city_title = Column(String)


class SearchParams(Base):
    __tablename__ = 'search_params'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_User = Column(Integer, ForeignKey('vkinder_user.id'))
    gender = Column(Integer, nullable=False)
    age_from = Column(Integer, nullable=False)
    age_to = Column(Integer, nullable=False)
    date = Column(Date)


class SearchResult(Base):
    __tablename__ = 'search_result'
    id = Column(Integer, primary_key=True, autoincrement=True)
    vk_id = Column(Integer, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(String, default='')
    city_id = Column(Integer)
    city_title = Column(String)
    id_User = Column(Integer, ForeignKey('vkinder_user.id'))
    search_date = Column(Date)
    viewed = Column(Boolean, default=False)


class ViewedUsers(Base):
    __tablename__ = 'viewed_users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_SearchResult = Column(Integer, ForeignKey('search_result.id'))
    status = Column(Integer)


# class Country(Base):
#     __tablename__ = 'country'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     title = Column(String)
#
#
# class Region(Base):
#     __tablename__ = 'region'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     title = Column(String)
#     country_id = Column(String, ForeignKey('country.id'))
#
#
# class City(Base):
#     __tablename__ = 'city'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     title = Column(String)
#     region_id = Column(String, ForeignKey('region.id'))

def create_tables():
    Base.metadata.create_all(engine)
