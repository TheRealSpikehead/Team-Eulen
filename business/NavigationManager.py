# include all navigation functions here
# create menu, display menu, hand-over tasks to different "Managers" e.g. SearchManager/UserManager etc.

from console_base import *

class AllHotels(Menu):
    def __init__(self):
        super().__init__("HomeScreen - Guest")
        self.add_option(MenuOption("View all Hotels"))
        self.add_option(MenuOption("Filter Hotels"))
        self.add_option(MenuOption("Quit"))

    def _navigate(self, choice: int):
        match choice:
            case 1:
                return None
            case 2:
                return None
            case 3:
                return None
class HomeScreenGuest(Menu):
    def __init__(self):
        super().__init__("HomeScreen - Guest")
        self.add_option(MenuOption("View all Hotels"))
        self._All_Hotels = AllHotels()
        self.add_option(MenuOption("Filter Hotels"))
        self.add_option(MenuOption("Quit"))

    def _navigate(self, choice: int):
        match choice:
            case 1:
                return self._All_Hotels
            case 2:
                return None
            case 3:
                return None

class HotelMenu(Menu):
    def __init__(self, back):
        super().__init__("Hotel Management")
        self.add_option(MenuOption("Login as Guest"))
        self._Home_Guest = HomeScreenGuest()
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
