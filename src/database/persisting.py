from models import Date, Time_Entry
from sqlalchemy.orm import Session
from connect import engine

session = Session(bind=engine)

date1 = Date(
  date_column = 28112023,
  time_entries = [
    Time_Entry(time_from=10, time_to=12)
  ]
)
date2 = Date(
  date_column = 28112024,
  time_entries = [
    Time_Entry(time_from=11, time_to=12),
    Time_Entry(time_from=14, time_to=18)
  ]
)
date3 = Date(
  date_column = 28112025,
  time_entries = [
    Time_Entry(time_from=2, time_to=12),
    Time_Entry(time_from=17, time_to=22)
  ]
)

session.add_all([date1, date2, date3])
session.commit()