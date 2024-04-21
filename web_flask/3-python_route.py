#!/usr/bin/python3
"""
Starts a Flask web application.
"""

from flask import Flask, request

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """
    Displays "Hello HBNB!" when accessing the root URL.
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Displays "HBNB" when accessing the /hbnb URL.
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """
    Displays "C ", followed by the value of the text variable.
    Replaces underscore (_) symbols with spaces in the text.
    """
    return "C {}".format(text.replace("_", " "))


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text="is cool"):
    """
    Displays "Python ", followed by the value of the text variable.
    Replaces underscore (_) symbols with spaces in the text.
    Defaults to "is cool" if no text is provided.
    """
    return "Python {}".format(text.replace("_", " "))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
