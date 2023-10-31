#!/usr/bin/env python3
"""This module sets up a flask app"""
from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def home():
    """renders index page"""
    return render_template("0-index.html")


if __name__ == "__main__":
    app.run()
