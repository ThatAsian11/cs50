import urllib.request
import json
from datetime import date
from flask import redirect, render_template, request, session, jsonify

def lookup(date):
    """Look up APOD for entered date"""
    
    if "-" not in date:
        return None
    
    try:

        with urllib.request.urlopen(f"https://api.nasa.gov/planetary/apod?date={date}&api_key=DEMO_KEY") as url:
            data = json.loads(url.read().decode())
            return data

    except:
        return None

def random():
    """Returns a random APOD"""
    try:

        with urllib.request.urlopen("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&count=1") as url:
            data = json.loads(url.read().decode())
            return data[0]

    except:
        return None
    

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code