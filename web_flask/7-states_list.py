#!/usr/bin/python3
"""
Flask web application that use storage for fetching data from storage engine
"""

from flask import Flask
from flask import render_template
from models import storage
from models.state import State
from models import *
app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def states_list():
    """ displays a HTML page of states from storage"""
    states = sorted(list(storage.all("State").values()), key=lambda x: x.name)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown(exception):
    """ close storage """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
