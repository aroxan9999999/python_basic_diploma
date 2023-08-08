from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, DateTime, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)
    firstname = Column(String(255), nullable=False)
    searches = relationship('Search', back_populates='user')


class Search(Base):
    __tablename__ = 'searches'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    price = Column(Float, nullable=True)
    promotion_price = Column(Float, nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    country = Column(String(50), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    url = Column(Text, nullable=False)
    image_url = Column(Text, nullable=False)
    user = relationship('User', back_populates='searches')


# Создание базы данных и таблиц
engine = create_engine('mysql+mysqlconnector://root:ARO9510999@localhost/mydatabase')
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
