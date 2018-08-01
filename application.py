import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
import time
import sqlite3
# Ensure environment variable is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
    

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Select symbol,shares and price from database
    assets = db.execute("SELECT symbol, shares, price FROM portfolio WHERE id=:id",
                        id=session["user_id"])

    # Update value of shares and total
    total_assets = 0
    for assets in assets:
        symbol = assets["symbol"]
        shares = int(assets["shares"])
        stock = lookup(symbol)
        new_total = float(shares * stock["price"])
        total_assets += new_total
        db.execute("UPDATE portfolio SET price=:price, total=:total WHERE id=:id AND symbol=:symbol",
                    price=usd(stock["price"]), total=usd(new_total), id=session["user_id"], symbol=symbol)

     # Select data to display in table
    cash = db.execute("SELECT cash FROM users WHERE id=:id",
                      id=session["user_id"])
   
    total_assets += cash[0]["cash"]

    port = db.execute("SELECT symbol, shares, price FROM portfolio WHERE id=:id",
                      id=session["user_id"])
            
    total = db.execute("SELECT total FROM portfolio WHERE id=:id",
                       id=session["user_id"])

    return render_template("index.html", stocks=port, cash=usd(cash[0]["cash"]), total=total, total_assets=usd(total_assets))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        stock = lookup(request.form.get("symbol"))

        # Ensure fields are filled
        if not request.form.get("symbol"):
            return apology("Missing Stock Symbol")

        elif not request.form.get("shares"):
            return apology("Number of shares not specified")

        # Ensures valid symbol entered
        elif not stock:
            return apology("Invalid Stock Symbol")

        # Ensure proper number of shares
        try:
            shares = int(request.form.get("shares"))
            if shares < 0:
                return apology("Shares must be positive integer")
        except:
            return apology("Shares must be positive integer")

        # Select user's cash
        money = db.execute("SELECT cash FROM users WHERE id = :id",
                            id=session["user_id"])

        # Check if money is enough to buy
        if not money or float(money[0]["cash"]) < int(stock["price"] * shares):
            return apology("Not enough money")

        # update user cash 
        db.execute("UPDATE users SET cash = cash - :purchase WHERE id = :id",
                    id=session["user_id"],
                    purchase=stock["price"] * float(shares))

        # update history
        db.execute("INSERT INTO history (symbol, shares, price, date, id) VALUES(:symbol, :shares, :price, :date, :id)",
                    symbol=stock["symbol"], shares=shares, price=usd(stock["price"] * shares),
                    date=time.asctime(time.localtime(time.time())), id=session["user_id"])

        # Select user shares of that symbol
        purchase = db.execute("SELECT symbol FROM portfolio WHERE id = :id AND symbol=:symbol", 
                              id=session["user_id"], symbol=stock["symbol"]) 

        # if user doesn't have shares of that symbol, create new stock object
        if not purchase:
            db.execute("INSERT INTO portfolio (id, symbol, price, shares, total) VALUES(:id, :symbol, :price, :shares, :total)",
                       id=session["user_id"], symbol=stock["symbol"],
                       price=usd(stock["price"]), shares=shares, total=shares * stock["price"])

        # Else increment the shares count
        else:

            db.execute("UPDATE portfolio SET shares = shares + :bshares, total = total + :ptotal WHERE id=:id AND symbol=:symbol", 
                       bshares=shares, ptotal=shares * stock["price"], id=session["user_id"], symbol=stock["symbol"])
       # Redirect user to home page
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    transactions = db.execute("SELECT symbol, price, shares, date FROM history WHERE id=:id",
                              id=session["user_id"])

    return render_template("history.html", history=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        rows = lookup(request.form.get("symbol"))

        if not rows:
            return apology("Invalid Symbol")

        return render_template("quoted.html", stock=rows)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Checking if username has been entered
        if not request.form.get("username"):
            return apology("Missing Username")

        # Checking if password has been entered
        elif not request.form.get("password"):
            return apology("Missing password")

        # Checking if password has been confirmed
        elif not request.form.get("confirmation"):
            return apology("Please confirm your password")

        # Checking if passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Password doesn't match")

        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                            username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))
        if not result:
            return apology("Username already exists")
        
        # remember which user has logged in
        session["user_id"] = result

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    options = db.execute("SELECT symbol FROM portfolio WHERE id=:id",
                         id=session["user_id"])

    if request.method == "POST":

        # Importing stock info
        stock = lookup(request.form.get("symbol"))

        # Checking for input validity
        if not request.form.get("symbol"):
            return apology("Missing symbol")

        elif not request.form.get("shares"):
            return apology("Specify number of share")

        elif not stock:
            return apology("Invalid stock symbol")

        # ensure proper number of shares
        try:
            shares = int(request.form.get("shares"))
            if shares < 0:
                return apology("Shares must be positive integer")
        except:
            return apology("Shares must be positive integer")

        tsymbol = db.execute("SELECT symbol,shares FROM portfolio WHERE id=:id AND symbol=:symbol",
                             id=session["user_id"], symbol=stock["symbol"])

        # Checking if user owns entered stock 
        if not tsymbol:
            return apology("Stock not found")

        else:
            share_count = db.execute("SELECT shares FROM portfolio WHERE id=:id AND symbol=:symbol",
                                     id=session["user_id"], symbol=stock["symbol"])

            if share_count[0]["shares"] - int(request.form.get("shares")) < 0:
                return apology("You do not have that many shares of selected stock")

            # If the sale of shares results in the no. of that stock to become 0
            elif share_count[0]["shares"] - int(request.form.get("shares")) == 0:

                # Delete that stock from portfolio
                db.execute("DELETE FROM portfolio WHERE id=:id AND symbol=:symbol",
                           id=session["user_id"], symbol=stock["symbol"])

                # Update cash
                db.execute("UPDATE users SET cash = cash + :sale WHERE id = :id",
                           id=session["user_id"], sale=float(stock["price"]))

            else:

                # Update cash
                db.execute("UPDATE users SET cash = cash + :sale WHERE id = :id",
                           id=session["user_id"], sale=stock["price"] * int(request.form.get("shares")))

                # Update no. of shares owned in portfolio
                db.execute("UPDATE portfolio SET shares = shares - :sold WHERE id=:id AND symbol=:symbol",
                        sold=request.form.get("shares"), id=session["user_id"], symbol=stock["symbol"])

                # update history
                db.execute("INSERT INTO history (symbol, shares, price, date, id) VALUES(:symbol, :shares, :price, :date, :id)", 
                           symbol=stock["symbol"], shares=-int(request.form.get("shares")), price=usd(stock["price"] * int(request.form.get("shares"))),
                           date=time.asctime(time.localtime(time.time())), id=session["user_id"])

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("sell.html", select=options)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
