from sqlalchemy import create_engine

engine = create_engine("sqlite:///database.sqlite3", echo=True)