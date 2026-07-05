from flask import Blueprint, render_template
from flask.typing import ResponseReturnValue

bylaws = Blueprint("bylaws", __name__, url_prefix="/bylaws")


@bylaws.route("/")
def index() -> ResponseReturnValue:
    return render_template("bylaws/index.html")
