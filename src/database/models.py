from typing import List
from sqlalchemy import ForeignKey, String
from sqlalchemy import Integer
from sqlalchemy import Date
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Date(Base):
    __tablename__ = "dates"
    id: Mapped[int] = mapped_column(primary_key=True)
    date_column: Mapped[int] = mapped_column(unique=True, nullable=False)
    time_entries: Mapped[List["TimeEntry"]] = relationship(back_populates="date")

    def __repr__(self) -> str:
        return f"<ID = (id={self.id}), date={self.date_column}"


class TimeEntry(Base):
    __tablename__ = "time_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    identifier: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    from_time: Mapped[int] = mapped_column(Integer, nullable=False)
    to_time: Mapped[int] = mapped_column(Integer, nullable=False)
    date_id: Mapped[int] = mapped_column(ForeignKey("dates.id"), nullable=False)
    date: Mapped["Date"] = relationship(back_populates="time_entries")

    def __repr__(self) -> str:
        return f"<Time_Entry from {self.from_time} to {self.to_time}"
