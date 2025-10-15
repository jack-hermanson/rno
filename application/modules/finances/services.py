from datetime import date
from decimal import Decimal
from time import perf_counter

from sqlalchemy import case, func, select

from application import db
from application.modules.finances.models import LedgerItem
from application.modules.finances.view_models import LedgerItemViewModel, LedgerViewModel
from logger import logger


def get_ledger(start: date, end: date) -> LedgerViewModel:
    # Step 1: running total over all ledger items
    big_query_started = perf_counter()
    ledger_with_balance = select(
        LedgerItem.ledger_item_id,
        LedgerItem.ledger_item_date,
        LedgerItem.ledger_item_type,
        LedgerItem.amount,
        LedgerItem.description,
        func.sum(
            case(
                (LedgerItem.ledger_item_type == 1, LedgerItem.amount),
                (LedgerItem.ledger_item_type == -1, -LedgerItem.amount),
                else_=0,
            ),
        )
        .over(order_by=[LedgerItem.ledger_item_date, LedgerItem.ledger_item_id])
        .label("balance"),
    ).cte("ledger_with_balance")
    big_query_ended = perf_counter()
    logger.debug(f"Completed big query in {(big_query_ended - big_query_started):.6f} seconds")

    # Step 2: filter to only the date range for display
    filter_query_started = perf_counter()
    stmt = (
        select(ledger_with_balance)
        .where(ledger_with_balance.c.ledger_item_date.between(start, end))
        .order_by(ledger_with_balance.c.ledger_item_date, ledger_with_balance.c.ledger_item_id)
    )
    filter_query_ended = perf_counter()
    logger.debug(f"Completed filter query in {(filter_query_ended - filter_query_started):.6f} seconds")

    # Map to view model
    view_model_map_started = perf_counter()
    ordered_ledger_items = [LedgerItemViewModel(**row) for row in db.session.execute(stmt).mappings()]
    view_model_map_ended = perf_counter()
    logger.debug(f"Completed view model map in {(view_model_map_ended - view_model_map_started):.6f} seconds")

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

    # Put into a result for front end to consume.
    return LedgerViewModel(
        start=start,
        end=end,
        total_income=total_income,
        total_expense=total_expense,
        ending_balance=(ordered_ledger_items[-1].balance if len(ordered_ledger_items) > 0 else Decimal(0)),
        ledger_items=ordered_ledger_items,
    )
