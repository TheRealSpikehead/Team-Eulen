# include all navigation functions here
# create menu, display menu, hand-over tasks to different "Managers" e.g. SearchManager/UserManager etc.
from sqlalchemy.orm import scoped_session

from console_base import *
from SearchManager import SearchManager
from InventoryManager import InventoryManager
from ReservationManager import ReservationManager
from UserManager import UserManager
from datetime import date

# Annahme: Der Dateipfad zur Datenbankdatei wird als Argument übergeben
database_file = "../data/database.db"

# Erstelle eine Instanz von SearchManager und übergebe den Dateipfad zur Datenbankdatei
search_manager = SearchManager(database_file)
inventory_manager = InventoryManager(database_file)
reservation_manager = ReservationManager(database_file)
user_manager = UserManager(database_file)

# Rufe die Methode get_all_hotels auf der Instanz auf
all_hotels = search_manager.get_all_hotels()

#Der Plan für die Implementation eines Admin Users ist nicht alle Klassen neu zu machen sondern die bestehende Klassen zu erweitern.
#Dazu wird eine Variable weitergegeben die sagt ob sich ein Admin oder User in der Konsole befindet.
#Je nach dem werden gewisse Optionen sichtbar welche für einen Guest User nicht sichtbar sind.
#Dies wird durch die Verwendung von der If else funktion erreicht. Aufpassen bei match choices. Dort weiss ich noch nicht wie ich das Lösen kann.
#Dazu muss aber zuerst der UserManager stehen.

class BookingHistory(Menu):
    def __init__(self, back, login):
        super().__init__("Hotelreservationsystem - Booking Overview")
        guest_id = user_manager.get_registered_guest(login)
        self.booking_history = reservation_manager.get_bookings(guest_id)
        for booking in self.booking_history:
            self.add_option(MenuOption(f"Room number: {booking[0]} / Number of guests: {booking[1]} / Start Date: {booking[2]} / End Date: {booking[3]}"))
        self.add_option(MenuOption("Back"))
        self._back = back

    def _navigate(self, choice: int):
        if choice == len(self.booking_history) + 1:
            # Benutzer hat "Back" ausgewählt
            return self._back
        elif 1 <= choice <= len(self.booking_history):
            return None
        else:
            print("Ungültige Auswahl.")
            return None

#----------------------------------------------------------------------------------Admin
#class AllRooms(Menu):
#    def __init__(self, back, myhotel):
#        super().__init__("Hotelreservationsystem - All Rooms")
#        Hotel_name = myhotel
#        self.all_rooms = search_manager.get_all_rooms(Hotel_name)
#        for allrooms in self.all_rooms:
#            self.add_option(MenuOption(allrooms))
#        self.add_option(MenuOption("Quit"))
#        self._back = back
#
#    def _navigate(self, choice: int):
#        if choice == len(self.all_rooms) + 1:
#            # Benutzer hat "Back" ausgewählt
#            return self._back
#        elif 1 <= choice <= len(self.all_rooms):
            # Der Benutzer hat ein Hotel ausgewählt
#            myroom = self.all_rooms[choice - 1]
#            return Current_Room(self, myroom)
#        else:
#            print("Ungültige Auswahl.")
#            return None

class BookingOverview(Menu):
    def __init__(self, back):
        super().__init__("Hotelreservationsystem - Booking Overview")
        inventory_manager.get_all_bookings_grouped_by_hotel()
        self.add_option(MenuOption("Above you see the list of all bookings"))
        self.add_option(MenuOption("Back"))
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 2:
                return self._back

class UpdateHotel(Menu):
    def __init__(self, back):
        super().__init__("Hotelreservationsystem - Update Hotel")
        self.update_hotel = inventory_manager.update_hotel()
        for hotel in self.update_hotel:
            self.add_option(MenuOption(f"Congratulation! You updated the following hotel:{hotel[0]}"))
        self.add_option(MenuOption("Quit"))
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 2:
                return self._back

class DeleteHotel(Menu):
    def __init__(self, back):
        super().__init__("Hotelreservationsystem - Hotel Deletion")
        self.delete_hotel = inventory_manager.remove_hotel()
        for hotel in self.delete_hotel:
            self.add_option(MenuOption(f"Congratulation! You removed the following hotel:{hotel[0]}"))
        self.add_option(MenuOption("Quit"))
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 2:
                return self._back

class AddHotel(Menu):
    def __init__(self, back):
        super().__init__("Hotelreservationsystem - Available Hotel")
        self.add_hotel = inventory_manager.add_hotel_and_address()
        for hotel in self.add_hotel:
            self.add_option(MenuOption(f"Congratulation! You created a new hotel:{hotel[0]}"))
        self.add_option(MenuOption("Quit"))
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 2:
                return self._back

#---------------------------------------------------------------------------Guest
class HotelsFilter2(Menu):
    def __init__(self, back, start_date, end_date, city, max_guests):
        super().__init__("Hotelreservationsystem - Available Hotel")
        #self.start_date = start_date
        #self.end_date = end_date
        #self.city = city
        #self.max_guests = max_guests
        self.available_hotels = search_manager.get_available_hotels(city, start_date, end_date, max_guests)
        unique_hotels = set(self.available_hotels)
        for hotel in unique_hotels:
            self.add_option(MenuOption(hotel[0]))
        self.add_option(MenuOption("Quit"))
        self._back = back

    def _navigate(self, choice: int):
        if choice == len(self.available_hotels) + 1:
            # Benutzer hat "Back" ausgewählt
            return self._back
        elif 1 <= choice <= len(self.available_hotels):
            # Der Benutzer hat ein Hotel ausgewählt
            myhotel = self.available_hotels[choice - 1][0]
            return Current_Hotel(self, myhotel)
        else:
            print("Ungültige Auswahl.")
            return None


class HotelsFilter1(Menu):
    def __init__(self, back):
        super().__init__("Hotelreservationsystem - Filter Hotel")
        self.add_option(MenuOption("Filter Hotels"))
        self.add_option(MenuOption("Quit"))
        self._back = back

    def _navigate(self, choice: int, available_hotels=None):
        match choice:
            case 1:
                return HotelsFilter2(self, start_date=input("Start Date (YYYY-MM-DD): "), end_date=input("End Date (YYYY-MM-DD): "), city=input("City: "), max_guests=input("Number of Guests: "))
            case 2:
                return self._back

class RoomDetails(Menu):
    def __init__(self, back, myroom, myhotel):
        super().__init__("Hotelreservierungssystem - Hotel Information")
        details = search_manager.get_room_details(myroom, myhotel)
        for detail in details:
            self.add_option(MenuOption(f"Number: {detail[0]}"))
            self.add_option(MenuOption(f"Type: {detail[1]}"))
            self.add_option(MenuOption(f"Number of Guests: {detail[2]}"))
            self.add_option(MenuOption(f"Amenities: {detail[3]}"))
            self.add_option(MenuOption(f"Description: {detail[4]}"))
        self.add_option(MenuOption("Quit"))
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 6:
                return self._back

class ReservationConfirmation(Menu):
    def __init__(self, back, mybooking):
        super().__init__("Hotelreservationsystem - Reservation Confirmation")
        Totalprice = reservation_manager.get_price(mybooking)
        self.add_option(MenuOption(f"Congratulation! Your reservation was processed. Total costs are: {Totalprice}"))
        self.add_option(MenuOption("Quit"))
        self._back = back

    def _navigate(self, choice: int, available_hotels=None):
        match choice:
            case 1:
                return None
            case 2:
                return self._back

class Current_Room(Menu):
    def __init__(self, back, myroom, myhotel, mymaxguests, mystartdate, myenddate):
        super().__init__("Hotelreservierungssystem - Room")
        self.add_option(MenuOption("View Room Details"))
        self._RoomDetails = RoomDetails(self, myroom, myhotel)
        self.add_option(MenuOption("Make a Reservation"))
        self._myroom = myroom
        self._myhotel = myhotel
        self._mystartdate = mystartdate
        self._myenddate = myenddate
        self._mymaxguests = mymaxguests
        self.add_option(MenuOption("Quit"))
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 1:
                return self._RoomDetails
            case 2:
                mybooking = reservation_manager.make_booking(room_id=self._myroom, Hotel_name=self._myhotel, start_date=self._mystartdate, end_date=self._myenddate, number_of_guests=self._mymaxguests, comment=input("Enter a comment here: "))
                return ReservationConfirmation(self, mybooking)
            case 3:
                return self._back

class AvailableRooms(Menu):
    def __init__(self, back, myhotel, start_date, end_date, max_guests):
        super().__init__("Hotelreservationsystem - Available Rooms")
        self.available_rooms = search_manager.get_available_rooms(myhotel, start_date, end_date, max_guests)
        for rooms in self.available_rooms:
            self.add_option(MenuOption(rooms[0]))
        self._myhotel = myhotel
        self._mystartdate = start_date
        self._myenddate = end_date
        self._mymaxguests = max_guests
        self.add_option(MenuOption("Quit"))
        self._back = back

    def _navigate(self, choice: int):
        if choice == len(self.available_rooms) + 1:
            # Benutzer hat "Back" ausgewählt
            return self._back
        elif 1 <= choice <= len(self.available_rooms):
            # Der Benutzer hat ein Hotel ausgewählt
            myroom = self.available_rooms[choice - 1][0]
            return Current_Room(self, myroom, self._myhotel, self._mymaxguests, self._mystartdate, self._myenddate)
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
        self.add_option(MenuOption("Quit"))
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 6:
                return self._back

class Current_Hotel(Menu):
    def __init__(self, back, myhotel):
        super().__init__("Hotelreservierungssystem - Hotel")
        self.add_option(MenuOption("View Hotel Details"))
        self._HotelDetails = HotelDetails(self, myhotel)
        #self.add_option(MenuOption("View All Rooms"))
        self.add_option(MenuOption("Available Rooms"))
        self._myhotel = myhotel
        self.add_option(MenuOption("Quit"))
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 1:
                return self._HotelDetails
            #case 2:
            #    return AllRooms(self, self._myhotel)
            case 2:
                return AvailableRooms(self, self._myhotel, start_date=input("Start Date (YYYY-MM-DD): "),end_date=input("End Date (YYYY-MM-DD): "), max_guests=input("Number of Guests: "))
            case 3:
                return self._back

class AllHotels(Menu):
    def __init__(self, back):
        super().__init__("Hotelreservationsystem - All Hotel")
        for hotel in all_hotels:
            self.add_option(MenuOption(hotel))
#        start_index = 0
#       self.add_option(MenuOption(all_hotels[0]))
#       self.add_option(MenuOption(all_hotels[1]))
#        self.add_option(MenuOption(all_hotels[start_index:0]))
        self.add_option(MenuOption("Quit"))
        self._back = back

    def _navigate(self, choice: int):
        if choice == len(all_hotels) + 1:
            # Benutzer hat "Back" ausgewählt
            return self._back
        elif 1 <= choice <= len(all_hotels):
            # Der Benutzer hat ein Hotel ausgewählt
            myhotel = all_hotels[choice - 1]
            return Current_Hotel(self, myhotel)
        else:
            print("Ungültige Auswahl.")
            return None
class HomeScreen(Menu):
    def __init__(self, back, login=None):
        super().__init__("Hotelreservationssystem - HomeScreen")
        self.add_option(MenuOption("View all Hotels"))
        self._All_Hotels = AllHotels(self)
        self.add_option(MenuOption("Filter Hotels"))
        self._Filter_Hotels1 = HotelsFilter1(self)
        self._login = login
        if login is not None:
            self._isadmin = user_manager.is_admin(login)
            if self._isadmin == True:
                self.add_option(MenuOption("Add Hotel"))
                self.add_option(MenuOption("Delete Hotel"))
                self.add_option(MenuOption("Update Hotel"))
                self.add_option(MenuOption("View all Bookings"))
                self.add_option(MenuOption("Quit"))
                self._back = back
            else:
                self.add_option(MenuOption("View Booking history"))
                self.add_option(MenuOption("Quit"))
                self._back = back
        else:
            self.add_option(MenuOption("Quit"))
            self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 1:
                return self._All_Hotels
            case 2:
                return self._Filter_Hotels1
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
                user_manager.logout()
                return self._back

#---------------------------------------------------------------------------Base
class HotelMenu(Menu):
    def __init__(self, back):
        super().__init__("Hotel Management")
        self.add_option(MenuOption("Login as Guest"))
        self.add_option(MenuOption("Login with Account"))
#        self._Home_Admin = HomeScreenAdmin(self)
        self.add_option(MenuOption("Register New Account"))
        self.add_option(MenuOption("Quit"))
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 1:
                login = None
                return HomeScreen(self, login)
            case 2:
                user_manager.has_attempts_left()
                login = user_manager.login(username=input("Username: "), password=input("Password: "))
                return HomeScreen(self, login)
            case 3:
                self.clear()
                print("Add Hotel")
                input("Press Enter to continue...")
                return self
            case 4:
                return self._back

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
