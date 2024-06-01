
# include all user-related functions here
# login, register, authenticate
import sys
from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, scoped_session, Session

from data_models.models import Login, RegisteredGuest, Role, Address, Login, Guest
from data_access.data_base import init_db


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

    def create_guest(self, first_name, last_name, email, street, zip, city, bookings):
        query = select(Role).where(Role.name == "guest")
        role = self._session.execute(query).scalars().one()
        new_guest = Guest(
            first_name=first_name,
            last_name=last_name,
            email=email,
            street=street,
            zip=zip,
            city=city,
            bookings=bookings,
        )
        self._session.add(new_guest)
        self._session.commit()

    def create_registered_guest(self, firstname, lastname, email, street, zip, city, username, password, bookings):
        query = select(Role).where(Role.name == "registered_guest")
        role = self._session.execute(query).scalars().one()
        new_registered_guest = RegisteredGuest(
            firstname=firstname,
            lastname=lastname,
            email=email,
            address=Address(street=street, zip=zip, city=city),
            login=Login(username=username, password=password, role=role),
        )
        self._session.add(new_registered_guest)
        self._session.commit()


#Robin, siehst du mich?
    def create_admin(self, username, password):
        query = select(Role).where(Role.name == "registered_admin")
        role = self._session.execute(query).scalars().one()
        new_registered_admin = Registered_admin(
            Username=username,
            password=password,
        )
        self._session.add(new_registered_admin)
        self._session.commit()

    def get_registered_guest(self, login):
        query = select(RegisteredGuest.id).where(RegisteredGuest.login == login)
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

    #print("US: 2.1 - Login")

    # wenn sich ein Benutzer registrieren will
    print("Register User")
    firstname = input("First Name: ")
    lastname = input("Last Name: ")
    email = input("Email: ")
    street = input("Street Address: ")
    zip = input("Zip: ")
    city = input("City: ")
    Username = input("Username: ")
    password = input("Password: ")
    user_manager.register_guest(firstname, lastname, email, street, zip, city, password)

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
            user_manager.logout()
            print(user_manager.get_current_login())
    else:
        print("Too many attempts, close program")
        sys.exit(1)

        #testtest
