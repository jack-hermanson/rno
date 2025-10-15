from datetime import datetime

from flask import Blueprint, render_template, request
from flask.typing import ResponseReturnValue

from application import ClearanceEnum
from application.modules.accounts.requires_clearance import requires_clearance
from application.modules.finances.services import get_ledger
from application.utils.date_time import LOCAL_TIMEZONE

finances = Blueprint("finances", __name__, url_prefix="/finances")


@finances.route("/")
def index() -> ResponseReturnValue:
    return render_template("finances/index.html")


@finances.route("/add", methods=["GET", "POST"])
@requires_clearance(ClearanceEnum.ADMIN)
def add() -> ResponseReturnValue:
    return ""


@finances.route("/ledger")
def ledger() -> ResponseReturnValue:
    start = request.args.get("start") or datetime.now(tz=LOCAL_TIMEZONE).date().replace(day=1)
    end = request.args.get("end") or datetime.now(tz=LOCAL_TIMEZONE).date()

    ledger_data = get_ledger(start, end)
    return render_template("finances/ledger.html", ledger_data=ledger_data)
