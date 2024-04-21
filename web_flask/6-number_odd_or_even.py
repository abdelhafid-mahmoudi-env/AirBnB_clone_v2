#!/usr/bin/python3
"""
A script that starts a Flask web application.
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """
    Route that displays "Hello HBNB!" when accessing the root URL.
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Route that displays "HBNB" when accessing the /hbnb URL.
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """
    Route that displays "C ", followed by the value of the text variable.
    Replaces underscore _ symbols with a space.
    """
    return "C {}".format(text.replace("_", " "))


@app.route('/python/', defaults={"text": "is cool"}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text):
    """
    Route that displays "Python ", followed by the value of the text variable.
    Replaces underscore _ symbols with a space.
    Defaults to "Python is cool" if no text is provided.
    """
    return "Python {}".format(text.replace("_", " "))


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """
    Route that displays "<n> is a number" only if n is an integer.
    """
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """
    Route that displays an HTML page with "Number: n" only if n is an integer.
    """
    return render_template('6-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """
    Route that displays an HTML page with "Number: n is even|odd".
    """
    return render_template('6-number_odd_or_even.html', n=n)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
