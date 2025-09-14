from flask import Blueprint
from flask.typing import ResponseReturnValue

from logger import logger

main = Blueprint("main", __name__, url_prefix="")


@main.route("/")
def index() -> ResponseReturnValue:
    logger.debug("we have reached the index")
    return """
            <html>
                <head>
                    <title>Home</title>
                    <style>
                    body {
                        font-family: sans-serif;
                        color: #aaa;
                        background-color: #222;
                        padding-left: 10vw;
                        padding-right: 10vw;
                    }
                    h1 {
                        border-bottom: 1px solid #aaa;
                    }
                    </style>
                </head>
                <body>
                    <h1>Home</h1>
                    <p>Hi there.</p>
                </body>
            </html>
            """
