from persisting import session
from models import Date, Time_Entry
from sqlalchemy import update

time_from = session.query(Time_Entry).filter_by(id=1).first()

time_from.integer = 111111