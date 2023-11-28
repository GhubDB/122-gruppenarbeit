from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    pass
class Row(Base):
  __tablename__ = "rows"

  primary_key = Column("primary_key", Integer, primary_key=True, autoincrement=True)
  date = Column("date", Integer)

  def __init__(self, primary_key, date):
    self.primary_key = primary_key
    self.date = date

  def __repr__(self):
    return f"({self.primary_key}) {self.date}"
  
engine = create_engine("sqlite:///src/database/database.sqlite3", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

row1 = Row(12345)
row2 = Row(12345)
row3 = Row(12345)
session.add(row1)
session.add(row2)
session.add(row3)
session.commit()

show = session.query(Row).all()
print(show)