from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///database.sqlite3", echo=True)

with engine.connect() as connection:
  result = connection.execute(text('select "Hello"'))
  print(result.all())