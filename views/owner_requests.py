import sqlite3
from models import Owner


def get_all_owners():
    # Open a connection to the database
    with sqlite3.connect("./snakes.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT *
        FROM Owners o
        """)

        # Initialize an empty list to hold all owner representations
        owners = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an owner instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Owner class above.
            owner = Owner(row['id'], row['first_name'], row['last_name'], row['email'])

            owners.append(owner.__dict__)

    return owners

def get_single_owner(id):
    with sqlite3.connect("./snakes.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT *
        FROM Owners o
        WHERE o.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create a species instance from the current row
        owner = Owner(data['id'], data['first_name'],
                      data['last_name'], data['email'])

        
    return owner.__dict__
