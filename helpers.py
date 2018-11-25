import uuid
import hashlib

import requests
from flask import redirect, render_template, request, session
from functools import wraps

# Creating the functin that queries the API for data
def lookup(isbn):
    results = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "LxgZiwNVfYBDtTJESQTQ", "isbns": isbn}).json()
    return results

# Creating the functin that redirects to the login page if not logged in
def login_required(f):
    """
    Decorate routes to require login.
    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
