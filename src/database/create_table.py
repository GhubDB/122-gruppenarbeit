from models import Base
from CRUD_db import engine

print("Creating Tables")
Base.metadata.create_all(bind=engine)