from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from application import db
from application.utils.date_time import utcnow


class Contact(db.Model):
    __tablename__ = "contact"

    contact_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    phone_number: Mapped[str] = mapped_column(String(10), nullable=True)
    email: Mapped[str] = mapped_column(String(50), nullable=True)
    first_name: Mapped[str] = mapped_column(String(25), nullable=True)
    last_name: Mapped[str] = mapped_column(String(25), nullable=True)
    company: Mapped[str] = mapped_column(String(50), nullable=True)
    notes: Mapped[str] = mapped_column(String(255), nullable=True)
    created_datetime_utc: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=utcnow)
