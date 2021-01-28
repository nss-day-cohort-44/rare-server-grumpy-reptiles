import sqlite3
import json


def create_comment(new_comment):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Comments
            ( post_id,
              author_id,
              content
               )

        VALUES
            ( ?, ?, ?);
        """, (new_comment['post_id'],
              new_comment['author_id'],
              new_comment['content'], 
              ))


              

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_comment['id'] = id

    return json.dumps(new_comment)
