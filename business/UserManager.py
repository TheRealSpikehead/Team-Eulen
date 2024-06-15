import tkinter as tk
# include all user-related functions here
# login, register, authenticate
import sys
from pathlib import Path


from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, scoped_session, session
from sqlalchemy.sql.functions import current_user

from data_models.models import Login, RegisteredGuest, Role, Address, Login, Guest
from data_access.data_base import init_db
import os


def admin(Username, password):
    pass

def guest(first_name, last_name, email, street, zip, city):
    pass

def registeredGuest(firstname, lastname, email, street, zip, city, username, password):
    pass

class UserManager:
    def __init__(self, database_file):
        database_path = Path(database_file)
        if not database_path.is_file():
            init_db(database_file, generate_example_data=True)
        self.__engine = create_engine(f'sqlite:///{database_file}', echo=False)
        self._session = scoped_session(sessionmaker(bind=self.__engine))
        self._MAX_ATTEMPTS = 3
        self._attempts_left = self._MAX_ATTEMPTS
        self._current_login = None

#Es wird definiert dass man nur drei Loginversuche hat
    def has_attempts_left(self):
        if self._attempts_left > 0:
            return True
        else:
            print(f'Attempts left: {self._attempts_left}')
            return False


    def login(self, username, password):
        if self.has_attempts_left():
            query = select(Login).where(Login.username == username).where(Login.password == password)
            result = self._session.execute(query).scalars().one_or_none()
            self._attempts_left -= 1
            self._current_login = result
            return result
            print("Login succsessful")
        else:
            raise PermissionError("Too many attempts")

    def logout(self):
        self._current_login = None
        self._attempts_left = self._MAX_ATTEMPTS
        print("User logged out")

    def get_current_login(self):
        return self._current_login

    def get_bookings(self):
        return self.bookings()

#User sowie Admins werden hier erstellt

    def create_guest(self, first_name, last_name, email, street, zip, city):
        query = select(Guest).where(Guest.type == "guest")
        self._session.execute(query).scalars().first()
        type = "guest"
        new_guest = Guest(
            firstname=first_name,
            lastname=last_name,
            email=email,
            type=type,
            address=Address(street=street, zip=zip, city=city),
        )
        self._session.add(new_guest)
        self._session.commit()

    def create_RegisteredGuest(self, firstname, lastname, email, street, zip, city, username, password):
        query = select(Role).where(Role.name == "registered_user")
        role = self._session.execute(query).scalars().one()
        new_RegisteredGuest = RegisteredGuest(
            firstname=firstname,
            lastname=lastname,
            email=email,
            address=Address(street=street, zip=zip, city=city),
            login=Login(username=username, password=password, role=role),
        )
        self._session.add(new_RegisteredGuest)
        self._session.commit()


    def create_admin(self, username, password):
        query = select(Role).where(Role.name == "administrator")
        role = self._session.execute(query).scalars().one()
        new_admin = Login(
            username=username, password=password, role=role
        )
        self._session.add(new_admin)
        self._session.commit()

    def get_Guest(self, firstname, lastname):
        query = select(Guest.id).where(Guest.firstname == firstname, Guest.lastname == lastname)
        result = self._session.execute(query).scalars().one_or_none()
        return result

    def get_RegisteredGuest(self, login):
        query = select(RegisteredGuest.id).where(RegisteredGuest.login == login)
        result = self._session.execute(query).scalars().one_or_none()
        return result

    def get_admin(self, login):
        query = select(admin).where(admin.login == login)
        result = self._session.execute(query).scalars().one_or_none()
        return result

    def is_admin(self, login:Login):
        if login.role.access_level < sys.maxsize:
            return False
        else:
            return True

if __name__ == "__main__":

    db_file = "../data/test.db"
    db_path = Path(db_file)

    #if not db_path.is_file():
    #   init_db(db_file, generate_example_data=True)
    #engine = create_engine(f"sqlite:///{db_path}", echo=False)
    #session = scoped_session(sessionmaker(bind=engine))
    user_manager = UserManager(db_path)

