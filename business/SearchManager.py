from pathlib import Path
from sqlalchemy import create_engine, select, join, and_, or_
from sqlalchemy.orm import sessionmaker, scoped_session
from data_access.data_base import init_db
from data_models.models import *
from data_models.models import Booking


class SearchManager(object):
    def __init__(self, database_file):
        database_path = Path(database_file)
        if not database_path.is_file():
            init_db(database_file, generate_example_data=True)
        self.__engine = create_engine(f'sqlite:///{database_file}', echo=False)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))

    # --------------------------------get all hotels--------------------------------------------------------------------
    def get_all_hotels(self):
        query = select(Hotel.name, Hotel)
        allhotels = self.__session.execute(query).scalars().all()
        return allhotels

    # ---------------------------------get all rooms--------------------------------------------------------------------
    def get_all_rooms(self, Hotel_name):
        query = select(Room.number). \
            select_from(Hotel). \
            outerjoin(Room, Hotel.id == Room.hotel_id). \
            where(and_(Hotel.name == Hotel_name))
        rooms = self.__session.execute(query).scalars().all()
        return rooms

    # --------------------------get hotel information-------------------------------------------------------------------
    def get_hotel_information(self, Hotel_name):
        j = join(Hotel, Address, Hotel.address_id == Address.id)
        query = select(Hotel.name, Hotel.stars, Address.street, Address.zip, Address.city).select_from(j). \
            where(and_(Hotel.name == Hotel_name))
        details = self.__session.execute(query).fetchall()
        return details

    # ------------------------------get room details--------------------------------------------------------------------
    def get_room_details(self, room_id):
        j = join(Hotel, Room, Hotel.id == Room.hotel_id)
        query = select(Room.number, Room.type, Room.max_guests, Room.amenities, Room.description,
                       Room.price).select_from(j)
        if room_id:
            query = query.where(Room.id == room_id)
        room_details = self.__session.execute(query)
        return room_details

    # -----------------------available rooms in hotels------------------------------------------------------------------
    def get_available_hotels_and_rooms(self, city: str, stars: int, max_guests: int, start_date: str, end_date: str):
        query = select(Hotel.name, Room.number, Room.description, Room.price, Room.id). \
            join(Address). \
            join(Room, Hotel.id == Room.hotel_id)

        # Subquery, überprüft in einem Raum alle Buchungen, so dass wenn eine Buchung von bsp. 3 Buchungen
        # in einem Raum ein Konflikt darstellt, der Room nicht zurück gegeben wird.
        conflict_query = select(Booking.room_number). \
            where(and_(Room.hotel_id == Booking.room_hotel_id, Room.number == Booking.room_number,
                       or_(and_(Booking.start_date <= end_date, Booking.start_date >= start_date),
                           and_(Booking.end_date >= start_date, Booking.end_date <= end_date),
                           and_(Booking.start_date <= start_date, Booking.end_date >= end_date)))). \
            distinct()

        conditions = []

        if city:
            conditions.append(Address.city == city)
        if stars:
            conditions.append(Hotel.stars >= stars)
        if max_guests:
            conditions.append(Room.max_guests >= max_guests)

        # Die Hauptabfrage schließt jetzt alle Zimmer aus, die in der Konflikt-Subquery zurückgegeben werden
        conditions.append(Room.number.notin_(conflict_query))

        if conditions:
            query = query.where(and_(*conditions))

        # Gruppierung, um Duplikate zu vermeiden
        query = query.group_by(Room.number, Hotel.name, Room.description, Room.price, Room.id)

        # Ausführen der Abfrage
        available_rooms = self.__session.execute(query).fetchall()

        if not available_rooms:
            print("No available hotels found.")

        return available_rooms



if __name__ == "__main__":
    sm = SearchManager('../data/database.db')

