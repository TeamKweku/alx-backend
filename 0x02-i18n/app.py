#!/usr/bin/env python3
"""
module that implements a basic flask app
"""

import pytz
from flask import Flask, render_template, request, g
from flask_babel import Babel


class Config:
    """
    Flask babel configuration class
    """

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)


app.config.from_object(Config)

app.url_map.strict_slashes = False

babel = Babel(app)

# Mock user table
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """
    Retrieves a user based on the user id
    """
    login_id = request.args.get("login_as")
    print(login_id)
    if login_id:
        # print(users.get(int(login_id)))
        return users.get(int(login_id))
    return None


@app.before_request
def before_request():
    """
    check routines before request is resolved
    """
    user = get_user()
    g.user = user
    # print(g.user)


@babel.localeselector
def get_locale():
    """
    function that selects the default locale for the app
    based users url
    """
    queries = request.query_string.decode("utf-8").split("&")
    query_table = dict(
        map(
            lambda x: (x if "=" in x else "{}=".format(x)).split("="),
            queries,
        )
    )
    locale = query_table.get("locale")

    if locale in app.config["LANGUAGES"]:
        return locale

    user_details = getattr(g, "user", None)

    if user_details and user_details["locale"] in app.config["LANGUAGES"]:
        return user_details["locale"]

    header_locale = request.headers.get("locale")
    if header_locale in app.config["LANGUAGES"]:
        return header_locale

    return app.config["BABEL_DEFAULT_LOCALE"]


@babel.timezoneselector
def get_timezone():
    """
    method that sets the prefered timezone of the user
    """
    timezone = request.args.get("timezone")
    if not timezone and g.user:
        timezone = g.user["timezone"]
    try:
        return pytz.timezone(timezone).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config["BABEL_DEFAULT_TIMEZONE"]


@app.route("/")
def index():
    """
    index page
    """
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
