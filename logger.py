import logging
import os
import sys
from logging import LogRecord
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import ClassVar


class StaticURLFilter(logging.Filter):
    def filter(self, record: LogRecord) -> bool:
        return not record.getMessage().__contains__("GET /static")


class StreamLogFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    cyan = "\033[96m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    # format = f"%(levelname)-8s [%(asctime)s]: %(message)s  {reset}{grey}%(filename)s:%(lineno)d %(name)s"
    format_string = (
        f"%(levelname)-8s {reset}{grey}%(filename)s:%(lineno)d{reset} [%(asctime)s]: %(message)s{reset}{grey}"
    )

    FORMATS: ClassVar[dict[int, str]] = {
        logging.DEBUG: grey + format_string + reset,
        logging.INFO: cyan + format_string + reset,
        logging.WARNING: yellow + format_string + reset,
        logging.ERROR: red + format_string + reset,
        logging.CRITICAL: bold_red + format_string + reset,
    }

    def format(self, record: LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, "%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


class FileLogFormatter(logging.Formatter):
    # format_string = f"%(levelname)-8s [%(asctime)s]: %(message)s  %(fxilename)s:%(lineno)d %(name)s"
    format_string = "%(levelname)-8s [%(asctime)s]: %(message)s - %(filename)s:%(lineno)d "

    FORMATS: ClassVar[dict[int, str]] = {
        logging.DEBUG: format_string,
        logging.INFO: format_string,
        logging.WARNING: format_string,
        logging.ERROR: format_string,
        logging.CRITICAL: format_string,
    }

    def format(self, record: LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, "%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


# Set up logging
environment = os.environ.get("ENVIRONMENT")
logging.basicConfig()
logger = logging.getLogger("app")
logger.propagate = False
sh = logging.StreamHandler(sys.stdout)
sh.setFormatter(StreamLogFormatter())

log_dir = "logs"
logs_path = Path(log_dir)
if not logs_path.exists():
    logs_path.mkdir(parents=True, exist_ok=True)

fh = TimedRotatingFileHandler((logs_path / "logs.txt"), when="midnight", interval=1, backupCount=7)
fh.setFormatter(FileLogFormatter())
fh.suffix += ".txt"
fh.namer = lambda name: name.replace(".txt", "") + ".txt"

logger.addHandler(fh)
logger.addHandler(sh)
log_level = getattr(logging, os.environ.get("LOG_LEVEL", "INFO"))
logger.setLevel(log_level)

# SQL Alchemy
logging.getLogger("sqlalchemy.engine").setLevel(
    logging.INFO if bool(int(os.environ.get("SQLALCHEMY_ECHO", "0"))) else logging.WARNING,
)
logging.getLogger("sqlalchemy.engine").addHandler(fh)
logging.getLogger("sqlalchemy.engine").addHandler(fh)
logging.getLogger("sqlalchemy.engine").propagate = False

# Werkzeug
werkzeug_log_level = logging.WARNING  # if environment == "production" else logging.INFO
logging.getLogger("werkzeug").setLevel(werkzeug_log_level)
logging.getLogger("werkzeug").addFilter(StaticURLFilter())
logging.getLogger("werkzeug").addHandler(fh)
logging.getLogger("werkzeug").addHandler(sh)
logging.getLogger("werkzeug").propagate = False
