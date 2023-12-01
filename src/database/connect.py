from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///database.sqlite3", echo=True)