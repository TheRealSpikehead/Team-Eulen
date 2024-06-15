Teammitglieder:
Robin Meier,Andrej Mauron, Jan Steiner, Flavio Sibilia

Aufgabenaufteilung:
Robin Meier: Navigation Manager
Andrej Mauron: User Manager
Jan Steiner: SearchManager & InventoryManager
Flavio Sibilia: ReservationManager 



Python Interpreter
- Python 3.12
- Interpreter Settings: Project Structure -> Add Content Root -> console -> Sources -> OK

Start der Anwendung
1. Start der Applikation: Run NaviagtionManager.py (Im NavigationManager.py file sind alle Manager miteinander verknüpft).
2. Start Hotel Management: Taste 1
3. Anmeldung: Loggen Sie sich ein als Guest oder mit einem bestehenden Account. Falls die noch keinen Account besitzen, können Sie einen erstellen.
4. Nach abschliessen der Sitzung ausloggen durch Funktion Loggout.
   
Navigation und Input
1. Auswahl von Optionen: Tastenzahl == Zahl nach dem #
2. Back: Schritt zurück zur vorherigen Seite
3. Start- und Endatum müssen mit Bindestrich eingegeben werden


Beschreibung zu den Manager:

ReservationManager: Beim Ausführen des ReservationManagers öffnet sich ein UI, dort kann man nun das gewünschte Startdatum angeben und die Anzahl Tage, die man im Hotel verbringen möchte. 
Bei der Eingabe der Anzahl Gäste, ändert sich die Anzahl der verfügbaren Hotels, je nach Maximalen Plätzen des Hotelzimmers. Falls gewünscht kann man auch einen Kommentar dazu schreiben.
Zusätzlich, hat man die Option, ein Word Dokument erstellen zu lassen, um eine Buchungsbestätigung zu erhalten. Beim erfolgreichen Buchen des Zimmers, ertönt ein Sound.

Gastnutzer(nicht eingeloggt/registriert)
- Ich möchte ein Hotel auswählen, um die Details zu sehen(z.B verfügbare Zimmer) (1.16)
- Als Gastnutzer möchte ich ein Zimmer in einem bestimmten Hotel buchen. (1.3)

Admin-Nutzer
- Als Admin-Nutzer des Buchungssystems möchte ich alle Buchungen aller Hotels sehen können, um eine Übersicht zu erhalten. (3.2)

UserManager
Der Usermanager läuft im Hintergrund und verwaltet Benutzerkonten. Er hat kein eigenes UI, die Funktionen werden durch den Navigation Manager ausgeführt.
Er ermöglicht das Erstellen von neuen Gästen, diese können sich registrieren, um auf mehr Funktionen zugreifen zu können, oder der User kann sich anmelden, wenn bereits eine Registrierung ausgeführt wurde. Auch Admin-User werden durch den UserManager verwaltet.
Bei der Anmeldung von Gästen und Admins wird jeweils nach der Eingabe «username» und «password» gefragt. Die beiden Inputs müssen für eine erfolgreiche Anmeldung mit den hinterlegten Angaben in der Database übereinstimmen. Gelingt die Anmeldung nach drei Versuchen nicht, wird das Programm gestoppt. 
Ob Admin, Gast- oder Registrierter-Nutzer, es können nicht zwei Logins zur selben Zeit ausgeführt werden. Daher ist es wichtig, nach jeder Sitzung die Funktion «logout» aufzurufen.
- Als Gastnutzer möglichst wenige Informationen preisgeben müssen (1.4)
- Als Gastnutzer Details meiner Reservierung in einer lesbaren Form erhalten (1.5)
- Als Gastnutzer sich registrieren können (1.6)
- Als registrierter Nutzer in bestehendes Konto einloggen können(2.1)
- Als registrierter Nutzer auf Buchungshistorie zugreifen können (2.1)
- Als registrierter Nutzer seine Buchungen verwalten können (2.1.1)

InventoryManager
Als Admin bietet mit der InventoryManager die Möglichkeiten, Hotelinformationen zu pflegen, um aktuelle Informationen im System zu haben. Der InventoryManager ist nicht direkt ausführbar, er übergibt die Ergebnisse direkt dem Navigation Manager.
-	Hotels inkl. Räume zum System hinzufügen (3.1.1)
-	Hotels inkl. Räume aus dem System entfernen (3.1.2)
-	Hotels inkl. Räume im System aktualisieren (3.1.3.)
-	Buchungsübersicht aller Hotels der Gäste (3.2)
-	Bearbeitung aller Buchungen der Hotels (3.3)

SearchManager
Dieser bietet dem Gastnutzer und dem registrierten Nutzer die Möglichkeiten, verfügbare Hotels und Zimmer nach seinen Wünschen zu durchsuchen. Der SearchManager ist nicht direkt ausführbar. Er übergibt die Ergebnisse direkt dem NavigationManager.
-	Hotels in einer Stadt durchsuchen (1.1.1)
-	Hotels in einer Stadt, nach Anzahl Sterne durchsuchen (1.1.2)
-	Hotels in einer Stadt, nach Anzahl Sterne und Gästeanzahl durchsuchen (1.1.3)
-	Hotels in einer Stadt, nach Anzahl Sterne, Gästeanzahl, Start- und Enddatum durchsuchen (1.1.4)
-	Übersicht der Information pro Hotel (1.1.5)
-	Übersicht der verfügbaren Zimmer pro Hotel (1.1.6)
-	Übersicht der Informationen eines Zimmers: Zimmertyp, maximale Gästeanzahl, Beschreibung, Ausstattung, Preis pro Nacht     (1.2.1)
-	Nur die verfügbaren Zimmer sehen (1.2.2)

NavigationManager
Der NavigationManager spielt eine zentrale Rolle. Die verschiedenen Manager-Klassen SearchManager, InventoryManager, ReservationManager und UserManager werden importiert und instanziiert, um die Interaktionen zwischen ihnen und dem User zu koordinieren. 
Seine Hauptaufgabe ist es, basierend auf den Eingaben des Benutzers die entsprechenden Funktionen der jeweiligen Manager aufzurufen und die Ansicht der Anwendung dementsprechend anzupassen. Dadurch bietet der NavigationManager eine strukturierte Navigation durch die verschiedenen Menüs.
Diese Menüstruktur wird verwendet, um verschiedene Optionen für Benutzer und Admins bereitzustellen, die es den ihnen erlauben, das Programm wie beabsichtigt zu verwenden. 
Jedes Menü hat Optionen, um zu einer nächsten Menüebene zu gelangen oder um eine Aktion auszuführen.

Beispiele hierfür sind:
Die Aufforderung sich anzumelden nach starten des Programms / die Möglichkeit einen neuen Benutzer zu registrieren.
War dies erfolgreich, wird das «RegistrationConfirmation» Menü angezeigt.
Unter "ReservationConfirmation" werden dem Benutzer nach Abschluss der Buchung die Gesamtkosten angezeigt und der User kann nun entscheiden, ob er ein Dokument erstellen oder zum Hauptmenü zurückkehren möchte.

Oder

Bei «BookingChanges» wird das Löschen einer bestehenden Buchung ermöglicht. Nach erfolgreichem Löschen wird das «BookingDeletionConfimation» Menü angezeigt.
Bei «BookingDeletionConfimation» erhält man neben der Bestätigung, dass eine Buchung erfolgreich gelöscht wurde, auch die Option zum «Home-Bildschirm» zurückzukehren.

Oder

Unter «RegisterNewAdmin» hat man die Möglichkeit einen neuen Admin zu registrieren. Der Benutzer wird aufgefordert, Admin-Benutzernamen und Passwort einzugeben.
Nach erfolgreicher Registrierung wird das «AdminRegistrationConfirmation» Menü angezeigt.
Ebenfalls wird hier eine Bestätigungsmeldung für die erfolgreiche Anmeldung eines neuen Admins angezeigt, und erhält die Option zum regulären Login-Menü.


Annahmen und Interpretationen

UserStory 2.1.1: Die Anwendungsfälle für meine Buchungen sind "neu/erstellen", "ändern/aktualisieren", "stornieren/löschen".
Diese Userstory wurde von uns nicht in ihrer ganzheit übernommen, User können Buchungen über das Fenster "meine Buchungen" stornieren, aber nicht ändern oder erstellen. Grund hierfür ist die unverhältnissmässige Komplexität einer solchen Funktion gegenüber ihres Nutzens. User werden statdessen gebeten ihre Buchung zu stornieren, und regulär eine neue zu erstellen.

Neue Userstory Admin: Als Admin möchte ich neue Admin's hinzufügen können, um neuen Mitarbeitenden Selbstständigkeit am Arbeitsplatz zu bieten.
Wenn man als Admin eingeloggt ist, hat man nun Zugriff auf eine Funktion die das Erstellen eines neuen Admin ermöglicht, so dass dieser sich regulär mit "username" und "password" anmelden kann.

Der Filter wurde Ergänzt:
Im NavigationManager gibt es zwei Filtermöglichkeiten. Es kann durch "view_all_hotels" ein passendes Hotel ausgewählt und anschliessend nach verfügbaren Räumen gefiltert werden. Es ist zusätzlich möglich, ohne ein bestimmtes Hotel einen Filter zu setzen: "Filter Hotels and Rooms". Dadurch kann der Gast Passende Räume finden, ohne sich auf ein Hotel zu beschränken.
