from datetime import datetime
from time import perf_counter

from flask import Blueprint, Response, flash, redirect, render_template, request, url_for
from flask.typing import ResponseReturnValue

from application import ClearanceEnum, CrudEnum
from application.modules.accounts.requires_clearance import requires_clearance
from application.modules.finances.dashboard.services import get_dashboard_data
from application.modules.finances.ledger.forms import CreateEditLedgerItemForm
from application.modules.finances.ledger.services import (
    create_ledger_item,
    edit_ledger_item,
    get_ledger,
    ledger_items_to_csv,
    prefill_edit_ledger_item_form_values,
)
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


@finances.route("/ledger/create", methods=["GET", "POST"])
@requires_clearance(ClearanceEnum.OFFICER)
def create() -> ResponseReturnValue:
    form = CreateEditLedgerItemForm()
    if form.validate_on_submit():
        create_ledger_item(form)
        flash("Ledger item created successfully.", "success")
        return redirect(url_for("finances.ledger"))
    return render_template(
        "finances/create-edit-ledger-item.html",
        mode=CrudEnum.CREATE,
        form=form,
    )


@finances.route("/ledger/edit/<int:ledger_item_id>", methods=["GET", "POST"])
@requires_clearance(ClearanceEnum.OFFICER)
def edit(ledger_item_id: int) -> ResponseReturnValue:
    form = CreateEditLedgerItemForm()
    if form.validate_on_submit():
        edit_ledger_item(form)
        flash("Ledger item edited successfully.", "success")

        # Parse out args to keep same filtering we started with on the index page so they're not like "uh where'd it go"
        # unless they change the date then I can't help you.
        start = request.args.get("start") or datetime.now(tz=LOCAL_TIMEZONE).date().replace(day=1)
        end = request.args.get("end") or datetime.now(tz=LOCAL_TIMEZONE).date()
        order = request.args.get("order") or "asc"
        order_by = request.args.get("order_by") or "date"

        return redirect(url_for("finances.ledger", start=start, end=end, order=order, order_by=order_by))
    if request.method == "GET":
        # first time, so prefill
        prefill_edit_ledger_item_form_values(form, ledger_item_id)
    return render_template(
        "finances/create-edit-ledger-item.html",
        ledger_item_id=ledger_item_id,
        mode=CrudEnum.EDIT,
        form=form,
    )


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
