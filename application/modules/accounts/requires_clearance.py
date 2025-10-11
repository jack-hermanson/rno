from collections.abc import Callable
from functools import wraps
from http import HTTPStatus

from flask import abort, redirect, request, url_for
from flask_login import current_user

from application import ClearanceEnum, logger


def requires_clearance(minimum_clearance: ClearanceEnum) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapped(*args, **kwargs) -> Callable:
            if not current_user.is_authenticated:
                logger.warning(
                    f"Anonymous user tried to access {request.path}\nUser-agent: {request.headers.get('User-Agent')}"
                )
                return redirect(url_for("accounts.login", next=request.path))
            if not current_user.clearance >= minimum_clearance:
                logger.warning(f"<{current_user.username}, {current_user.account_id}> tried to access {request.path}")
                return abort(HTTPStatus.FORBIDDEN)
            return func(*args, **kwargs)

        return wrapped

    return decorator
