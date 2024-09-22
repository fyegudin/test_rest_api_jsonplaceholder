import sqlite3
import os
from config import DATABASE


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            userId INTEGER,
            title TEXT,
            body TEXT,
            id INTEGER PRIMARY KEY
        )
    ''')
    conn.commit()
    conn.close()


def insert_post(userId, title, body, post_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO posts (userId, title, body, id) VALUES (?, ?, ?, ?)
    ''', (userId, title, body, post_id))
    conn.commit()
    conn.close()


def fetch_post(post_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM posts WHERE id = ?
    ''', (post_id,))
    post = cursor.fetchone()
    conn.close()
    return post


def delete_database():
    """Delete the database file if it exists."""
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
        return True
    return False
