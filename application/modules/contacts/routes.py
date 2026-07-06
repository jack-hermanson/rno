from flask import Blueprint, render_template
from flask.typing import ResponseReturnValue

from application import ClearanceEnum
from application.modules.accounts.requires_clearance import requires_clearance
from application.modules.contacts.services import get_contacts

contacts = Blueprint("contacts", __name__, url_prefix="/contacts")


@contacts.route("/")
@requires_clearance(ClearanceEnum.NORMAL)
def index() -> ResponseReturnValue:
    contacts_list = get_contacts()
    return render_template("contacts/index.html", contacts_list=contacts_list)
