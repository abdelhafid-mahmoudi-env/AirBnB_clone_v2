#!/usr/bin/python3
"""
This script initializes a Flask web application.
"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """
    Route: '/'
    Displays 'Hello HBNB!' when accessing the root URL.
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Route: '/hbnb'
    Displays 'HBNB' when accessing the /hbnb URL.
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """
    Route: '/c/<text>'
    Displays 'C ' followed by the value of the text variable.
    Replaces underscores (_) with spaces in the text.
    """
    return "C {}".format(text.replace("_", " "))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
