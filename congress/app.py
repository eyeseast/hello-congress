#!/usr/bin/env python

# **Hello, Congress!** is a simple demo app to see what can be
# done with Flask (a really simple microframework) and the
# New York Times' Congress API, using python-nytcongress.

import datetime
import os
from flask import Flask, render_template

from nytcongress import NytCongress, get_congress

# Create our Flask app
app = Flask(__name__)

# Instantiate our NYT Congress client:
# We're storing our API key in an environment variable
# called `NYT_CONGRESS_API_KEY`. `NytCongress` will
# check for this automatically if a key isn't provided,
# but better to be explicit here.
nyt = NytCongress(os.environ.get('NYT_CONGRESS_API_KEY'))

# Index view grabs the House and Senate votes from the
# last three days. There's a shortcut here if we just
# wanted today's votes, `nyt.votes.today(<chamber>)`,
# but that makes things pretty boring in the morning.
@app.route('/')
def home():
    today = datetime.date.today()
    house = nyt.votes.by_range('house', today, today - datetime.timedelta(days=3))
    senate = nyt.votes.by_range('senate', today, today - datetime.timedelta(days=3))
    return render_template('votes.html', house=house, senate=senate)

# Get a specific rollcall vote. The Times puts pretty much everything
# we need in one API call, and the data we need to link here will
# be in the votes returned in our index view above.
@app.route('/<int:congress>/<chamber>/<int:session>/<int:rollcall>')
def vote_detail(congress, chamber, session, rollcall):
    vote = nyt.votes.get(chamber, rollcall, session, congress)
    return render_template('vote_detail.html', vote=vote['votes']['vote']) # just trimming a little fat here

# Make it go.
if __name__ == "__main__":
    app.run(debug=True)
