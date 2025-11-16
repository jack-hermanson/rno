import time
from datetime import datetime, timedelta

import pytz
from flask import flash
from flask_login import current_user, login_user
from sqlalchemy import func, or_

from application import bcrypt, db
from application.modules.accounts.clearance import ClearanceEnum
from application.modules.accounts.forms import CreateAccountForm, LoginForm
from application.modules.accounts.models import Account
from application.utils.date_time import utc_to_local
from logger import logger


def register(form: CreateAccountForm) -> Account:
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
    account = Account()
    account.email = form.email.data  # todo verify .lower() and .strip() are happening
    account.password = hashed_password
    account.clearance = ClearanceEnum.UNVERIFIED
    account.name = form.name.data  # todo verify .lower() and .strip() are happening
    db.session.add(account)
    db.session.commit()
    return account


def log_user_in(form: LoginForm) -> bool:
    account: Account = Account.query.filter(
        or_(
            func.lower(Account.email) == func.lower(form.email.data),
        ),
    ).first()
    if account and bcrypt.check_password_hash(account.password, form.password.data):
        login_user(account, remember=True, duration=timedelta(days=99))
        last_login: datetime | None = account.last_login
        formatted_last_login = (
            utc_to_local(last_login).strftime("%A, %D at %l:%M %p") if account.last_login is not None else "never"
        )
        flash(f"Welcome back, {account.name}. Your last login was {formatted_last_login}.", "info")
        current_user.last_login = datetime.now(tz=pytz.utc)
        db.session.commit()
        return True
    time.sleep(0.5)  # prevent spamming
    if account:
        logger.warning(f"Incorrect password for {form.email.data}")
    else:
        logger.warning(f"Incorrect email or password {form.email.data}")
    flash("Incorrect username/email or password.", "danger")
    return False
