from flask import Blueprint, render_template
from flask.typing import ResponseReturnValue

from application import ClearanceEnum
from application.modules.accounts.requires_clearance import requires_clearance

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
    """
    todo:
    Needs to be able to accept params for:
    - order by (date, category, description, income, expense)
    - start
    - end
    - search
    - category
    and return that in a way that the front end can generate URLs that preserve these params.
    """
    return render_template("finances/ledger.html")
