import sqlite3
import json


# def get_all_posts():
#     # Open a connection to the database
#     with sqlite3.connect("./rare.db") as conn:

#         # Just use these. It's a Black Box.
#         conn.row_factory = sqlite3.Row
#         db_cursor = conn.cursor()

#         # Write the SQL query to get the information you want
#         db_cursor.execute("""
#         SELECT
#             p.id,
#             p.user_id,
#             p.catergory_id,
#             p.title,
#             p.publication_date,
#             p.image-url,
#             p.content,
#             p.approved
#         """)

#         # Initialize an empty list to hold all animal representations
#         posts = []

#         # Convert rows of data into a Python list
#         dataset = db_cursor.fetchall()

#     return json.dumps(posts)


def create_post(new_post):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Posts
            (
            user_id,
            category_id,
            title,
            publication_date,
            image_url,
            content,
            approved )
        VALUES
            ( ?, ?, ?, ?, ?, ?, ?);
        """, (new_post['user_id'],
              new_post['category_id'],
              new_post['title'],
              new_post['publication_date'],
              new_post['image_url'],
              new_post['content'],
              new_post['approved']))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_post['id'] = id

    return json.dumps(new_post)
