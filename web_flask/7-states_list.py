#!/usr/bin/python3
"""
Flask web application that use storage for fetching data from storage engine
"""

from flask import Flask
from flask import render_template
from models import storage
from models.state import State


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/states_list", strict_slashes=False)
def display_states():
    """ displays a HTML page of states from storage"""
    states = sorted(storage.all(State).values(), key=lambda x: x.name)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown(exception):
    """ close storage """
    storage.close()


if __name__ == "__main__":
    storage.reload()
    app.run(host='0.0.0.0', port=5000)
