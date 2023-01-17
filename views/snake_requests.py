import sqlite3
import json
from models import Snake


def get_all_snakes():
    # Open a connection to the database
    with sqlite3.connect("./snakes.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT *
        FROM Snakes sn
        """)

        # Initialize an empty list to hold all snake representations
        snakes = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create a snake instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Snake class above.
            snake = Snake(row['id'], row['name'], row['owner_id'], row['species_id'], row['gender'], row['color'])

            snakes.append(snake.__dict__)

    return snakes

def get_snakes_by_species_id(species_id):
    with sqlite3.connect("./snakes.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT *
        FROM Snakes sn
        WHERE sn.species_id = ?
        """, (species_id, ))
        snakes = []
        dataset = db_cursor.fetchall()
        if len(dataset) > 0:
            for row in dataset:
                snake = Snake(row['id'], row['name'], row['owner_id'],
                          row['species_id'], row['gender'], row['color'])

                result = snake.__dict__
                snakes.append(result)
    return snakes
