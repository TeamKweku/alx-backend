#!/usr/bin/env python3
"""
module that implements a basic flask app
"""

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
    locale = request.args.get("locale")

    if locale in app.config["LANGUAGES"]:
        return locale

    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/")
def index():
    """
    index page
    """
    return render_template("5-index.html")


if __name__ == "__main__":
    app.run(debug=True)
