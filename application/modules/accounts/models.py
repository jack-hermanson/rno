from datetime import datetime
from typing import TYPE_CHECKING

from flask_login import UserMixin
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application import db
from application.modules.accounts.clearance import ClearanceEnum

# if TYPE_CHECKING:
#     from application.modules.schedule.models import CoverageRequest, Shift, ShiftAssignment
if TYPE_CHECKING:
    from application.modules.finances.models import LedgerItem


class Account(db.Model, UserMixin):
    __tablename__ = "account"

    def get_id(self) -> int:
        return self.account_id

    account_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    email: Mapped[str] = mapped_column(String(42), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    clearance: Mapped[int] = mapped_column(Integer, default=ClearanceEnum.UNVERIFIED, nullable=False)
    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # One-to-many relationship to LedgerItem
    ledger_items: Mapped[list["LedgerItem"]] = relationship(back_populates="account", cascade="all, delete-orphan")
    #
    # # One-to-many relationship to Shift - these are like "the exact evening of Monday, June 16"
    # assigned_shifts: Mapped[list["Shift"]] = relationship(
    #     back_populates="assigned_to_account",
    #     cascade="all, delete-orphan",
    #     foreign_keys="[Shift.assigned_to_account_id]",
    # )
    #
    # # One-to-many relationship to Assignment - these are like "every Monday evening"
    # assignments: Mapped[list["ShiftAssignment"]] = relationship(
    #     back_populates="account",
    #     cascade="all, delete-orphan",
    # )
    #
    # # Coverage requests accepted by this account
    # accepted_coverage_requests: Mapped[list["CoverageRequest"]] = relationship(
    #     back_populates="covered_by_account",
    #     cascade="all, delete-orphan",
    # )
