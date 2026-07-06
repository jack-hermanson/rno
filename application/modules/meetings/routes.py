from flask import Blueprint, render_template
from flask.typing import ResponseReturnValue

from application.modules.meetings.services import get_meetings

meetings = Blueprint("meetings", __name__, url_prefix="/meetings")


@meetings.route("/")
def index() -> ResponseReturnValue:
    meetings_list = get_meetings()
    return render_template("meetings/index.html", meetings_list=meetings_list)
