
import sqlite3
import json
from models import Comment


def get_all_comments():
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.content,
            c.post_id,
            c.author_id,
            c.created_on
        FROM Comments c
        """) 
        
        
        comments = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            post = Comment(row['id'], row['content'], row['post_id'],
                        row['author_id'], row['created_on'])

            comments.append(post.__dict__)

    return json.dumps(comments)

def get_comments_by_post(post_id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id,
            c.content,
            c.post_id,
            c.author_id,
            c.created_on
        FROM Comments c
        WHERE c.post_id = ?
        """, (post_id, ))

        comments = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            comment = Comment(row['id'],
                              row['content'],
                              row['post_id'], 
                              row['author_id'],
                              row['created_on'])

            comments.append(comment.__dict__)

    return json.dumps(comments)


def delete_comment(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Comments
        WHERE id = ?
        """, (id, ))


def create_comment(new_comment):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Comments
            ( post_id,
              author_id,
              content,
              created_on
               )

        VALUES
            ( ?, ?, ?, ?);
        """, (new_comment['post_id'],
              new_comment['author_id'],
              new_comment['content'],  
              new_comment['created_on'] 
              ))

        id = db_cursor.lastrowid

        new_comment['id'] = id

    return json.dumps(new_comment)


def update_comment(id, new_comment):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Comments
            SET
                
                content = ?,
                subject = ?
        WHERE id = ?
        """, (new_comment['content'],new_comment['subject'], id ))


        rows_affected = db_cursor.rowcount

    if rows_affected == 0:

        return False
    else:

        return True   

  
