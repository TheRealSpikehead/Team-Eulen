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
        query = select(Hotel)
        allhotels = self.__session.execute(query).scalars().all()
        return allhotels


    def get_all_rooms(self, Hotel_name):
        query = select(Room.number). \
            select_from(Hotel). \
            outerjoin(Room, Hotel.id == Room.hotel_id). \
            where(and_(Hotel.name == Hotel_name))
        rooms = self.__session.execute(query).scalars().all()
        return rooms

    def get_available_rooms(self, Hotel_name: str, start_date: date, end_date: date, max_guests: int):  # 1.1.4
        query = select(Room.number, Hotel). \
            join(Address). \
            outerjoin(Room, Hotel.id == Room.hotel_id). \
            outerjoin(Booking, and_(Room.number == Booking.id,
                                    or_(Booking.end_date < start_date, Booking.start_date > end_date))). \
            where(and_(Hotel.name == Hotel_name, Room.max_guests >= max_guests)). \
            group_by(Hotel.id, Room.number). \
            having(func.count(Booking.id) == 0)

        available_rooms2 = self.__session.execute(query).fetchall()
        return available_rooms2

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

    def get_hotel_information(self, Hotel_name):  # 1.1.5
        j = join(Hotel, Address, Hotel.address_id == Address.id)
        query = select(Hotel.name, Hotel.stars, Address.street, Address.zip, Address.city).select_from(j).\
            where(and_(Hotel.name == Hotel_name))
        details = self.__session.execute(query)
        return details


    def get_room_details(self, room_number, Hotel_name):
        j = join(Hotel, Room, Hotel.id == Room.hotel_id)
        query = select(Room.number, Room.type, Room.max_guests, Room.amenities, Room.description).select_from(j)
        if room_number:
            query = query.where(Room.number == room_number, Hotel.name == Hotel_name)
        room_details = self.__session.execute(query)
        return room_details

    def list_hotels(self):
        query = select(Hotel.name).distinct()
        hotels = self.__session.execute(query)
        return [hotel[0] for hotel in hotels]


if __name__ == "__main__":

    sm = SearchManager('../data/database.db')

    start_date = date(2024, 1, 1)
    end_date = date(2024, 12, 31)
    Hotel_name = "Hotel Amaris"
    max_guests = 2

    #available_rooms = sm.get_available_rooms(Hotel_name, start_date, end_date, max_guests)
    #for hotel in available_rooms:
    #    print(f"Hotel: {hotel[0]}, Stars: {hotel[1]}, Room: {hotel[2]}, Capacity: {hotel[3]}")

    # hotels = sm.list_hotels()
    # print("Available hotels:")
    # for idx, name in enumerate(hotels, start=1):
    #     print(f"{idx}: {name}")
    #
    # choice = int(input("Wählen Sie ein Hotel durch Eingabe der entsprechenden Nummer: "))
    # if 1 <= choice <= len(hotels):
    #     hotel_name = hotels[choice - 1]
    #     room_details = sm.get_room_details(hotel_name)
    #     print(f"Zimmerdetails für Hotel: {hotel_name}")
    #     for detail in room_details:
    #         print(f"Room_number: {detail[0]}, Zimmerart: {detail[1]}, Max. Gäste: {detail[2]}, "
    #               f"Ausstattung: {detail[3]}, Beschreibung: {detail[4]}")
    # else:
    #     print("Ungültige Auswahl!")


    # room_details = sm.get_room_details()
    # for detail in room_details:
    #     print(f"Hotelname: {detail[0]}, Room_type: {detail[1]}, guests: {detail[2]}, "
    #           f"Amanities: {detail[3]}, Description: {detail[4]}")
    #
    # details = sm.get_hotel_information()
    # for detail in details:
    #     print(f"Name: {detail[0]}, Stars: {detail[1]}, Street: {detail[2]}, Zip: {detail[3]}, City: {detail[4]}")

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



    # start_date = date(2024, 1, 1)
    # end_date = date(2024, 12, 31)
    # city = "Olten"
    # max_guests = 2
    #
    # available_hotels = sm.get_available_hotels(city, start_date, end_date, max_guests)
    # for hotel in available_hotels:
    #     print(f"Hotel: {hotel[0]}, Stars: {hotel[1]}, Room: {hotel[2]}, Capacity: {hotel[3]}")


