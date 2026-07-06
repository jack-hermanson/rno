import logging
import os
import subprocess
from datetime import date, datetime

from flask import Flask, request
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from application.modules.accounts.clearance import ClearanceEnum
from application.modules.finances.ledger.ledger_item_category_enum import LedgerItemCategoryEnum
from application.modules.finances.ledger.ledger_item_type_enum import LedgerItemTypeEnum
from application.utils import date_time
from application.utils.crud_enum import CrudEnum

# from application.modules.accounts.clearance_enum import ClearanceEnum
# from application.utils.crud_enum import CrudEnum
from application.utils.get_ip import get_ip

# from application.utils.ledger_item_type_enum import LedgerItemTypeEnum
from Config import Config
from logger import logger

bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate(compare_type=True)
logging.basicConfig(level=logging.DEBUG)

login_manager = LoginManager()
login_manager.login_view = "accounts.login"
login_manager.login_message_category = "warning"


def create_app(config_class: type[Config] = Config) -> Flask:
    # create app, set static stuff up
    app = Flask(__name__, static_url_path="/static", static_folder="web/static", template_folder="web/templates")

    # set up environment variables
    app.config.from_object(config_class)

    # bcrypt
    bcrypt.init_app(app)

    # models
    import application.modules.accounts.models  # noqa: PLC0415
    import application.modules.contacts.models  # noqa: PLC0415
    import application.modules.finances.models  # noqa: PLC0415
    import application.modules.meetings.models  # noqa: PLC0415, F401

    # database
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)

    # Don't worry about trailing slashes
    app.url_map.strict_slashes = False

    # routes and blueprints
    # from application.modules.about.routes import about
    from application.modules.accounts.routes import accounts  # noqa: PLC0415
    from application.modules.bylaws.routes import bylaws  # noqa: PLC0415
    from application.modules.contacts.routes import contacts  # noqa: PLC0415
    from application.modules.finances.routes import finances  # noqa: PLC0415
    from application.modules.main.routes import main  # noqa: PLC0415
    from application.modules.meetings.routes import meetings  # noqa: PLC0415

    # from application.modules.help.routes import help
    # from application.modules.ledger.routes import ledger
    # from application.modules.schedule.routes import schedule
    # from application.modules.support.routes import support
    #
    from .modules.errors.handlers import errors  # noqa: PLC0415

    for blueprint in [main, accounts, finances, contacts, errors, bylaws, meetings]:
        app.register_blueprint(blueprint)

    # login manager
    login_manager.init_app(app)

    # template filters / context processors / pre-request stuff
    @app.context_processor
    def inject_environment() -> dict:
        return {
            "commit": subprocess.check_output(["git", "describe", "--always"]).strip().decode("utf-8"),
            "environment": os.environ.get("ENVIRONMENT"),
            "rno_name": os.environ.get("RNO_NAME"),
            "ClearanceEnum": ClearanceEnum,
            "CrudEnum": CrudEnum,
            "LedgerItemTypeEnum": LedgerItemTypeEnum,
            "LedgerItemCategoryEnum": LedgerItemCategoryEnum,
        }

    @app.before_request
    def before_request() -> None:
        excluded_paths = ["/static"]
        request_path = request.path.lower()
        if not any(request_path.startswith(path) for path in excluded_paths):
            logger.debug(
                f"[<{f'{current_user.name}, {current_user.account_id}' if current_user.is_authenticated else 'anon'}> - {get_ip(request)}] "
                f"{request.method}: {request.path} ",
            )

    @app.template_filter()
    def to_short_date_string(d: date) -> str:
        return date_time.to_short_date_string(d)

    @app.template_filter()
    def utc_to_local(utc_datetime: datetime) -> date:
        return date_time.utc_to_local(utc_datetime)

    @app.template_filter()
    def to_short_time_string(d: datetime) -> str:
        return date_time.to_short_time_string(d)

    logger.info(f"APPLICATION RUNNING, probably at http://localhost:{config_class.PORT}")
    flask_debug = bool(int(os.environ.get("FLASK_DEBUG", "0")))
    logger.info(f"FLASK_DEBUG: '{flask_debug}'")

    return app
