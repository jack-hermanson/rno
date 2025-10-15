from datetime import date

from application import create_app

if __name__ == "__main__":
    start: date = date(2025, 10, 12)
    end: date = date(2025, 10, 15)
    app = create_app()
    # with app.app_context():
    #     statement = (
    #         select(
    #             LedgerItem.ledger_item_id,
    #             LedgerItem.ledger_item_date,
    #             LedgerItem.ledger_item_type,
    #             LedgerItem.amount,
    #             LedgerItem.description,
    #             func.sum(
    #                 case(
    #                     (LedgerItem.ledger_item_type == 1, LedgerItem.amount),
    #                     (LedgerItem.ledger_item_type == -1, -LedgerItem.amount),
    #                     else_=Decimal(0),
    #                 ),
    #             )
    #             .over(order_by=[LedgerItem.ledger_item_date, LedgerItem.ledger_item_id])
    #             .label("balance"),
    #         )
    #         .where(LedgerItem.ledger_item_date.between(start, end))
    #         .order_by(LedgerItem.ledger_item_date, LedgerItem.ledger_item_id)
    #     )
    #
    #     results = db.session.execute(statement).mappings().all()
    #
    #     print(results)
