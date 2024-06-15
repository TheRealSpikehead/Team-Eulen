# include all navigation functions here
# create menu, display menu, hand-over tasks to different "Managers" e.g. SearchManager/UserManager etc.
from sqlalchemy.orm import scoped_session

from console_base import *
from SearchManager import SearchManager
from InventoryManager import InventoryManager
from ReservationManager import ReservationManager
from UserManager import UserManager
from datetime import datetime

import os
from tkinter import Tk, filedialog

# Annahme: Der Dateipfad zur Datenbankdatei wird als Argument übergeben
database_file = "../data/database.db"

# Erstelle eine Instanz von SearchManager und übergebe den Dateipfad zur Datenbankdatei
search_manager = SearchManager(database_file)
inventory_manager = InventoryManager(database_file)
reservation_manager = ReservationManager(database_file)
user_manager = UserManager(database_file)


class RegistrationConfirmation(Menu):
    def __init__(self, back):
        super().__init__("Hotelreservationsystem - Registeration Confirmation")
        self.add_option(MenuOption("Congratulation! Your new Account was successfully registered!"))
        self.add_option(MenuOption("Back to Login"))
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 2:
                return HotelMenu(self)


class RegisterNewUser(Menu):
    def __init__(self, back):
        super().__init__("Hotelreservationsystem - Register New User")
        self.add_option(MenuOption("Register new account"))
        self.add_option(MenuOption("Back"))
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 1:
                firstname = input("First Name: ")
                lastname = input("Last Name: ")
                email = input("Email: ")
                street = input("Street Address: ")
                zip = input("Zip: ")
                city = input("City: ")
                username = input("Username: ")
                password = input("Password: ")
                user_manager.create_RegisteredGuest(firstname=firstname, lastname=lastname, email=email, street=street,
                                                    zip=zip, city=city, username=username, password=password)
                return RegistrationConfirmation(self)
            case 2:
                return self._back

class BookingDeletionConfirmation(Menu):
    def __init__(self, back, login):
        super().__init__("Hotelreservationsystem - Registeration Confirmation")
        self.add_option(MenuOption("Congratulation! Your Booking was deleted!"))
        self.add_option(MenuOption("Back to HomeScreen"))
        self._login = login
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 2:
                return HomeScreen(self, self._login)

class BookingChanges(Menu):
    def __init__(self, back, mybooking, login):
        super().__init__("Hotelreservationsystem - Change Booking")
        self._mybooking = mybooking
        self._login = login
        self.add_option(MenuOption("Delete Booking"))
        self.add_option(MenuOption("Back"))
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 1:
                inventory_manager.delete_booking(self._mybooking)
                return BookingDeletionConfirmation(self, self._login)
            case 2:
                return self._back

class BookingHistory(Menu):
    def __init__(self, back, login):
        super().__init__("Hotelreservationsystem - Booking Overview")
        guest_id = user_manager.get_RegisteredGuest(login)
        self.booking_history = reservation_manager.get_bookings(guest_id)
        for booking in self.booking_history:
            self.add_option(MenuOption(
                f"Room number: {booking[0]} / Number of guests: {booking[1]} / Start Date: {booking[2]} / End Date: {booking[3]}"))
        self.add_option(MenuOption("Back"))
        self._login = login
        self._back = back

    def _navigate(self, choice: int):
        if choice == len(self.booking_history) + 1:
            # Benutzer hat "Back" ausgewählt
            return self._back
        elif 1 <= choice <= len(self.booking_history):
            mybooking = self.booking_history[choice - 1][5]
            return BookingChanges(self, mybooking, self._login)
        else:
            print("Ungültige Auswahl.")
            return None


# ----------------------------------------------------------------------------------Admin

class AdminRegistrationConfirmation(Menu):
    def __init__(self, back):
        super().__init__("Hotelreservationsystem - Registeration Confirmation")
        self.add_option(MenuOption("Congratulation! Your new Admin Account was successfully registered!"))
        self.add_option(MenuOption("Back to Login"))
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 2:
                return HotelMenu(self)


class RegisterNewAdmin(Menu):
    def __init__(self, back):
        super().__init__("Hotelreservationsystem - Register New User")
        self.add_option(MenuOption("Register new Admin account"))
        self.add_option(MenuOption("Back"))
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 1:
                username = input("Username: ")
                password = input("Password: ")
                user_manager.create_admin(username=username, password=password)
                return AdminRegistrationConfirmation(self)
            case 2:
                return self._back


class BookingOverview(Menu):
    def __init__(self, back):
        super().__init__("Hotelreservationsystem - Booking Overview")
        inventory_manager.get_all_bookings_grouped_by_hotel()
        # self.add_option(MenuOption("Above you see the list of all bookings"))
        self.add_option(MenuOption("Update guest details"))
        self.add_option(MenuOption("Back"))
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 1:
                return UpdateGuestDetails(self)
            case 2:
                return self._back

class UpdateHotel(Menu):
    def __init__(self, back):
        super().__init__("Hotelreservationsystem - Update Hotel")
        self.add_option(MenuOption("Search hotels"))
        self.add_option(MenuOption("Back"))
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 1:
                return SearchHotel(self)
            case 2:
                return self._back

class SearchHotel(Menu):
    def __init__(self,back):
        super().__init__("Hotelreservationsystem - Search Hotel")
        self._hotel = inventory_manager.update_hotel()
        if self._hotel is None:
                self.add_option(MenuOption("This Hotel is not available. Please try again"))
        else:
            self.add_option(MenuOption(f"Congratulation! You updated the following hotel:{self._hotel}"))
        self.add_option(MenuOption("Back"))
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 1:
                return self._back
            case 2:
                return self._back


class UpdateGuestDetails(Menu):
    def __init__(self, back):
        super().__init__("Hotelreservationsystem - UpdateGuest")
        result = inventory_manager.update_guest_info()

        if result == "success":
            self.add_option(MenuOption("Update successful"))
        elif result == "no_change":
            self.add_option(MenuOption("No changes made. Do you want to try again?"))
        elif result == "invalid_input":
            self.add_option(MenuOption("Invalid input, please try again"))
        elif result == "no_booking":
            self.add_option(MenuOption("No booking found with that ID, please try again."))
        else:
            self.add_option(MenuOption("An error occurred"))

        self.add_option(MenuOption("Back"))
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 1:
                return self._back
            case 2:
                return self._back





class DeleteHotel(Menu):
    def __init__(self, back):
        super().__init__("Hotelreservationsystem - Hotel Deletion")
        deletion_massage = inventory_manager.remove_hotel()
        self.add_option(MenuOption(deletion_massage))
        # delete_hotel = self.delete_hotel.name
        # self.add_option(MenuOption(f"Congratulation! You removed the following hotel:{delete_hotel}"))
        self.add_option(MenuOption("Back"))
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 2:
                return self._back


class AddHotel(Menu):
    def __init__(self, back):
        super().__init__("Hotelreservationsystem - Available Hotel")
        self.add_hotel = inventory_manager.add_hotel()
        new_hotel = self.add_hotel.name
        self.add_option(MenuOption(f"Congratulation! You created a new hotel: {new_hotel}"))
        self.add_option(MenuOption("Back"))
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 2:
                return self._back


# ---------------------------------------------------------------------------Guest


class HotelsFilter1(Menu):
    def __init__(self, back, login):
        super().__init__("Hotelreservationsystem - Filter Hotel")
        self.add_option(MenuOption("Filter Hotels and Rooms"))
        self.add_option(MenuOption("Back"))
        self._login = login
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 1:
                valid_date = False
                while not valid_date:
                    try:
                        start_date_input = input("Enter start date (YYYY-MM-DD): ")
                        end_date_input = input("Enter end date (YYYY-MM-DD): ")
                        self._startdate = datetime.strptime(start_date_input, "%Y-%m-%d").date()
                        self._enddate = datetime.strptime(end_date_input, "%Y-%m-%d").date()
                        valid_date = True
                    except ValueError:
                        print("Please enter a valid date in the format YYYY-MM-DD")

                valid = False
                while not valid:
                    try:
                        number_of_guests = input("Number of Guests: ")
                        self._number_of_guests = int(number_of_guests)
                        valid = True
                    except ValueError:
                        print("Please give a number")
                return AvailableRooms(self, start_date=self._startdate, end_date=self._enddate, city=input("City: "),
                                      stars=input("Number of stars: "), max_guests=self._number_of_guests,
                                      login=self._login)
            case 2:
                return self._back



class RoomDetails(Menu):
    def __init__(self, back, myroomid):
        super().__init__("Hotelreservierungssystem - Hotel Information")
        details = search_manager.get_room_details(myroomid)
        for detail in details:
            self.add_option(MenuOption(f"Number: {detail[0]}"))
            self.add_option(MenuOption(f"Type: {detail[1]}"))
            self.add_option(MenuOption(f"Number of Guests: {detail[2]}"))
            self.add_option(MenuOption(f"Amenities: {detail[3]}"))
            self.add_option(MenuOption(f"Description: {detail[4]}"))
            self.add_option(MenuOption(f"Price: {detail[5]}"))
        self.add_option(MenuOption("Back"))
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 7:
                return self._back


class DocumentCreation(Menu):
    def __init__(self, back, login):
        super().__init__("Hotelreservationssystem - Document Creation")
        self.add_option(MenuOption(f"Congratulation! The Document of your Booking was succesfully created"))
        self.add_option(MenuOption("Back to HomeScreen"))
        self._mylogin = login
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 2:
                return HomeScreen(self, self._mylogin)



class ReservationConfirmation(Menu):
    def __init__(self, back, mybooking, login, start_date, end_date, number_of_guests, comment, room_id, guest_id):
        super().__init__("Hotelreservationsystem - Reservation Confirmation")
        self._totalprice = reservation_manager.get_price(mybooking)
        self.add_option(MenuOption(f"Congratulation! Your reservation was processed. Total costs are: {self._totalprice}"))
        self._start_date = start_date
        self._end_date = end_date
        self._number_of_guests = number_of_guests
        self._comment = comment
        self._room_id = room_id
        self._guest_id = guest_id
        self.add_option(MenuOption("Create a Document for my Booking"))
        self.add_option(MenuOption("Back to HomeScreen"))
        self._mylogin = login
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 2:
                #Hier kann ein Dokument der Buchung abgespeichert werden. Es wird ein Fenster hinter pycharm geöffnet
                root = Tk()
                root.withdraw()

                directory = filedialog.askdirectory(title="Wählen Sie ein Verzeichnis zum Speichern des Dokuments")

                #Hier wird der Name des Dokuments angegeben und als Word abgespeichert
                if directory:
                    Document_name = input("Name des Dokument: ")
                    if not Document_name.endswith(".docx"):
                        Document_name += ".docx"
                    file_path = os.path.join(directory, Document_name)
                    reservation_manager.create_document(file_path=file_path, start_date=self._start_date, end_date=self._end_date, number_of_guests=self._number_of_guests, comment=self._comment, room_id=self._room_id, guest_id=self._guest_id, price=self._totalprice)
                return DocumentCreation(self, self._mylogin)
            case 3:
                return HomeScreen(self, self._mylogin)


class Current_Room(Menu):
    def __init__(self, back, myroomid, mymaxguests, mystartdate, myenddate, login):
        super().__init__("Hotelreservierungssystem - Room")
        self.add_option(MenuOption("View Room Details"))
        self._Isguest = user_manager.get_current_login()
        if self._Isguest is None:
            self.add_option(MenuOption("I already did a reservation before"))
            self.add_option(MenuOption("I never did a reservation before"))
        else:
            self.add_option(MenuOption("Make a Reservation"))
            self._rguest = user_manager.get_RegisteredGuest(login)
        self._myroomid = myroomid
        self._mystartdate = mystartdate
        self._myenddate = myenddate
        self._mymaxguests = mymaxguests
        self._mylogin = login
        self.add_option(MenuOption("Back"))
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 1:
                return RoomDetails(self, self._myroomid)
            case 2:
                if self._Isguest is None:       #Hier wird kontrolliert ob es bereits einen Guest User mit dem Vor und Nachnamen gibt
                    while True:
                        firstname = input("Enter firstname: ")
                        lastname = input("Enter lastname: ")
                        guest_id = user_manager.get_Guest(firstname, lastname)
                        if guest_id is not None:
                            print("Successfully found your Guest User")
                            comment = input("Enter a comment here: ")
                            break
                        else:
                            print("There is no User with this name")
                            print("Do you want to try again? y/n")      #Diese Zeile wurde eingeführt damit man die möglichkeit hat den Loop zu unterbrechen
                            answer = input()
                            if answer == "n" or answer == "N":
                                return Current_Room(self, self._myroomid, self._mymaxguests, self._mystartdate, self._myenddate, self._mylogin)

                    mybooking = reservation_manager.make_booking(room_id=self._myroomid, guest_id=guest_id,
                                                                 start_date=self._mystartdate, end_date=self._myenddate,
                                                                 number_of_guests=self._mymaxguests,
                                                                 comment=comment)
                    return ReservationConfirmation(self, mybooking, self._mylogin, self._mystartdate, self._myenddate, self._mymaxguests, comment, self._myroomid, guest_id)
                else:
                    comment = input("Enter a comment here: ")
                    mybooking = reservation_manager.make_booking(room_id=self._myroomid, guest_id=self._rguest,
                                                                 number_of_guests=self._mymaxguests,
                                                                 start_date=self._mystartdate, end_date=self._myenddate,
                                                                 comment=comment)
                    return ReservationConfirmation(self, mybooking, self._mylogin, self._mystartdate, self._myenddate, self._mymaxguests, comment, self._myroomid, self._rguest)
            case 3:
                if self._Isguest is None:       #Hier kann ein neuer Gastuser erstellt werden um eine Reservation zu tätigen
                    print("Please give us your Personal Information so you can proceed with the Reservation")
                    firstname = input("Enter your first name: ")
                    lastname = input("Enter your last name: ")
                    user_manager.create_guest(first_name=firstname, last_name=lastname, email=input("Enter email: "),
                                              street=input("Enter street: "), zip=input("Enter zip: "),
                                              city=input("Enter city: "))
                    guest_id = user_manager.get_Guest(firstname, lastname)
                    print("Your Guest Account was created. Do you want to proceed with the booking? y/n")
                    answer = input()
                    if answer == "y" or answer == "Y":
                        comment = input("Enter a comment here: ")
                        mybooking = reservation_manager.make_booking(room_id=self._myroomid, guest_id=guest_id,
                                                                     start_date=self._mystartdate,
                                                                     end_date=self._myenddate,
                                                                     number_of_guests=self._mymaxguests,
                                                                     comment=comment)
                        return ReservationConfirmation(self, mybooking, self._mylogin, self._mystartdate, self._myenddate, self._mymaxguests, comment, self._myroomid, guest_id)
                    else:
                        return self._back
                else:
                    return self._back
            case 4:
                return self._back


class AvailableRooms(Menu):
    def __init__(self, back, stars, city, start_date, end_date, max_guests, login):
        super().__init__("Hotelreservationsystem - Available Rooms")
        self.available_rooms = search_manager.get_available_hotels_and_rooms(city, stars, max_guests, start_date,
                                                                             end_date)
        if not self.available_rooms:
            self.add_option(MenuOption("No available rooms"))
        else:
            for rooms in self.available_rooms:
                self.add_option(MenuOption(f"Room number: {rooms[1]}, Type: {rooms[2]}, Price: {rooms[3]}"))

        self._mystartdate = start_date
        self._myenddate = end_date
        self._mymaxguests = max_guests
        self._login = login
        self.add_option(MenuOption("Back"))
        self._back = back

    def _navigate(self, choice: int):
        if choice == len(self.available_rooms) + 1:
            # Benutzer hat "Back" ausgewählt
            return self._back
        elif not self.available_rooms:
            return self._back
        elif 1 <= choice <= len(self.available_rooms):
            # Der Benutzer hat ein Hotel ausgewählt
            selected_room = self.available_rooms[choice - 1]
            myroomid = selected_room[-1] #Hier wird nicht der gesamte Wert sondern nur der letzte Wert (room_id) in die Variable geschrieben
            return Current_Room(self, myroomid, self._mymaxguests, self._mystartdate, self._myenddate, self._login)
        else:
            print("Ungültige Auswahl.")
            return None


class HotelDetails(Menu):
    def __init__(self, back, myhotel):
        super().__init__("Hotelreservierungssystem - Hotel Information")
        details = search_manager.get_hotel_information(myhotel)
        for detail in details:
            self.add_option(MenuOption(f"Name: {detail[0]}"))
            self.add_option(MenuOption(f"Stars: {detail[1]}"))
            self.add_option(MenuOption(f"Street: {detail[2]}"))
            self.add_option(MenuOption(f"Zip: {detail[3]}"))
            self.add_option(MenuOption(f"City: {detail[4]}"))
        self.add_option(MenuOption("Back"))
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 6:
                return self._back


class Current_Hotel(Menu):
    def __init__(self, back, myhotel, login=None):
        super().__init__("Hotelreservierungssystem - Hotel")
        self.add_option(MenuOption("View Hotel Details"))
        self._HotelDetails = HotelDetails(self, myhotel)
        # self.add_option(MenuOption("View All Rooms"))
        self.add_option(MenuOption("Available Rooms"))
        self._detail = search_manager.get_hotel_information(myhotel)
        for detail in self._detail: #Hier werden die jeweiligen Information vom Hotel ausgegeben, welche vom Filter verwendet werden
            self._mystars = detail[1]
            self._mycity = detail[4]
        self._login = login
        self.add_option(MenuOption("Back"))
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 1:
                return self._HotelDetails
            case 2:
                valid_date = False #Mit den while try loops wird sichergestellt das ein korrektes Datum und int angegeben werden
                while not valid_date:
                    try:
                        start_date_input = input("Enter start date (YYYY-MM-DD): ")
                        end_date_input = input("Enter end date (YYYY-MM-DD): ")
                        self._startdate = datetime.strptime(start_date_input, "%Y-%m-%d").date()
                        self._enddate = datetime.strptime(end_date_input, "%Y-%m-%d").date()
                        valid_date = True
                    except ValueError:
                        print("Please enter a valid date in the format YYYY-MM-DD")

                valid = False
                while not valid:
                    try:
                        number_of_guests = input("Number of Guests: ")
                        self._number_of_guests = int(number_of_guests)
                        valid = True
                    except ValueError:
                        print("Please give a number")
                return AvailableRooms(self, stars=self._mystars, city=self._mycity, start_date=self._startdate,
                                      end_date=self._enddate, max_guests=self._number_of_guests, login=self._login)
            case 3:
                return self._back


class AllHotels(Menu):
    def __init__(self, back, login=None):
        super().__init__("Hotelreservationsystem - All Hotel")
        self._all_hotels = search_manager.get_all_hotels()
        for hotel in self._all_hotels:
            self.add_option(MenuOption(hotel))
        print(self._all_hotels)
        self._login = login
        self.add_option(MenuOption("Back"))
        self._back = back

    def _navigate(self, choice: int):
        if choice == len(self._all_hotels) + 1:
            # Benutzer hat "Back" ausgewählt
            return self._back
        elif 1 <= choice <= len(self._all_hotels):
            # Der Benutzer hat ein Hotel ausgewählt
            myhotel = self._all_hotels[choice - 1] #Hier wird die Auswahl(Hotel name) des Users in eine Variable geschrieben
            return Current_Hotel(self, myhotel, self._login)
        else:
            print("Ungültige Auswahl.")
            return None


class HomeScreen(Menu):
    def __init__(self, back, login=None):
        super().__init__("Hotelreservationssystem - HomeScreen")
        self.add_option(MenuOption("View all Hotels"))
        self.add_option(MenuOption("Filter Hotels and Rooms"))
        self._login = login
        if login is not None:           #Durch die Variable login und isadmin wird ermittelt welche Menupunkte angezeigt werden
            self._isadmin = user_manager.is_admin(login)
            if self._isadmin == True:
                self.add_option(MenuOption("Add Hotel"))
                self.add_option(MenuOption("Delete Hotel"))
                self.add_option(MenuOption("Update Hotel"))
                self.add_option(MenuOption("View all Bookings"))
                self.add_option(MenuOption("Create new Admin User"))
                self.add_option(MenuOption("Logout"))
                self._back = HotelMenu(self)
            else:
                self.add_option(MenuOption("View Booking history"))
                self.add_option(MenuOption("Logout"))
                self._back = HotelMenu(self)
        else:
            self.add_option(MenuOption("Back"))
            self._back = HotelMenu(self)

    def _navigate(self, choice: int):
        match choice:
            case 1:
                return AllHotels(self, self._login)
            case 2:
                return HotelsFilter1(self, self._login)
            case 3:
                if self._login is None:
                    return self._back
                elif self._isadmin == False:
                    return BookingHistory(self, self._login)
                else:
                    return AddHotel(self)
            case 4:
                if self._isadmin == False:
                    user_manager.logout()
                    return self._back
                else:
                    return DeleteHotel(self)
            case 5:
                return UpdateHotel(self)
            case 6:
                return BookingOverview(self)
            case 7:
                return RegisterNewAdmin(self)
            case 8:
                user_manager.logout()
                return self._back


# ---------------------------------------------------------------------------Base
class HotelMenu(Menu):
    def __init__(self, back):
        super().__init__("Hotel Management")
        self.add_option(MenuOption("Login as Guest"))
        self.add_option(MenuOption("Login with Account"))
        #        self._Home_Admin = HomeScreenAdmin(self)
        self.add_option(MenuOption("Register New Account"))
        self.add_option(MenuOption("Back"))
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 1:
                login = None
                return HomeScreen(self, login)
            case 2:         #Mit diesem Loop wird überprüft ob die Anmeldung valid ist
                while user_manager.has_attempts_left():
                    in_username = input("Enter username: ")
                    in_password = input("Enter password: ")
                    login = user_manager.login(in_username, in_password)
                    if login is not None:
                        print("Login Successful")
                        break
                    else:
                        print("Username or Password wrong!")
                if user_manager.get_current_login() is not None:
                    if user_manager.is_admin(user_manager.get_current_login()):
                        print()
                        print()
                        print(f"Welcome {user_manager.get_current_login().username}")
                        print("Admin rights granted")
                        print()
                        print()
                    else:
                        user_manager.get_RegisteredGuest(user_manager.get_current_login())
                        print()
                        print()
                        print(
                            f"Welcome {user_manager.get_current_login().username} ")
                        print()
                        print()
                else:
                    print("Too many attempts, close program")
                    return None
                return HomeScreen(self, login)
                # user_manager.has_attempts_left()
                # login = user_manager.login(username=input("Username: "), password=input("Password: "))
            case 3:
                return RegisterNewUser(self)
            case 4:
                return MainMenu()


class MainMenu(Menu):
    def __init__(self):
        super().__init__("Main Menu")
        self.add_option(MenuOption("Hotel Management"))
        self._hotel_menu = HotelMenu(self)
        self.add_option(MenuOption("Quit"))

    def _navigate(self, choice: int):
        match choice:
            case 1:
                return self._hotel_menu
            case 2:
                return None


if __name__ == "__main__":
    main_menu = MainMenu()
    app = Application(main_menu)
    app.run()
