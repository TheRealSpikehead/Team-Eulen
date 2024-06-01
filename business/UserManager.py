# include all user-related functions here
# login, register, authenticate
import sys
from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, scoped_session

from data_models.models import Login, RegisteredGuest
from data_access.data_base import init_db


class UserManager:
    def __init__(self, session: scoped_session):
        self._session = session
        self._MAX_ATTEMPTS = 3
        self._attempts_left = self._MAX_ATTEMPTS
        self._current_login = None

    def has_attempts_left(self):
        if self._attempts_left > 0:
            return True
        else:
            return False

    def login(self, username, password):
        if self.has_attempts_left():
            query = select(Login).where(Login.username == username).where(Login.password == password)
            result = self._session.execute(query).scalars().one_or_none()
            self._attempts_left -= 1
            self._current_login = result
            return result
        else:
            raise PermissionError("Too many attempts")

    def logout(self):
        self._current_login = None
        self._attempts_left = self._MAX_ATTEMPTS

    def get_current_login(self):
        return self._current_login

    def create_registered_guest(self, username, password):
        # get registered_guest role from db
        role = None
        # create RegisteredGuest object

        reg_guest = RegisteredGuest(
            login=Login(username, password, role)
        )
        self._session.add(reg_guest)
        self._session.commit()

    def create_admin(self, was_brauch_ich_für_parameter):
        pass

    def get_registered_guest(self, login):
        query = select(RegisteredGuest).where(RegisteredGuest.login == login)
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

    if not db_path.is_file():
        init_db(db_file, generate_example_data=True)
    engine = create_engine(f"sqlite:///{db_path}", echo=False)
    session = scoped_session(sessionmaker(bind=engine))
    user_manager = UserManager(session)

    print("US: 2.1 - Login")
    while user_manager.has_attempts_left():
        in_username = input("Enter username: ")
        in_password = input("Enter password: ")
        if user_manager.login(in_username, in_password) is not None:
            print("Login Successful")
            break
        else:
            print("Username or Password wrong!")
    if user_manager.get_current_login() is not None:
        if user_manager.is_admin(user_manager.get_current_login()):
            print(f"Welcome {user_manager.get_current_login().username}")
            print("Admin rights granted")
        else:
            reg_user = user_manager.get_registered_guest(user_manager.get_current_login())
            print(f"Welcome {reg_user.firstname} {reg_user.lastname}")
    else:
        print("Too many attempts, close program")
        sys.exit(1)



    print("US: 2.2 - Register")

