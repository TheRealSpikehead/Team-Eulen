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
        self.start_date = start_date
        self.end_date = end_date
        self.city = city
        self.max_guests = max_guests
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
            return all_hotels[choice - 1]
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
