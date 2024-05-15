# include all navigation functions here
# create menu, display menu, hand-over tasks to different "Managers" e.g. SearchManager/UserManager etc.

from console_base import *
from SearchManager import SearchManager
from datetime import date

# Annahme: Der Dateipfad zur Datenbankdatei wird als Argument übergeben
database_file = "../data/database.db"

# Erstelle eine Instanz von SearchManager und übergebe den Dateipfad zur Datenbankdatei
search_manager = SearchManager(database_file)

# Rufe die Methode get_all_hotels auf der Instanz auf
all_hotels = search_manager.get_all_hotels()


#available_hotels = search_manager.get_available_hotels(start_date=input("Start date: "), end_date=input("End date: "))

class HotelsFilter2(Menu):
    def __init__(self, back, start_date, end_date, city, max_guests):
        super().__init__("Hotelreservationsystem - Available Hotel")
        #self.start_date = start_date
        #self.end_date = end_date
        #self.city = city
        #self.max_guests = max_guests
        self.available_hotels = search_manager.get_available_hotels(city, start_date, end_date, max_guests)
        for hotel in self.available_hotels:
            self.add_option(MenuOption(hotel[0]))
        self.add_option(MenuOption("Quit"))
        self._back = back

    def _navigate(self, choice: int):
        if choice == len(self.available_hotels) + 1:
            # Benutzer hat "Back" ausgewählt
            return self._back
        elif 1 <= choice <= len(self.available_hotels):
            # Der Benutzer hat ein Hotel ausgewählt
            return self.available_hotels[choice - 1]
        else:
            print("Ungültige Auswahl.")
            return None


class HotelsFilter1(Menu):
    def __init__(self, back):
        super().__init__("Hotelreservationsystem - Filter Hotel")
        self.add_option(MenuOption("Enter Start Date"))
        self.add_option(MenuOption("Quit"))
        self._back = back

    def _navigate(self, choice: int, available_hotels=None):
        match choice:
            case 1:
                #available_hotels = search_manager.get_available_hotels(start_date = input("Start date: "),end_date = input("End date: "),city = input("Enter City: "),max_guests = (input("Enter number of Guests: ")))
                #return HotelsFilter2(self, start_date=date(2024, 1, 1), end_date=date(2024, 12, 31), city="Olten", max_guests= 2)  # Erstellen einer Instanz von HotelsFilter2 mit den verfügbaren Hotels
                return HotelsFilter2(self, start_date=input("Start Date (YYYY-MM-DD): "), end_date=input("End Date (YYYY-MM-DD): "), city=input("City: "), max_guests=input("Number of Guests: "))

            case 2:
                return self._back

class RoomDetails(Menu):
    def __init__(self, back, myroom):
        super().__init__("Hotelreservierungssystem - Hotel Information")
        details = search_manager.get_room_details(myroom)
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

class Current_Room(Menu):
    def __init__(self, back, myroom):
        super().__init__("Hotelreservierungssystem - Room")
        self.add_option(MenuOption("View Room Details"))
        self._RoomDetails = RoomDetails(self, myroom)
        self.add_option(MenuOption("Make a Reservation"))
        self._myroom = myroom
        self.add_option(MenuOption("Quit"))
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 1:
                return self._RoomDetails
            case 2:
                return None
            case 3:
                return self._back

class AvailableRooms(Menu):
    def __init__(self, back, myhotel, start_date, end_date, max_guests):
        super().__init__("Hotelreservationsystem - Available Rooms")
        Hotel_name = myhotel
        self.available_rooms = search_manager.get_available_rooms(Hotel_name, start_date, end_date, max_guests)
        for rooms in self.available_rooms:
            self.add_option(MenuOption(f"Room Number:{rooms[0]}"))
        self.add_option(MenuOption("Quit"))
        self._back = back

    def _navigate(self, choice: int):
        if choice == len(self.available_rooms) + 1:
            # Benutzer hat "Back" ausgewählt
            return self._back
        elif 1 <= choice <= len(self.available_rooms):
            # Der Benutzer hat ein Hotel ausgewählt
            myroom = self.available_rooms[choice - 1]
            return Current_Room(self, myroom)
        else:
            print("Ungültige Auswahl.")
            return None

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
class HomeScreenGuest(Menu):
    def __init__(self, back):
        super().__init__("HomeScreen - Guest")
        self.add_option(MenuOption("View all Hotels"))
        self._All_Hotels = AllHotels(self)
        self.add_option(MenuOption("Filter Hotels"))
        self._Filter_Hotels1 = HotelsFilter1(self)
        self.add_option(MenuOption("Quit"))
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 1:
                return self._All_Hotels
            case 2:
                return self._Filter_Hotels1
            case 3:
                return self._back

class HotelMenu(Menu):
    def __init__(self, back):
        super().__init__("Hotel Management")
        self.add_option(MenuOption("Login as Guest"))
        self._Home_Guest = HomeScreenGuest(self)
        self.add_option(MenuOption("Login with Account"))
        self.add_option(MenuOption("Register New Account"))
        self.add_option(MenuOption("Quit"))
        self._back = back

    def _navigate(self, choice: int):
        match choice:
            case 1:
                return self._Home_Guest
            case 2:
                self.clear()
                print("Add Hotel")
                input("Press Enter to continue...")
                return self
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
