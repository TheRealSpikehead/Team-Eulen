Teammitglieder:
Robin Meier,Andrej Mauron, Jan Steiner, Flavio Sibilia

Aufgabenaufteilung:
Robin Meier: Navigation Manager
Andrej Mauron: User Manager
Jan Steiner: SearchManager & InventoryManager
Flavio Sibilia: ReservationManager (User Stories: Als Gastnutzer möchte ich ein Hotel auswählen, um die Details zu sehen; Als Gastnutzer möchte ich ein Zimmer in einem bestimmten Hotel buchen; Als Admin-Nutzer des Buchungssystems möchte ich alle Buchungen aller Hotels sehen können, um eine Übersicht zu haben. 

Python Interpreter
- Python 3.12
- Interpreter Settings: Project Structure -> Add Content -> console -> Sources -> OK

Start der Anwendung
1. Start der Applikation: Run NaviagtionManager.py (Im NavigationManager.py file sind alle Manager miteinadner verknüpft).
2. Start Hotel Management: Taste 1
3. Anmeldung: Loggen SIe sich ein als Guest oder mit einem bestehenden Account. Falls die noch keinen Account besitzen, können Sie einen erstellen.
   
Navigation und Input
1. Auswahl von Optionen: Tastenzahl == Zahl nach dem #
2. Back: Schritt zurück zur vorherigen Seite
3. Start- und Endatum müssen mit Bindestrich eingegeben werden


Anleitung:
ReservationManager: Beim ausführen des ReservationManagers öffnet sich ein UI, dort kann man nun das gewünschte Startdatum angeben und die Anzahl Tage die man im Hotel verbringen möchte. 
Bei der eingabe der Anzahl Gäste, ändert sich die Anzahl der verfügbaren Hotels je nach Maximalen Plätzen des Hotelzimmer. Falls gewünscht kann man auch einen Kommentar dazu schreiben.
Zusätzlich, hat man die Option ein Word Dokument erstellen zu lassen um eine Buchungsbestätigung zu erhalten. Beim erfolgreichen Buchen des Zimmers ertönt ein Sound.

Beschreibung:
UserManager: UserStories 1.4, 1.5, 1.6, 2.1 & 2.1.1
Der Usermanager läuft im Hintergrund und verwaltet Benutzerkonten. Er hat kein eigenes UI, die Funktionen werden durch den Navigation Manager ausgeführt.
Er ermöglicht das Erstellen von neuen Gästen, diese können sich registrieren, um auf mehr Funktionen zugreifen zu können (wie auf die Buchungshistorie zugreifen, oder kommende Buchungen erstellen, ändern oder stornieren). Oder der User kann sich anmelden, wenn bereits eine Registrierung ausgeführt wurde. Auch Admin-User werden durch den UserManager verwaltet.
Bei der Anmeldung von Gästen und Admins wird jeweils nach der Eingabe «username» und «password» gefragt. Die beiden Inputs müssen für eine erfolgreiche Anmeldung mit den hinterlegten Angaben in der Database übereinstimmen. Gelingt die Anmeldung nach drei Versuchen nicht, wird das Programm gestoppt. 
Ob Admin, Gast- oder Registrierter-Nutzer, es kann zu jeder Zeit höchstens ein Login auf dem Programm geben. Daher ist es wichtig, nach jeder Sitzung die Funktion «LOGOUT» aufzurufen.
