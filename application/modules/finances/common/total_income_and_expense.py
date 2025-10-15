import dataclasses
from datetime import date
from decimal import Decimal
from time import perf_counter

from sqlalchemy import case, func, select

from application import db, logger
from application.modules.finances.models import LedgerItem


@dataclasses.dataclass(frozen=True)
class TotalIncomeAndExpense:
    total_income: Decimal
    total_expense: Decimal


def get_total_income_and_expense(start: date, end: date) -> TotalIncomeAndExpense:
    # Get totals.
    totals_query_started = perf_counter()
    totals = (
        db.session.execute(
            select(
                func.sum(case((LedgerItem.ledger_item_type == 1, LedgerItem.amount), else_=Decimal(0))).label(
                    "total_income",
                ),
                func.sum(case((LedgerItem.ledger_item_type == -1, LedgerItem.amount), else_=Decimal(0))).label(
                    "total_expense",
                ),
            ).where(LedgerItem.ledger_item_date.between(start, end)),
        )
        .mappings()
        .one()
    )
    totals_query_ended = perf_counter()
    logger.debug(f"Completed totals query in {(totals_query_ended - totals_query_started):.6f} seconds")

    total_income = totals["total_income"] or Decimal(0)
    total_expense = totals["total_expense"] or Decimal(0)

    return TotalIncomeAndExpense(
        total_income=total_income,
        total_expense=total_expense,
    )
