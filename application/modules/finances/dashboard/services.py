from datetime import date, datetime

from application.modules.finances.common.total_income_and_expense import get_total_income_and_expense
from application.modules.finances.dashboard.view_models import DashboardViewModel, RecentTransactionViewModel
from application.modules.finances.models import LedgerItem
from application.utils.date_time import LOCAL_TIMEZONE


def get_dashboard_data() -> DashboardViewModel:
    # Recent transactions (really just ledger items)
    recent_transactions = _get_recent_transactions()

    # Current balance
    total_income_and_expense = get_total_income_and_expense(
        start=date(1900, 1, 1),
        end=datetime.now(tz=LOCAL_TIMEZONE).date(),
    )
    current_balance = total_income_and_expense.total_income - total_income_and_expense.total_expense

    return DashboardViewModel(
        recent_transactions=recent_transactions,
        recent_audit_log_entries=[],
        current_balance=current_balance,
    )


def _get_recent_transactions() -> list[RecentTransactionViewModel]:
    ledger_items: list[LedgerItem] = (
        LedgerItem.query.order_by(LedgerItem.ledger_item_date.desc(), LedgerItem.ledger_item_id.desc()).limit(3).all()
    )

    return [
        RecentTransactionViewModel(
            ledger_item_id=ledger_item.ledger_item_id,
            amount=ledger_item.amount,
            ledger_item_type=ledger_item.ledger_item_type,
            description=ledger_item.description,
            ledger_item_date=ledger_item.ledger_item_date,
        )
        for ledger_item in ledger_items
    ]
