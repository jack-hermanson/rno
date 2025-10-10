from __future__ import annotations

import time

from flask_login import current_user
from flask_wtf import FlaskForm
from sqlalchemy import and_, func
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, ValidationError

from application.modules.accounts.models import Account
from application.utils.form_filters import lowercase
from logger import logger

name_length = Length(min=2, max=32)
password_length = Length(min=2, max=32)
EMAIL_MAX = 42
email_length = Length(min=5, max=EMAIL_MAX)


class CreateOrEditAccountFormBase(FlaskForm):
    """Just the base - inherit this in create and edit"""

    name = StringField(
        "Name",
        validators=[DataRequired(), name_length],
        render_kw={
            "autofocus": "true",
            "autocorrect": "off",
        },
        description="Your full name, or whatever you want to enter; it's up to you.",
    )
    email = StringField(
        "Email",
        validators=[Email(), email_length],
        filters=[lowercase],
        render_kw={
            "spellcheck": "false",
            # "autocorrect": "off",
            "autocapitalize": "off",
        },
        description="Your email address to be used for logging in, notifications, and password resets.",
    )


class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[Email()],
        filters=[lowercase],
        render_kw={
            "autofocus": "true",
            "spellcheck": "false",
            # "autocorrect": "off",
            "autocapitalize": "off",
        },
        description="The email address you used when signing up.",
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), password_length],
        description="The password you used when signing up, ideally saved in a secure password manager.",
    )
    # remember = BooleanField("Remember Me", default=True)
    submit = SubmitField("Log In")

    @staticmethod
    def validate_email(_: LoginForm, email: StringField) -> None:
        if not Account.query.filter(func.lower(Account.email) == email.data).count():
            logger.warning(f"{email.data} does not match an existing email address.")
            time.sleep(0.5)  # prevent spamming
            raise ValidationError("That email address hasn't been registered.")

    # @staticmethod
    # def validate_username(_, username):
    #     if not Account.query.filter(func.lower(Account.username) == func.lower(username.data)).count():
    #         raise ValidationError("Doesn't exist.")


class CreateAccountForm(CreateOrEditAccountFormBase):
    password = PasswordField(
        "Password",
        validators=[DataRequired(), password_length],
        description="You should use a password manager, or pick something secure that you can remember.",
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), password_length, EqualTo("password", "Your passwords must match.")],
        description="Type in your password again to confirm it's correct.",
    )
    submit = SubmitField("Create Account")

    @staticmethod
    def validate_email(_: CreateAccountForm, email: StringField) -> None:
        if Account.query.filter(func.lower(Account.email) == email.data).all():
            raise ValidationError("That email has already been used.")


class EditAccountForm(CreateOrEditAccountFormBase):
    password = PasswordField(
        "Password",
        validators=[Optional(), password_length],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[EqualTo("password", "Your passwords must match.")],
        description="Type in your password again to confirm it's correct.",
    )
    submit = SubmitField("Save Changes")

    @staticmethod
    def validate_username(_: EditAccountForm, username: StringField) -> None:
        # Check if it already exists.
        if Account.query.filter(
            and_(
                func.lower(Account.username) == func.lower(username.data),  # Has same username, and...
                Account.account_id != current_user.account_id,  # has same account id.
            ),
        ).all():
            raise ValidationError("That username has already been taken.")

    @staticmethod
    def validate_email(_: EditAccountForm, email: StringField) -> None:
        if Account.query.filter(
            and_(
                func.lower(Account.email) == func.lower(email.data),  # Has same email, and...
                Account.account_id != current_user.account_id,  # has same account id.
            ),
        ).all():
            raise ValidationError("That email has already been used.")
