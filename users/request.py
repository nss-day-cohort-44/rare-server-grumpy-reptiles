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

        id = db_cursor.lastrowid

        new_user['id'] = id

        user_id = {"token": id, "valid": True }


    return json.dumps(user_id)


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