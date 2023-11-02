#!/usr/bin/env python3
"""This module sets up a flask app"""
from flask import Flask, render_template, request, g
from flask_babel import Babel
from datetime import datetime
from pytz import timezone
import pytz.exceptions
import locale


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

    # locale from URL parameters
    locale = request.args.get("locale")
    if locale and locale in app.config["LANGUAGES"]:
        return locale

    # locale from user settings
    if g.user and g.user["locale"] in app.config["LANGUAGES"]:
        return g.user["locale"]

    # locale from request headers
    header_locale = request.headers.get("locale", "")
    if header_locale in app.config["LANGUAGES"]:
        return header_locale

    # default locale
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@babel.timezoneselector
def get_timezone():
    """returns timezone for the request"""

    # timezone from URL parameters
    tzone = request.args.get("timezone", None)
    if tzone:
        try:
            return timezone(tzone).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    # timezone from user settings
    if g.user:
        try:
            tzone = g.user.get("timezone")
            return timezone(tzone).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    # default to UFC
    default_tz = app.config["BABEL_DEFAULT_TIMEZONE"]
    return default_tz


def get_user():
    """get user from mock database"""
    login_id = request.args.get("login_as")
    if login_id:
        return users.get(int(login_id))
    return None


@app.before_request
def before_request() -> None:
    """before request function"""
    user = get_user()
    g.user = user

    time_now = pytz.utc.localize(datetime.utcnow())
    time = time_now.astimezone(timezone(get_timezone()))
    locale.setlocale(locale.LC_TIME, (get_locale(), "UTF-8"))
    time_format = "%b, %d, %Y, %I:%M:%S %p"

    g.time = time.strftime(time_format)


@app.route("/")
def home() -> str:
    """renders index page"""
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
