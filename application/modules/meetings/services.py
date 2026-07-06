from application.modules.meetings.models import Meeting


def get_meetings() -> list[Meeting]:
    return Meeting.query.order_by(Meeting.meeting_datetime.desc()).all()
