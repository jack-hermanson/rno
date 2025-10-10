from flask import Blueprint, render_template
from flask.typing import ResponseReturnValue

from logger import logger

main = Blueprint("main", __name__, url_prefix="")


@main.route("/")
def index() -> ResponseReturnValue:
    logger.debug("we have reached the index")
    return render_template("main/index.html")
