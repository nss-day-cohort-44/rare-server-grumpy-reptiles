import sqlite3
import json


def create_category(new_category):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO CATEGORIES
            (label)
        VALUES
            (?);
        """, (new_category['label'],))

        id = db_cursor.lastrowid

        new_category['id'] = id

        return json.dumps(new_category)

def get_all_categories():
    
    with sqlite3.connect("./rare.db") as conn:

        
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        
        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM category c
        """)

        categories = []

        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            category = Category(row['id'], row['label'])

            categories.append(category.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(categories)
