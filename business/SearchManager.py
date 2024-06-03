from pathlib import Path
import sm
from sqlalchemy import create_engine, select, join, func, and_, or_
from sqlalchemy.orm import sessionmaker, scoped_session, aliased
from data_access.data_base import init_db
from data_models.models import *
from data_models.models import Booking
from datetime import datetime


class SearchManager(object):
    def __init__(self, database_file):
        database_path = Path(database_file)
        if not database_path.is_file():
            init_db(database_file, generate_example_data=True)
        self.__engine = create_engine(f'sqlite:///{database_file}', echo=False)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))

    # --------------------------------get hotels------------------------------------------------------------------------
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
    def get_hotel_information(self):
        query = select(
            Hotel.name, Hotel.stars, Address.city, Address.street, Address.zip
        ).join(Address, Hotel.address_id == Address.id)

        result = self.__session.execute(query).fetchall()

        if not result:
            print("No hotel information found.")
        else:
            print("Hotel Information:")
            current_hotel = None
            for hotel in result:
                if current_hotel != hotel.name:
                    if current_hotel is not None:
                        print("")
                    current_hotel = hotel.name
                    print(f"Hotel: {hotel.name}")
                    print(f"    Stars: {hotel.stars}")
                    print(f"    City: {hotel.city}")
                    print(f"    Street: {hotel.street}")
                    print(f"    Zip: {hotel.zip}")
                else:

                    print(f"    Stars: {hotel.stars}")
                    print(f"    City: {hotel.city}")
                    print(f"    Street: {hotel.street}")
                    print(f"    Zip: {hotel.zip}")

    # ------------------------------get room details--------------------------------------------------------------------
    def get_room_details(self):
        query = select(Hotel.name, Room.number, Room.type,Room.price, Room.type,
                       Room.description, Room.price, Room.amenities, Room.price).\
            join(Hotel, Hotel.id == Room.hotel_id)

        result = self.__session.execute(query).fetchall()

        if not result:
            print("No room details found.")
        else:
            print("Room Details:")
            current_hotel = None
            for room in result:
                if current_hotel != room.name:
                    # Neues Hotel, also drucken wir den Hotelnamen
                    current_hotel = room.name
                    print(f"\nHotel: {room.name}")
                # Drucken der Zimmerdetails
                print(
                    f"  Number: {room.number}, Type: {room.type}, Price: {room.price}, "
                    f"Amenities: {room.amenities}, Description: {room.description}"
                )

    # -------------------------get available hotels---------------------------------------------------------------------
    def get_available_hotels(self):

        city = input("Enter the city (leave blank if not specific): ") or None
        stars = input("Enter minimum stars (leave blank if not specific): ") or None
        max_guests = input("Enter maximum guests (leave blank if not specific): ") or None
        start_date = input("Enter start date (YYYY-MM-DD, leave blank if not specific): ") or None
        end_date = input("Enter end date (YYYY-MM-DD, leave blank if not specific): ") or None

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

        query = select(Hotel). \
            join(Address). \
            join(Room, Hotel.id == Room.hotel_id). \
            outerjoin(Booking, Room.hotel_id == Booking.room_hotel_id). \
            group_by(Hotel.id)

        conditions = []

        if city:
            conditions.append(Address.city == city)
        if stars:
            conditions.append(Hotel.stars >= int(stars))
        if max_guests:
            conditions.append(Room.max_guests >= int(max_guests))

        booking_conditions = []

        if start_date and end_date:
            booking_conditions.append(or_(
                Booking.id.is_(None),
                Booking.end_date <= start_date, Booking.start_date >= end_date)
            )

        if booking_conditions:
            conditions.append(and_(*booking_conditions))

        if conditions:
            query = query.where(and_(*conditions))

        available_hotels = self.__session.execute(query).scalars().all()

        if not available_hotels:
            print("No available hotels found.")
        else:
            print("Available hotels:")
            for hotel in available_hotels:
                print(f"Hotel Name: {hotel.name}, Located in: {hotel.address.city}")

    # -----------------------available Rooms in hotels------------------------------------------------------------------

    def get_userinput(self):
        city = input("Enter the city (leave blank if not specific): ") or None
        stars = input("Enter minimum stars (leave blank if not specific): ") or None
        max_guests = input("Enter maximum guests (leave blank if not specific): ") or None
        start_date = input("Enter start date (YYYY-MM-DD, leave blank if not specific): ") or None
        end_date = input("Enter end date (YYYY-MM-DD, leave blank if not specific): ") or None
        return city, stars, max_guests, start_date, end_date

    def get_available_hotels_and_rooms(self, city, stars, max_guests, start_date, end_date):

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

        query = select(Hotel.name, Room.number, Room.description, Room.price). \
            join(Address). \
            join(Room, Hotel.id == Room.hotel_id). \
            outerjoin(Booking, and_(Room.hotel_id == Booking.room_hotel_id, Room.number == Booking.room_number))

        conditions = []

        if city:
            conditions.append(Address.city == city)
        if stars:
            conditions.append(Hotel.stars >= int(stars))
        if max_guests:
            conditions.append(Room.max_guests >= int(max_guests))

        booking_conditions = []

        if start_date and end_date:
            booking_conditions.append(or_(
                Booking.id.is_(None),
                and_(
                    Booking.end_date <= start_date, Booking.start_date >= end_date))
            )

        if booking_conditions:
            conditions.append(and_(*booking_conditions))

        if conditions:
            query = query.where(and_(*conditions))

        available_rooms = self.__session.execute(query).all()

        if not available_rooms:
            print("No available rooms found.")
        else:
            print("Available rooms:")
            for room in available_rooms:
                print(f"Hotel Name: {room[0]}, Room Number: {room[1]}, Description: {room[2]}, Price: {room[3]}")


if __name__ == "__main__":
    sm = SearchManager('../data/database.db')
    city, stars, max_guests, start_date, end_date = sm.get_userinput()
    sm.get_available_hotels_and_rooms(city, stars, max_guests, start_date, end_date)
    # sm.get_available_hotels()
    # sm.get_room_details()
    # sm.get_hotel_information()




