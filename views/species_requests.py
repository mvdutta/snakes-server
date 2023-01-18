import sqlite3
from models import Species


def get_all_species():
    # Open a connection to the database
    with sqlite3.connect("./snakes.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            sp.id,
            sp.name
        FROM Species sp
        """)

        # Initialize an empty list to hold all species representations
        all_species = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create a species instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Species class above.
            species = Species(row['id'], row['name'])

            all_species.append(species.__dict__)

    return all_species

def get_single_species(id):
    with sqlite3.connect("./snakes.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            sp.id,
            sp.name
        FROM Species sp
        WHERE sp.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create a species instance from the current row
        species = Species(data['id'], data['name'])

    return species.__dict__
