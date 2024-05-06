from pathlib import Path
from sqlalchemy import create_engine, select
from sqlalchemy.orm import joinedload, session
from sqlalchemy.orm import sessionmaker, scoped_session
from data_access.data_base import init_db
from data_models.models import *

class SerachManager(object):
    def __init__(self, database_file):
        database_path = Path(database_file)
        if not database_path.is_file():
            init_db(database_file, generate_examples=False)
        self.__engine = engine = create_engine(f'sqlite:///{database_file}', echo=False)
        self.__session = session = scoped_session(sessionmaker(bind= self.__engine))


    def get_hotels(self, name: str = None, stars: int = None, address: str = None):
        query = select(Hotel)

        if name:
            query = query.where(Hotel.name.like(f"%{name}%"))
        if stars is not None:
            query = query.where(Hotel.stars == stars)
        if address:
            query = query.join(Hotel.address).where(Address.city.like(f"%{address}%"))

        hotels = self.__session.execute(query).scalars().all()
        return hotels


if __name__ == "__main__":
    sm = SerachManager('../data/hotel_reservation.db')

    name = input("Geben Sie den Namen des Hotels ein (oder lassen Sie das Feld leer): ")
    stars_input = input("Geben Sie die Sterneanzahl des Hotels ein (oder lassen Sie das Feld leer): ")
    address = input("Geben Sie die Stadtadresse des Hotels ein (oder lassen Sie das Feld leer): ")

    # Konvertierung der Sterne-Eingabe in einen Integer, falls nicht leer
    stars = int(stars_input) if stars_input.isdigit() else None

    # Suche durchführen
    hotels = sm.get_hotels(name=name if name else None, stars=stars, address=address if address else None)

    if hotels:
        print(f"Anzahl gefundener Hotels: {len(hotels)}")
        for hotel in hotels:
            print(hotel)  # Angenommen, `hotel` ist eine Instanz, die sinnvoll als String dargestellt werden kann
    else:
        print("Keine Hotels gefunden, die den Kriterien entsprechen.")