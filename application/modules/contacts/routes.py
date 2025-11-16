from flask import Blueprint, render_template
from flask.typing import ResponseReturnValue

from application import ClearanceEnum
from application.modules.accounts.requires_clearance import requires_clearance

contacts = Blueprint("contacts", __name__, url_prefix="/contacts")


@contacts.route("/")
@requires_clearance(ClearanceEnum.NORMAL)
def index() -> ResponseReturnValue:
    return render_template("contacts/index.html")
