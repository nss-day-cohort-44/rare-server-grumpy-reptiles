
import sqlite3
import json
from models import Comment


def get_comments_by_post(post_id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.content,
            c.post_id,
            c.author_id
        FROM Comments c
        WHERE c.post_id = ?
        """, (post_id, ))

        comments = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            comment = Comment(row['id'],
                              row['content'],
                              row['post_id'], 
                              row['author_id'])

            comments.append(comment.__dict__)

    return json.dumps(comments)