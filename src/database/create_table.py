from models import Base, Date, Time_Entry
from connect import engine

print("Creating Tables")
Base.metadata.create_all(bind=engine)