import os

from flask import Flask, session, render_template, jsonify, abort, request, redirect
from flask_session import Session
from tempfile import mkdtemp
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, lookup

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
@login_required
def index():
    """This page will be the first thing shown after a user logs in"""
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Will register a user"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get('username')
        password1 = request.form.get('password')
        password2 = request.form.get('confirmation')

        # Checking if username has been entered
        if not username:
            return "Enter a username please"

        # Checking if password has been entered
        elif not password1:
            return "Missing password"

        # Checking if password has been confirmed
        elif not password2:
            return "Please confirm your password"

        # Checking if passwords match
        elif password1 != password2:
            return "Password doesn't match"

        # Checking if username already exists in database
        username_check = db.execute("SELECT * FROM users WHERE username = :username",{"username": username}).first()
        if username_check:
            return "Username is already taken"

        # Adding user otherwise
        else:
            hashed = generate_password_hash(password2)
            result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                                {"username": username, "hash": hashed})
            db.commit()

            # Stroring id value in session to log user in
            session["user_id"] = db.execute("SELECT id FROM users WHERE username = :username", {"username": username}).fetchone()
            # Redirect user to home page
            return redirect("/")

    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Logs a user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            return "Must provide a username"

        # Ensure password was submitted
        elif not password:
            return "Must provide a password"

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          {"username": username}).fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return "Invalid username/password"

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    """Logs a user out"""
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    """This page will contain the search functionality of the site"""
    if request.method == "POST":
        # Getting the entered query
        q = request.form.get("query")
        q = "%" + q + "%"

        # Getting anything that matched the entered text
        results = db.execute("SELECT isbn, title, author, id, year FROM books WHERE isbn LIKE :q OR title LIKE :q OR author LIKE :q",
                {"q": q})

        # The data will be given to the template in a list, where each row is represented by another list
        result_list = []

        # In this loop, result and the rows therein are converted to lists; result_list containing row_lists
        for row in results:
            row_list = []
            for i in range(5):
                row_list.append(row[i])

            result_list.append(row_list)

        results.close()

        # Passing data to be shown
        return render_template("searched.html", result_list=result_list)

    else:
        return render_template("search.html")



@app.route("/book/<id>", methods=["GET", "POST"])
@login_required
def book(id):
    """The GET-method for this page will take the id of a book, search for that id in our database and return a page with
    info on the book. Part of that info is an average score on Goodreads. This data is retrieved
    using a query to the Goodreads API. Once implemented, this page will also display a form to
    leave a review, and display all existing reviews for the book.
    The POST-method for this route will submit the user's review, and redirect the user to this same
    route via GET"""
    if request.method == "POST":

        # Search for reviews on this book by this author
        result = db.execute("SELECT * FROM reviews WHERE user_id = :user AND id = :id",
        {"user": session["user_id"], "id": id })
        print("RESULT: ")
        print(result)
        userreview = result.first()

        # If there are no reviews on this book by this user, commit it to the reviews table
        if not userreview:
            # Get all data from submitted form
            rating = request.form.get("rating")
            review_text = request.form.get("review_text")

            # add review to database
            db.execute("INSERT INTO reviews (id, user_id, rating, review) VALUES (:id, :user, :rating, :review)",
            {"id": id,  "user": session["user_id"], "rating": rating, "review": review_text})
            db.commit()

            # Make URL to redirect user back to updated book-page
            this_book_url = "/book/" + id

            # redirect user to updated book page
            return redirect(this_book_url)

        else:

            return "You already reviewed this book."

    else:
        # Get data about book from database
        result = db.execute("SELECT isbn, title, author, year FROM books WHERE id = :id",
        {"id": id})

        # Store isbn, title, author, year (in that order) in book_data
        for row in result:
            book_data = dict(row)

        # add book id to book_data
        book_data['id'] = id

        # Query Goodreads for info on the book
        api_data = lookup(book_data['isbn'])

        # Store results from query in book_data
        book_data['average_rating'] = api_data['books'][0]['average_rating']
        book_data['number_ratings'] = api_data['books'][0]['reviews_count']

        # Get all reviews on this book from reviews table
        result = db.execute("SELECT user_id, rating, review FROM reviews WHERE id = :id",
                            {"id": id})

        # Store all rows in a list of dicts
        review_rows = []

        for row in result:
            review_rows.append(dict(row))

        return render_template("book.html", book_data=book_data, review_rows=review_rows)

@app.route("/api/<isbn>")
def api(isbn):
    """If user wants to query the api directly using
       isbn, this page will return a json object from the api"""

    # Select data from databse and store in a dict
    data = db.execute("SELECT title, author, year FROM books WHERE isbn = :isbn",
    {"isbn": isbn}).fetchone()
    print(data)
    if data:
        result = dict(data.first())

        # Adding isbn to the dict
        result['isbn'] = isbn

        # Adding the additional data from API
        api_data = lookup(isbn)
        result['review_count'] = api_data['books'][0]['reviews_count']
        result['average_score'] = api_data['books'][0]['average_rating']

        # Returning data as JSON
        return jsonify(result)

    else:
        # Aborting with 404 code if isbn is not in database
        abort(404)
