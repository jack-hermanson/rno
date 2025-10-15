import csv
import io
from datetime import date
from decimal import Decimal
from time import perf_counter

from sqlalchemy import case, desc, func, select

from application import LedgerItemTypeEnum, db
from application.modules.finances.common.total_income_and_expense import get_total_income_and_expense
from application.modules.finances.ledger.view_models import LedgerItemViewModel, LedgerViewModel
from application.modules.finances.models import LedgerItem
from logger import logger


def get_ledger(start: date, end: date, order: str, order_by: str) -> LedgerViewModel:
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
    mapped_ledger_items = db.session.execute(
        select(ledger_with_balance)
        .where(ledger_with_balance.c.ledger_item_date.between(start, end))
        # .order_by(ledger_with_balance.c.ledger_item_date, ledger_with_balance.c.ledger_item_id)
        .order_by(
            ledger_with_balance.c.ledger_item_date
            if order == "asc" and order_by == "date"
            else desc(ledger_with_balance.c.ledger_item_date)
            if order == "desc" and order_by == "date"
            else ledger_with_balance.c.ledger_item_id
            if order == "asc" and order_by == "id"
            else desc(ledger_with_balance.c.ledger_item_id),
            # desc(ledger_with_balance.c.ledger_item_date)
        ),
    ).mappings()
    filter_query_ended = perf_counter()
    logger.debug(f"Completed filter query in {(filter_query_ended - filter_query_started):.6f} seconds")

    # Map to view model
    view_model_map_started = perf_counter()
    ordered_ledger_items = [LedgerItemViewModel(**row) for row in mapped_ledger_items]
    view_model_map_ended = perf_counter()
    logger.debug(f"Completed view model map in {(view_model_map_ended - view_model_map_started):.6f} seconds")

    # Get totals.
    total_income_and_expense = get_total_income_and_expense(start, end)

    # Put into a result for front end to consume.
    return LedgerViewModel(
        start=start,
        end=end,
        total_income=total_income_and_expense.total_income,
        total_expense=total_income_and_expense.total_expense,
        ending_balance=(ordered_ledger_items[-1].balance if len(ordered_ledger_items) > 0 else Decimal(0)),
        ledger_items=ordered_ledger_items,
        order=order,
        order_by=order_by,
    )


def ledger_items_to_csv(ledger_items: list[LedgerItemViewModel]) -> str:
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_ALL)

    headers = ["id", "date", "description", "income", "expense", "balance"]
    writer.writerow(headers)

    for row in ledger_items:
        data = [
            f"{row.ledger_item_id}",
            row.ledger_item_date.strftime("%-m/%-d/%y"),
            row.description,
            f"{row.amount:.2f}" if row.ledger_item_type == LedgerItemTypeEnum.INCOME else "",
            f"{row.amount:.2f}" if row.ledger_item_type == LedgerItemTypeEnum.EXPENSE else "",
            f"{row.balance:.2f}" if row.balance else "",
        ]
        writer.writerow(data)
    return output.getvalue()
