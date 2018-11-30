import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
# This will import all the data in books.csv to the Postgres databse
# Run 'python3 import.py' to execute program
def main():
    # Create table to import data into
    db.execute("CREATE TABLE books (id SERIAL PRIMARY KEY, isbn VARCHAR NOT NULL, title VARCHAR NOT NULL, author VARCHAR NOT NULL, year VARCHAR NOT NULL)")

    with open('books.csv', 'r') as books_csv:
        csv_reader = csv.reader(books_csv)

        # Skip first row in csv, since this holds names of columns, not actual data
        next(csv_reader)

        for isbn, title, author, year in csv_reader:
            # Insert data into books table
            db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", {'isbn': isbn, 'title': title, 'author': author, 'year': year})
        db.commit()


if __name__ == "__main__":
    main()
