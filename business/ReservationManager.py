# include all functions related to reservations here
# make reservation, retrieve all reservations for a hotel, retrieve reservations for a user
# check for appropriate user roles inside the functions
# Flavio
# reservation_manager.py

from pathlib import Path
from math import modf
from datetime import datetime, timedelta

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, scoped_session

from data_access.data_base import init_db
from data_models.models import Room, Guest, Booking, RegisteredGuest


class ReservationManager(Manager):
    def __init__(self, db_file):
        if not db_file.is_file():
            init_db(str(db_file), generate_example_data=True)
        self._engine = create_engine(f'sqlite:///{db_file}')
        self._session = scoped_session(sessionmaker(bind=self._engine))

    def make_booking(self, room_id:int, guest_id:int, number_of_guests:int, start_date: datetime, end_date: datetime, comment:str = None):
        query_room = select(Room).where(Room.id == room_id)
        room = self._session.execute(query_room).scalars().one()
        query_guest = select(Guest).where(Guest.id == guest_id)
        guest = self._session.execute(query_guest).scalars().one()
        if number_of_guests <= room.max_guests:
            new_booking = Booking(
                room=room,
                guest=guest,
                number_of_guests=number_of_guests,
                start_date=start_date,
                end_date=end_date,
                comment=comment
            )
            self._session.add(new_booking)
            self._session.commit()
            return new_booking
        else:
            raise ValueError('Number of guests is bigger than the room allows')

    def get_price(self, booking:Booking):
        duration = booking.end_date - booking.start_date
        price = booking.room.price * duration.days
        price_mwst = round(price + price*0.077, 2)
        return self.round_for_currency(price), self.round_for_currency(price_mwst)

    def round_for_currency(self, price):
        first_digit = modf(price)[0]*10
        to_round = round(modf(first_digit)[0]/10, 2)
        if to_round < 0.03:
            diff = round(0.0-to_round, 2)
        elif to_round < 0.07:
            diff = round(0.05-to_round, 2)
        else:
            diff = 0.1-to_round
        result = round(price+diff, 2)
        return result

    def get_bookings(self, registered_guest:RegisteredGuest):
        query = select(Booking).where(Booking.guest == registered_guest)
        result = self._session.execute(query).scalars().all()
        return result

if __name__ == '__main__':
    manager = ReservationManager(Path("../data/test.db"))

    date_format = '%d.%m.%Y'
    in_date = input("Enter start date (DD.MM.YYY): ")

    start_date = datetime.strptime(in_date, date_format)
    duration = input("Enter how many days you stay: ")
    duration = int(duration)
    end_date = start_date + timedelta(days=duration)
    number_of_guests = input("Enter the number of guests: ")
    number_of_guests = int(number_of_guests)
    comment = input("Enter any additional comment for your booking: ")
    booking = manager.make_booking(1, 4, number_of_guests, start_date, end_date, comment)

