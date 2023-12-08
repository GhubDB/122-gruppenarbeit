from models import Date, Time_Entry
from sqlalchemy.orm import Session
from connect import engine
from sqlalchemy.exc import IntegrityError
session = Session(bind=engine)

""" 
Commented out as otherwise unique constraint error 
date1 = Date(
  date_column = 281122023,
  time_entries = [
    Time_Entry(time_from=10, time_to=12)
  ]
)
date2 = Date(
  date_column = 281212024,
  time_entries = [
    Time_Entry(time_from=11, time_to=12),
    Time_Entry(time_from=14, time_to=18)
  ]
)
date3 = Date(
  date_column = 20226,
  time_entries = [
    Time_Entry(time_from=2, time_to=12),
    Time_Entry(time_from=17, time_to=22)
  ]
)

session.add_all([date1, date2, date3])
session.commit() """


