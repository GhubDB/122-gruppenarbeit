from sqlalchemy import create_engine, ForeignKey, Column, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    pass
class Row(Base):
  __tablename__ = "rows"
  id = Column(Integer, primary_key=True, autoincrement=True )
  date = Column("date", Integer)

  def __init__(self, id, date):
    self.id = id
    self.date = date

  def __repr__(self):
    return f"({self.id}) {self.date}"

class Time(Base):
   __tablename__ = "time_entries"

   id = Column(Integer, primary_key=True, autoincrement=True)
   time_from = ("from", Integer)
   time_to = ("to", Integer)
   date = Column(Integer, ForeignKey("Row.id"))
   
   def __init__(self, id, time_from, time_to, date):
      self.id = id
      self.time_from = time_from
      self.time_to = time_to
      self.date = date
    
   def __repr__(self):
    return f"({self.id}) {self.time_to} on {self.date}"
  


engine = create_engine("sqlite:///src/database/database.sqlite3", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

row1 = Row(12345)
row2 = Row(1234235)
row3 = Row(1234245)
session.add(row1)
session.add(row2)
session.add(row3)
session.commit()

show = session.query(Row).all()
print(show)