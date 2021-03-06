import sqlite3
from models import Post
import json
import datetime
from models import User


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
              datetime.datetime.now(),
              new_post['image_url'],
              new_post['content'],
              1))

        id = db_cursor.lastrowid
        new_post['id'] = id

    return json.dumps(new_post)


def get_all_posts():
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved
        FROM posts p
        WHERE approved="1"
        """)

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'],
                        row['title'], row['content'], row['approved'], row['publication_date'],
                        row['image_url'])

            posts.append(post.__dict__)

    return json.dumps(posts)


def get_posts_by_user(user_id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            u.username,
            u.first_name,
            u.last_name,
            u.email,
            u.password,
            u.bio,
            u.created_on,
            u.active,
            u.profile_image_url
        FROM posts p
        JOIN Users u
            ON u.id = p.user_id
        WHERE p.user_id = ?
        """, (user_id, ))

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            post = Post(row['id'], row['user_id'], row['category_id'],
                        row['title'], row['content'], row['approved'], row['publication_date'],
                        row['image_url'])

            posts.append(post.__dict__)

            user = User(row['id'], row['first_name'], row['last_name'], row['email'], row['password'],
                        row['bio'], row['username'],
                        row['created_on'], row['active'], row['profile_image_url'])
            post.user = user.__dict__

    return json.dumps(posts)


def get_single_post(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            u.username,
            u.first_name,
            u.last_name,
            u.email,
            u.password,
            u.bio,
            u.created_on,
            u.active,
            u.profile_image_url
        FROM posts p
        JOIN Users u
            ON u.id = p.user_id
        WHERE p.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        post = Post(data['id'], data['user_id'], data['category_id'],
                    data['title'], data['content'], data['approved'], data['publication_date'],
                    data['image_url'])

        user = User(data['id'], data['first_name'], data['last_name'], data['email'], data['password'],
                    data['bio'], data['username'],
                    data['created_on'], data['active'], data['profile_image_url'])
        post.user = user.__dict__
    return json.dumps(post.__dict__)


def delete_post(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Posts
        WHERE id = ?
        """, (id, ))


def update_post(id, new_post):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Posts
            SET
                category_id = ?,
                title = ?,
                image_url = ?,
                content = ?
        WHERE id = ?
        """, (new_post['category_id'], new_post['title'], new_post['image_url'], new_post['content'], id, ))

        rows_affected = db_cursor.rowcount

        if rows_affected == 0:
            return False
        else:
            return True
