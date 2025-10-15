import dataclasses
from datetime import date
from decimal import Decimal

from application import LedgerItemTypeEnum


@dataclasses.dataclass
class RecentTransactionViewModel:
    ledger_item_id: int
    amount: Decimal
    ledger_item_type: LedgerItemTypeEnum
    description: str
    ledger_item_date: date


@dataclasses.dataclass
class RecentLedgerItemAuditLogEntryViewModel:
    pass


@dataclasses.dataclass
class DashboardViewModel:
    recent_transactions: list[RecentTransactionViewModel]
    recent_audit_log_entries: list[RecentLedgerItemAuditLogEntryViewModel]
    current_balance: Decimal
