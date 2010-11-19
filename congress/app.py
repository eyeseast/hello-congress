import datetime
import json
import os
from flask import Flask, render_template

from nytcongress import NytCongress, get_congress

app = Flask(__name__)
nyt = NytCongress()

@app.route('/')
def home():
    house = nyt.votes.today('house')
    senate = nyt.votes.today('senate')
    return render_template('votes.html', house=house, senate=senate)

if __name__ == "__main__":
    app.run(debug=True)
