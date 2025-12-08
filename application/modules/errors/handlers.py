import traceback

from flask import Blueprint, current_app, render_template
from flask.typing import ResponseReturnValue
from werkzeug.exceptions import HTTPException

from application import logger

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(Exception)
def handle_http_exception(e: Exception) -> ResponseReturnValue:
    logger.debug("AN ERROR OCCURRED")
    logger.error(traceback.format_exc())

    if current_app.debug:  # If debugging, re-raise the error to let Flask handle it
        raise e

    status = 500
    if isinstance(e, HTTPException):
        status = e.code

    return render_template("errors/generic-error.html", status=status, error=str(e)), status
