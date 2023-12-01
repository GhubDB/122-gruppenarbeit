from sqlalchemy import create_engine

engine = create_engine("sqlite:///src/database/database.sqlite3", echo=True)