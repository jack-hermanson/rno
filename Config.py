import os
from typing import ClassVar

from dotenv import load_dotenv

load_dotenv()


class Config:
    TEMPLATES_AUTO_RELOAD = bool(int(os.getenv("TEMPLATES_AUTO_RELOAD")))
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_ENGINE_OPTIONS: ClassVar[dict] = {"pool_pre_ping": True}
    PORT = os.getenv("PORT")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG")
    LOG_LEVEL = os.getenv("LOG_LEVEL")
    # SQLALCHEMY_ECHO = bool(int(os.getenv("SQLALCHEMY_ECHO", "0")))
