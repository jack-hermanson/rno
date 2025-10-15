from datetime import datetime
from time import perf_counter

from flask import Blueprint, Response, render_template, request
from flask.typing import ResponseReturnValue

from application import ClearanceEnum
from application.modules.accounts.requires_clearance import requires_clearance
from application.modules.finances.dashboard.services import get_dashboard_data
from application.modules.finances.ledger.services import get_ledger, ledger_items_to_csv
from application.utils.date_time import LOCAL_TIMEZONE
from logger import logger

finances = Blueprint("finances", __name__, url_prefix="/finances")


@finances.route("/")
def index() -> ResponseReturnValue:
    dashboard_data = get_dashboard_data()
    return render_template(
        "finances/index.html",
        dashboard_data=dashboard_data,
    )


@finances.route("/add", methods=["GET", "POST"])
@requires_clearance(ClearanceEnum.ADMIN)
def add() -> ResponseReturnValue:
    return ""


@finances.route("/ledger")
def ledger() -> ResponseReturnValue:
    perf_start = perf_counter()

    # Parse out args.
    start = request.args.get("start") or datetime.now(tz=LOCAL_TIMEZONE).date().replace(day=1)
    end = request.args.get("end") or datetime.now(tz=LOCAL_TIMEZONE).date()
    order = request.args.get("order") or "asc"
    order_by = request.args.get("order_by") or "date"

    # Get data from db.
    ledger_data = get_ledger(start, end, order, order_by)

    # Check timing
    perf_end = perf_counter()
    logger.debug(f"Ledger completed in {(perf_end - perf_start):.6f} seconds")

    # CSV stuff if requested.
    if (request.args.get("csv") or "").lower() == "true":
        csv_str = ledger_items_to_csv(ledger_data.ledger_items)
        download = (request.args.get("download") or "").lower() == "true"
        return Response(csv_str, mimetype="text/csv" if download else "text/plain")

    # Done.
    return render_template("finances/ledger.html", ledger_data=ledger_data)


# @finances.route("/")
