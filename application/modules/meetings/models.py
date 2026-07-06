from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from application import db


class Meeting(db.Model):
    __tablename__ = "meeting"

    meeting_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    meeting_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    minutes: Mapped[str] = mapped_column(String(), nullable=False)
