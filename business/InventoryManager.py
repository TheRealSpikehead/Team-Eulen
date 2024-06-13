# Möglichkeiten für den Admin Nutzer um Hotels und Buchungen zu verwalten
# Option1: Maintain Hotel Information's -> add Hotel, remove Hotel, update Hotel
# Option2: View all Bookings ... -> get all Bookings -> update Bookings
# Option3: Update room availability ... -> update room availability, update price

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, scoped_session
from data_models.models import *

database_file = "../data/database.db"


class InventoryManager(object):

    def __init__(self, database_file="../data/database.db"):
        self.__engine = engine = create_engine(f'sqlite:///{database_file}', echo=False)
        self.__Session = session = scoped_session(sessionmaker(bind=self.__engine))

    # --------------------------Add hotels to the system----------------------------------------------------------------

    def add_hotel(self):
        session = self.__Session()
        print('-------------------ADDRESS-----------------------')
        street = input(str("Enter new street: "))
        zip = input("Enter new zip: ")
        city = input(str("Enter new city: "))
        new_address = Address(street=street, zip=zip, city=city)
        session.add(new_address)
        session.commit()

        print('---------------------HOTEL-----------------------')
        name = input(str("Enter new hotel name: "))
        stars = input(("Enter stars: "))
        new_hotel = Hotel(name=name, stars=stars, address_id=new_address.id)
        session.add(new_hotel)
        session.commit()

        print('----------------------ROOM-----------------------')
        while True:
            number = input("Enter new room number: ")
            type = input(str("Enter new type: "))
            max_guests = input("Enter maximum guests: ")
            description = input(str("Enter new description: "))
            amenities = input(str("Enter new amenities: "))
            price = input("Enter new price: ")
            new_room = Room(number=number, type=type, max_guests=max_guests, description=description,
                            amenities=amenities,
                            price=price, hotel_id=new_hotel.id)
            session.add(new_room)
            session.commit()

            another_room = input("Doo you want to add another room (y/n)? ")
            if another_room != 'y':
                break

        return new_hotel

    # Der Input Room block wurde in eine While SChleife eingebettet so dass wenn der Benutzer 'y' wählt der ganze Input
    # Block nochmals aufgerufen wird bis er 'n' wählt oder != 'y'

    #     print("Hotel and Address was successfully added")
    #     return new_hotel
    #
    # def close1(self) -> None:
    #     self.__Session.remove()

    # -------------------------------Remove hotels from the system------------------------------------------------------

    def remove_hotel(self):
        session = self.__Session()
        try:
            hotel_name = input("Enter the name of the hotel to be removed: ")
            hotel = session.query(Hotel).filter(Hotel.name == hotel_name).first()
            if not hotel:
                return f"Hotel {hotel_name} was not found."

            rooms = session.query(Room).filter(Room.hotel_id == hotel.id).all()
            for room in rooms:
                bookings = session.query(Booking).filter(Booking.room_hotel_id == room.hotel_id,
                                                         Booking.room_number == room.number).all()
                for booking in bookings:
                    session.delete(booking)
                session.delete(room)

            if hotel.address_id:
                address = session.query(Address).filter(Address.id == hotel.address_id).first()
                if address:
                    session.delete(address)

            session.delete(hotel)
            session.commit()

            return f"Hotel {hotel_name} was successfully removed."

        except Exception as e:
            session.rollback()
            return f"An error has occurred: {e}"

        finally:
            session.close()

    # ------------------------Update hotel information's----------------------------------------------------------------
    def update_hotel(self):
        session = self.__Session()
        try:
            hotel_name = input("Enter the name of the hotel to be updated: ")
            hotel = session.query(Hotel).filter(Hotel.name == hotel_name).first()

            if not hotel:
                print(f"No Hotel {hotel_name} was found")
                return None

            # Update Hotel Information
            new_name = input("New name of the hotel (leave blank if no change): ") or None
            new_stars = input("New star rating (leave blank if no change): ") or None
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

            # List all rooms
            rooms = session.query(Room).filter(Room.hotel_id == hotel.id).all()
            print("Rooms:")
            for room in rooms:
                print(f"Room ID: {room.id}, Number: {room.number}, Type: {room.type}")

            # After listing all rooms, ask for updates
            continue_update = input("Do you want to update any rooms? (y/N): ").strip().lower() == 'y'
            while continue_update:
                selected_room_id = int(input("Enter the Room ID to update: "))
                selected_room = next((room for room in rooms if room.id == selected_room_id), None)

                if selected_room:
                    self.update_room_details(selected_room)

                continue_update = input("Update another room? (y/N): ").strip().lower() == 'y'

            print(f"All updates completed for {hotel_name}.")
            return hotel_name

        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
        finally:
            session.close()

    def update_room_details(self, room):
        session = self.__Session()  # Ensure you have a valid session
        new_number = input("New room number (leave blank if no change): ") or None
        new_type = input("New room type (leave blank if no change): ") or None
        new_max_guest = input("New room max_guest (leave blank if no change): ") or None
        new_description = input("New room description (leave blank if no change): ") or None
        new_amenities = input("New room amenities (leave blank if no change): ") or None
        new_price = input("New room price (leave blank if no change): ") or None

        if new_number:
            room.number = new_number
        if new_type:
            room.type = new_type
        if new_max_guest:
            room.max_guests = new_max_guest
        if new_description:
            room.description = new_description
        if new_amenities:
            room.amenities = new_amenities
        if new_price:
            room.price = new_price

        session.commit()


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
    def update_guest_info(self):
        session = self.__Session()
        # self.get_all_bookings_grouped_by_hotel()
        try:
            booking_id = int(input("Enter the Booking ID to the guest to update: "))
            session = self.__Session()
            booking = session.query(Booking).filter(Booking.id == booking_id).first()
            if not booking:
                print("No bookings found")
                return "no_booking"


            guest = booking.guest
            print(f"Current Guest Name: {guest.firstname}, {guest.lastname}")

            changes_made = False


            new_firstname = input("Enter new firstname (press enter to skip): ")
            new_lastname = input("Enter new lastname (press enter to skip): ")
            new_email = input("Enter new email (press enter to skip): ")

            if new_firstname and new_firstname != guest.firstname:
                guest.firstname = new_firstname
                changes_made = True
            if new_lastname and new_lastname != guest.lastname:
                guest.lastname = new_lastname
                changes_made = True
            if new_email and new_email != guest.email:
                guest.email = new_email
                changes_made = True

            if changes_made:
                session.commit()
                print("Update successful.")
                return "success"
            else:
                print("No changes made. Do you want to try again?")
                return "no_change"

        except ValueError:
            print("Something went wrong. Can you please try again?")
            return "invalid_input"

        except Exception as e:
            print(f"An error occurred: {e}")
            return "error"

        finally:
            session.close()


    def delete_booking(self, bookingid):
        session = self.__Session()
        bookings = session.query(Booking).filter(Booking.id == bookingid).first()
        session.delete(bookings)
        session.commit()


    def add_booking(self):
        pass

    def update_booking(self, bookingid):
        session = self.__Session()





    # # ----------------Update Room availability and Price [Optional]---------------------------------------------------
    #
    # def updateRoomAvailability(self):
    #     pass


if __name__ == "__main__":
    im = InventoryManager()
    # im.add_hotel_and_room()
    # im.remove_hotel()
    # im.update_hotel()
    # im.get_all_bookings_grouped_by_hotel()
    #
    # im.close1()
    # im.close2()
    # im.close3()
    # im.close4()
