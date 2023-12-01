from persisting import session
from models import Date, Time_Entry
from sqlalchemy import select

dates = session.query(Date).all()

for date in dates:
  print(date)