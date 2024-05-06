from pathlib import Path
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, scoped_session


from data_access.data_base import init_db
from data_models.models import *

class SearchManager(object):
    def __init__(self, database_file):
        database_path = Path(database_file)
        if not database_path.is_file():
            init_db(database_file, generate_example_data=True)
        self.engine = create_engine(f'sqlite:///{database_file}', echo=False)
        self.session = scoped_session(sessionmaker(bind=self.engine))

    def get_all_hotels(self):
        query = select(Hotel)
        hotels = self.session.execute(query).scalars().all()
        return hotels

    def get_hotels_by_name(self, name):
        query = select(Hotel).where(Hotel.name.like(f"%{name}%"))
        hotels = self.session.execute(query).scalars().all()
        return hotels


if __name__ == "__main__":
    sm = SearchManager('../data/database.db')

    hotels = sm.get_all_hotels()
    for hotel in hotels:
        print(hotel)

    name = input("Enter the hotel name: ")
    hotels = sm.get_hotels_by_name(name)
    for hotel in hotels:
        print(hotel)

