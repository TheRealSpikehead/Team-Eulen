# Möglichkeiten für den Admin Nutzer um Hotels und Buchungen zu verwalten
# Option1: Maintain Hotel Information's -> add Hotel, remove Hotel, update Hotel
# Option2: View all Bookings ... -> get all Bookings -> update Bookings
# Option3: Update room availability ... -> update room availability, update price

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from data_models.models import *


database_file = "../data/database.db"


class InventoryManager(object):

    def __init__(self, database_file="../data/database.db"):
        self.__engine = engine = create_engine(f'sqlite:///{database_file}', echo=False)
        self.__Session = session = scoped_session(sessionmaker(bind=self.__engine))

    # --------------------------Add hotels to the system----------------------------------------------------------------

    def add_hotel_and_address(self):

        session = self.__Session()

        street = input("Enter the street: ")
        zip = input("Enter the zip: ")
        city = input("Enter the city: ")

        new_address = Address(street=street, zip=zip, city=city)
        session.add(new_address)
        session.commit()

        name = input("Enter the name of the hotel: ")
        stars = int(input("Enter number of stars: "))

        new_hotel = Hotel(name=name, stars=stars, address_id=new_address.id)
        session.add(new_hotel)
        session.commit()

        print("Hotel and Address was successfully added")
        return new_hotel

    def close1(self) -> None:
        self.__Session.remove()

    # -------------------------------Remove hotels from the system------------------------------------------------------

    def remove_hotel(self):
        session = self.__Session()
        try:

            hotel_name = input("Enter the name of the hotel to be removed: ")
            hotel = session.query(Hotel).filter(Hotel.name == hotel_name).first()
            if hotel:
                address_id = hotel.address_id
                session.delete(hotel)
                session.commit()

                address = session.query(Address).filter(Address.id == address_id).first()
                if address:
                    session.delete(address)
                    session.commit()
                return hotel
                #print(f"Hotel {hotel_name} was successfully removed.")
            else:
                print(f"Hotel {hotel_name} was not found")
        except Exception as e:
            print(f"An Error has occurred: {e}")
            session.rollback()
        finally:
            session.close()


    def close2(self) -> None:
        self.__Session.remove()

    # ------------------------Update hotel information's----------------------------------------------------------------

    def update_hotel(self):
        session = self.__Session()
        try:
            hotel_name = input("Enter the name of the hotel to be updated: ")
            hotel = session.query(Hotel).filter(Hotel.name == hotel_name).first()

            if hotel is not None:

                if hotel:
                    new_name = input("New name of the hotel (leave blank if no change): ") or None
                    new_stars = input("New star rating  (leave blank if no change): ") or None
                    new_street = input("New street (leave blank if no change): ") or None
                    new_zip = input("New zip (leave blank if no change): ") or None
                    new_city = input("New city (leave blank if no change): ") or None

                    if new_name:
                        hotel.name = new_name
                    if new_stars:
                        hotel.stars = int(new_stars)
                    if new_street:
                        hotel.address.street = new_street
                    if new_zip:
                        hotel.address.zip = new_zip
                    if new_city:
                        hotel.address.city = new_city
                session.commit()
                return hotel_name
                #print(f"Hotel '{hotel_name}' was successfully updated!.")
            else:
                return None #print(f"No Hotel {hotel_name} was found")

        except Exception as e:
            session.rollback()
            print(f"Error: {e}")

        finally:
            session.close()

    def close3(self) -> None:
        self.__Session.remove()

    # ----------------------View all bookings from each Hotel-----------------------------------------------------------

    def get_all_bookings_grouped_by_hotel(self):
        session = self.__Session()
        try:
            # Abfrage aller Hotels mit ihren Buchungen
            hotels = session.query(Hotel).all()
            bookings = session.query(Booking).order_by(Booking.start_date.desc()).all()
            bookings_by_hotel = {hotel.id: [] for hotel in hotels}
            for booking in bookings:
                bookings_by_hotel[booking.room_hotel_id].append(booking)

            for hotel in hotels:
                print(f"\nHotel: {hotel.name}")
                if bookings_by_hotel[hotel.id]:
                    for booking in bookings_by_hotel[hotel.id]:
                        print(
                            f"  Booking ID: {booking.id:2}\t Room no.: {booking.room_number}\t"
                            f" Guest ID: {booking.guest_id}\t No of Guests: {booking.number_of_guests}\t"
                            f" Start Date: {booking.start_date}\t End Date: {booking.end_date}")
                else:
                    print("  No bookings found")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            session.close()

    def close4(self):
        session = self.__Session.remove()

    # --------------------------------Edit Bookings [Optional]----------------------------------------------------------
    # def update_Bookings(self):
    #     session = self.__Session()

    # # ----------------Update Room availability and Price [Optional]---------------------------------------------------
    #
    # def updateRoomAvailability(self):
    #     pass


if __name__ == "__main__":
    im = InventoryManager()
    im.add_hotel_and_address()
    im.remove_hotel()
    im.update_hotel()
    im.get_all_bookings_grouped_by_hotel()

    im.close1()
    im.close2()
    im.close3()
    im.close4()
