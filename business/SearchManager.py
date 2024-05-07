from pathlib import Path
import sqlite3

import sm
from sqlalchemy import create_engine, select, join, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import joinedload, session
from sqlalchemy import and_, or_, not_
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker, scoped_session
from data_access.data_base import init_db
from data_models.models import *
from datetime import date
from data_models.models import Booking


class SearchManager(object):
    def __init__(self, database_file):
        database_path = Path(database_file)
        if not database_path.is_file():
            init_db(database_file, generate_example_data=True)
        self.__engine = engine = create_engine(f'sqlite:///{database_file}', echo=False)
        self.__session = session = scoped_session(sessionmaker(bind=self.__engine))

    def get_hotels(self, name: str = None, stars: int = None, address: str = None):
        query = select(Hotel)

        if name:
            query = query.where(Hotel.name.like(f"%{name}%"))
        if stars is not None:
            query = query.where(Hotel.stars == stars)
        if address:
            query = query.join(Hotel.address).where(Address.city.like(f"%{address}%"))

        hotels = self.__session.execute(query).scalars().all()
        return hotels

    def get_all_hotels(self):
        query = select(Hotel.name, Hotel)
        allhotels = self.__session.execute(query).scalars().all()
        return allhotels

    def get_all_rooms_by_date(self, date: str):
        pass

    def get_all_rooms(self):
        query = select(Room)
        rooms = self.__session.execute(query).scalars().all()
        return rooms

    def get_available_hotels(self, city: str, start_date: date, end_date: date, max_guests: int):  # 1.1.4
        query = select(Hotel.name, Hotel.stars, Room.number, Room.max_guests). \
            join(Address). \
            outerjoin(Room, Hotel.id == Room.hotel_id). \
            outerjoin(Booking, and_(Room.number == Booking.id,
                                    or_(Booking.end_date < start_date, Booking.start_date > end_date))). \
            where(and_(Address.city == city, Room.max_guests >= max_guests)). \
            group_by(Hotel.id, Room.number). \
            having(func.count(Booking.id) == 0)

        available_rooms = self.__session.execute(query).fetchall()
        return available_rooms

    def get_hotel_informations(self):  # 1.1.5
        j = join(Hotel, Address, Hotel.address_id == Address.id)
        query = select(Hotel.name, Hotel.stars, Address.street, Address.zip, Address.city).select_from(j)
        details = self.__session.execute(query)
        return details


if __name__ == "__main__":

    sm = SearchManager('../data/database.db')

    # name = input("Geben Sie den Namen des Hotels ein (oder lassen Sie das Feld leer): ")
    # stars_input = input("Geben Sie die Sterneanzahl des Hotels ein (oder lassen Sie das Feld leer): ")
    # address = input("Geben Sie die Stadtadresse des Hotels ein (oder lassen Sie das Feld leer): ")
    #
    # # Konvertierung der Sterne-Eingabe in einen Integer, falls nicht leer
    # stars = int(stars_input) if stars_input.isdigit() else None
    #
    # # Suche durchführen
    # hotels = sm.get_hotels(name=name if name else None, stars=stars, address=address if address else None)
    #
    # if hotels:
    #     print(f"Anzahl gefundener Hotels: {len(hotels)}")
    #     for hotel in hotels:
    #         print(hotel)  # Angenommen, `hotel` ist eine Instanz, die sinnvoll als String dargestellt werden kann
    # else:
    #     print("Keine Hotels gefunden, die den Kriterien entsprechen.")

    # hotels = sm.get_hotels()
    # for hotel in hotels:
    #     print(hotel)

    # allrooms = sm.get_all_rooms()
    # for room in allrooms:
    #     print(room)

    # details = sm.get_hotel_informations()  ## 1.1.5
    # for detail in details:
    #     print(f"Name: {detail[0]}, Stars: {detail[1]}, Street: {detail[2]}, Zip: {detail[3]}, City: {detail[4]}")

    start_date = date(2024, 1, 1)
    end_date = date(2024, 12, 31)
    city = "Olten"
    max_guests = 2

    available_hotels = sm.get_available_hotels(city, start_date, end_date, max_guests)
    for hotel in available_hotels:
        print(f"Hotel: {hotel[0]}, Stars: {hotel[1]}, Room: {hotel[2]}, Capacity: {hotel[3]}")
