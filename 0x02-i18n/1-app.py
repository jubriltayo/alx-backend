#!/usr/bin/env python3
"""This module sets up a flask app"""
from flask import Flask, render_template
from flask_babel import Babel


class Config():
    """defines different languages"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
babel = Babel(app)
app.config.from_object(Config)


@app.route("/")
def home():
    """renders index page"""
    return render_template("1-index.html")


if __name__ == "__main__":
    app.run()
