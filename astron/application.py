import os
import re
from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import default_exceptions
from datetime import date
from helpers import lookup, apology, random

# Configure application
app = Flask(__name__)

@app.route("/")
def index():

    return render_template("index.html",)

@app.route("/explore", methods=["GET", "POST"])
def explore():
    
    today = str(date.today())

    if request.method == "POST":
        
        if "explore" in request.form:
            en_date = request.form.get("date")
            astro_pic = lookup(en_date)
            
            if not astro_pic:
                return apology("Invalid date")
            else:
                return render_template("explored.html", images=astro_pic)

        elif "random" in request.form:
            rand_pic = random()
            
            if not rand_pic:
                return apology("Oops something went wrong")
            else:
                return render_template("explored.html", images=rand_pic)

    else:
        return render_template("explore.html", today=today)

@app.route("/about")
def about():
    return render_template("about.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
