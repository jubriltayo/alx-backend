#!/usr/bin/env python3
"""This module sets up a flask app"""
from flask import Flask, render_template, request
from flask_babel import Babel


class Config():
    """defines different languages"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
babel = Babel(app)
app.config.from_object(Config)


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/")
def home():
    """renders index page"""
    return render_template("2-index.html")


if __name__ == "__main__":
    app.run()
