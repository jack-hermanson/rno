import dataclasses
from datetime import date
from decimal import Decimal

from application.modules.finances.ledger.ledger_item_type_enum import LedgerItemTypeEnum


@dataclasses.dataclass
class LedgerItemViewModel:
    ledger_item_id: int
    ledger_item_date: date
    ledger_item_type: LedgerItemTypeEnum
    amount: Decimal
    description: str
    balance: Decimal


@dataclasses.dataclass
class LedgerViewModel:
    start: date
    end: date
    total_income: Decimal
    total_expense: Decimal
    ending_balance: Decimal
    ledger_items: list[LedgerItemViewModel]
    order: str
    order_by: str
