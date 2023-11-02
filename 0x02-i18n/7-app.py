#!/usr/bin/env python3
"""This module sets up a flask app"""
from flask import Flask, render_template, request, g
from flask_babel import Babel
import pytz


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config():
    """defines different languages"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
babel = Babel(app)
app.config.from_object(Config)
app.url_map.strict_slashes = False


@babel.localeselector
def get_locale() -> str:
    """select best match from languages"""

    locale = request.args.get("locale")
    if locale and locale in app.config["LANGUAGES"]:
        return locale

    if g.user and g.user["locale"] in app.config["LANGUAGES"]:
        return g.user["locale"]

    header_locale = request.headers.get("locale", "")
    if header_locale in app.config["LANGUAGES"]:
        return header_locale

    return request.accept_languages.best_match(app.config["LANGUAGES"])


@babel.timezoneselector
def get_timezone():
    """returns timezone for the request"""

    timezone = request.args.get("timezone")
    if timezone and timezone in app.config["LANGUAGES"]:
        return timezone

    if g.user and g.user["timezone"] in app.config["LANGUAGES"]:
        return g.user["timezone"]

    try:
        return pytz.timezone(timezone).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return Config.BABEL_DEFAULT_TIMEZONE

def get_user(user_id):
    """get user from mock database"""
    return users.get(user_id)


@app.before_request
def before_request():
    """before request function"""
    user_id = request.args.get("login_as")
    g.user = get_user(int(user_id)) if user_id else None


@app.route("/")
def home() -> str:
    """renders index page"""
    return render_template("7-index.html")


if __name__ == "__main__":
    app.run()
