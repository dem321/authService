from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from services.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    middle_name = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String, default='base')

