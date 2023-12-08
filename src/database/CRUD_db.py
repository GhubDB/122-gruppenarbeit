from sqlalchemy.orm import Session
from connect import engine
from models import Date, Time_Entry
from sqlalchemy import update, delete, select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

session = Session(bind=engine)

# This has to work with multiple entries, by now: only one possible
def insert_time_entries_into_db(date, time_from, time_to):
    try:
        # Check if the record already exists
        existing_date_entry = session.query(Date).filter_by(date_column=date).first()
        # Logic: when date already in db: skip step of inserting it and simply add time entry to existing date 
        if existing_date_entry:
            time_entry = Time_Entry(time_from=time_from, time_to=time_to)
            existing_date_entry.time_entries.append(time_entry)
            session.commit()
            print(f"Time entries added to the existing record for date {date}.")
        # If date hasn't been inserted yet
        else:
            # Insert the new record
            date_entry = Date(
                date_column=date,
                time_entries=[
                    Time_Entry(time_from=time_from, time_to=time_to)
                ]
            )
            session.add(date_entry)
            session.commit()
            print("Time entries inserted successfully.")

    except IntegrityError as e:
        session.rollback()
        print(f"Error: {e}")
        print("Failed to insert time entries due to a unique constraint violation.")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        print("Failed to insert time entries.")

# insert_time_entries_into_db(2, 10, 14)

def read_time_entries_from_db(date):
        date_id = session.query(Date.id).filter_by(date_column=date).scalar()

        # Query the time entries for the specified date
        stmt = (
            select(Time_Entry)
            .where(Time_Entry.date_id == date_id)
        )

        # Iterate through the results and print each time entry
        # How can I display them? Printing works
        for time_entry in session.execute(stmt):
            print(time_entry)

read_time_entries_from_db(2)


# Delete a row --> not really necessary!
def delete_time_entry(date, time_from, time_to):
    date_id = session.query(Date.id).filter_by(date_column=date).scalar()
    try:
        stmt = (
            delete(Time_Entry)
            .where(
                (Time_Entry.date_id == date_id) &
                (Time_Entry.time_from == time_from) &
                (Time_Entry.time_to == time_to)
            )
        )
        session.execute(stmt)
        session.commit()
        print(f"Time entry deleted successfully.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()
# delete_time_entry(2026, 17, 22)


"""
Code needed to experiment below
"""
# Updating the date works 
try:
    stmt = (
        update(Date)
        .where(Date.id == 1)
        .values(date_column=113124)
    )
    session.execute(stmt)
    session.commit()
except SQLAlchemyError as e:
    session.rollback()
    print(f"Error: {e}")
finally:
    session.close()

# update a time_entry
try:
    stmt = (
        update(Time_Entry)
        .where(Time_Entry.id == 1)
        .values(time_from=12, time_to=13)
    )
    session.execute(stmt)
    session.commit()
except SQLAlchemyError as e:
    session.rollback()
    print(f"Error: {e}")
finally:
    session.close()