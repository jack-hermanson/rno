from datetime import date

from flask_wtf import FlaskForm
from wtforms.fields import DateField, DecimalField, IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import AnyOf, DataRequired, Length, NumberRange, Optional
from wtforms.widgets.core import HiddenInput

from application import LedgerItemTypeEnum
from application.modules.finances.ledger.ledger_item_category_enum import LedgerItemCategoryEnum


class CreateOrEditLedgerItemForm(FlaskForm):
    # only for edit
    ledger_item_id = IntegerField(validators=[Optional()], widget=HiddenInput())

    ledger_item_type = SelectField(
        "Ledger Item Type",
        coerce=int,
        choices=[
            (0, "Select..."),
            (LedgerItemTypeEnum.EXPENSE, "- Expense"),
            (LedgerItemTypeEnum.INCOME, "+ Income"),
        ],
        validators=[
            AnyOf(
                [
                    LedgerItemTypeEnum.INCOME,
                    LedgerItemTypeEnum.EXPENSE,
                ],
            ),
            DataRequired(),
        ],
        default=LedgerItemTypeEnum.INCOME,
    )

    category = SelectField(
        "Category",
        coerce=int,
        choices=[
            (None, "(no category)"),
            (LedgerItemCategoryEnum.MEMBERSHIP, "Membership"),
            (LedgerItemCategoryEnum.DONATION, "Donation"),
            (LedgerItemCategoryEnum.WEBSITE_EMAIL_SUBSCRIPTION, "Website/Email Subscription"),
        ],
        validators=[Optional()],
    )

    ledger_item_date = DateField("Ledger Item Date", validators=[DataRequired()], default=date.today)
    amount = DecimalField("Amount", validators=[DataRequired(), NumberRange(min=0, max=10_000)])
    description = StringField("Description", validators=[DataRequired(), Length(min=3, max=255)])
    private_notes = StringField(
        "Private Notes",
        validators=[Optional(), Length(min=0, max=255)],
        description="If there are more sensitive details that we do not want to show to the public (like names and "
        "addresses), save them here",
    )
    submit = SubmitField("Create" if ledger_item_id is None else "Save Changes")
