#!/usr/bin/python3
"""
Starts a Flask web application.
"""

from flask import Flask, render_template

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


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """
    Displays "<n> is a number" if n is an integer.
    """
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """
    Displays an HTML page with "Number: n" if n is an integer.
    """
    return render_template('6-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """
    Displays an HTML page with "Number: n is even|odd" if n is an integer.
    """
    return render_template('6-number_odd_or_even.html', n=n, even_or_odd=('even' if n % 2 == 0 else 'odd'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
