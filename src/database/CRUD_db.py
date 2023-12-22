import datetime
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import create_engine

from src.database.models import Base, TimeEntry, Date


class Database:
    def __init__(self):
        self.engine = create_engine("sqlite:///database.sqlite3", echo=True)
        self.Session: Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    # This has to work with multiple entries, by now: only one possible
    def insert_time_entry_into_db(self, date, identifier, from_time, to_time):
        try:
            session: Session = self.Session()

            # Logic: when date already in db: skip step of inserting it and simply add time entry to existing date
            date_entry = self.get_or_create_date_entry(session, date)
            self.create_or_update_time_entry(
                session, date_entry, identifier, from_time, to_time
            )

            print(f"Time entries added to the existing record for date {date}.")
            print("Time entries inserted successfully.")

        except IntegrityError as e:
            session.rollback()
            print(f"Error: {e}")
            print("Failed to insert time entries due to a unique constraint violation.")
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
            print("Failed to insert time entries.")

        finally:
            session.close()

    def get_or_create_date_entry(self, session: Session, date: datetime) -> Date:
        existing_date_entry = session.query(Date).filter_by(date_column=date).first()

        if existing_date_entry:
            # Check if the record already exists
            return existing_date_entry

        date_entry = Date(date_column=date)
        session.add(date_entry)
        session.commit()

        return date_entry

    def create_or_update_time_entry(
        self,
        session: Session,
        date_entry: Date,
        identifier: str,
        from_time: int,
        to_time: int,
    ):
        time_entry = (
            session.query(TimeEntry)
            .filter_by(date_id=date_entry.id, identifier=identifier)
            .first()
        )

        if time_entry:
            # Check if the record already exists
            time_entry.from_time = from_time
            time_entry.to_time = to_time

        else:
            # If date hasn't been inserted yet
            new_time_entry = TimeEntry(
                identifier=identifier, from_time=from_time, to_time=to_time
            )
            date_entry.time_entries.append(new_time_entry)

        session.commit()

    def read_time_entries_from_db(self, date):
        try:
            session: Session = self.Session()
            date_id = session.query(Date.id).filter_by(date_column=date).scalar()

            # Query the time entries for the specified date
            selected_time_entries = (
                session.query(TimeEntry)
                .filter_by(date_id=date_id)
                .order_by(TimeEntry.from_time.asc())
                .all()
            )
            return selected_time_entries

        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error: {e}")

        finally:
            session.close()

    def delete_time_entry(self, identifier):
        try:
            session: Session = self.Session()
            stmt = delete(TimeEntry).where((TimeEntry.identifier == identifier))
            session.execute(stmt)
            session.commit()
            print(f"Time entry deleted successfully.")

        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error: {e}")

        finally:
            session.close()
