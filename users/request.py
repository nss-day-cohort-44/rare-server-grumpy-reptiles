import sqlite3
import json


def create_user(new_user):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Users
            ( first_name,
              last_name,
              email,
              password,
              bio,
              username,
              profile_image_url,
              created_on,
              active,
              account_type_id )
        VALUES
            ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (new_user['first_name'],
              new_user['last_name'],
              new_user['email'], 
              new_user['password'], "", new_user['username'], "", "", "", ""))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_user['id'] = id

    return json.dumps(new_user)


def login_user(user):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT u.id 
        FROM Users u
        WHERE u.email = ? 
        AND u.password = ?
        """, (user["username"], user["password"], ))

        data = db_cursor.fetchone()

        user_id = {"token": data[0], "valid": True }

    return json.dumps(user_id)