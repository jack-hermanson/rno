from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application import db
from application.modules.finances.ledger_item_category_enum import LedgerItemCategoryEnum
from application.modules.finances.ledger_item_type_enum import LedgerItemTypeEnum
from application.utils.date_time import utcnow

if TYPE_CHECKING:
    from application.modules.accounts.models import Account


class LedgerItem(db.Model):
    __tablename__ = "ledger_item"

    ledger_item_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ledger_item_type: Mapped[LedgerItemTypeEnum] = mapped_column(Integer, nullable=False)
    ledger_item_date: Mapped[date] = mapped_column(Date, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    created_datetime_utc: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utcnow,
    )

    # Protected notes that shouldn't be shown to the public, for personal details like name/address
    private_notes: Mapped[str] = mapped_column(String(255), nullable=False)

    # Hardcoded category enum
    category: Mapped[LedgerItemCategoryEnum] = mapped_column(Integer, nullable=True)

    # Foreign key
    created_by_account_id: Mapped[int] = mapped_column(ForeignKey("account.account_id"), nullable=False)

    # Relationship back to Account
    account: Mapped["Account"] = relationship(back_populates="ledger_items")
