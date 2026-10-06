"""
Database models and operations for the Portfolio application.
Uses SQLite via Python's built-in sqlite3 module.
"""

import sqlite3
from datetime import datetime
from config import Config


def get_db_connection():
    """Create and return a database connection with row factory."""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database and create tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            ip_address TEXT,
            is_read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print("[DB] Database initialized successfully.")


def save_message(name, email, subject, message, ip_address=None):
    """
    Save a contact form message to the database.

    Args:
        name: Sender's name
        email: Sender's email
        subject: Message subject
        message: Message body
        ip_address: Sender's IP address (for rate limiting)

    Returns:
        dict with the saved message data, or None on failure
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO contacts (name, email, subject, message, ip_address, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (name, email, subject, message, ip_address, datetime.utcnow().isoformat())
        )

        conn.commit()
        message_id = cursor.lastrowid
        conn.close()

        return {
            "id": message_id,
            "name": name,
            "email": email,
            "subject": subject,
            "message": message,
            "created_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        print(f"[DB ERROR] Failed to save message: {e}")
        return None


def get_all_messages():
    """
    Retrieve all contact messages from the database, newest first.

    Returns:
        List of message dictionaries
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM contacts ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]
    except Exception as e:
        print(f"[DB ERROR] Failed to retrieve messages: {e}")
        return []


def count_recent_messages(ip_address, window_seconds):
    """
    Count messages sent from an IP address within a time window (for rate limiting).

    Args:
        ip_address: The IP to check
        window_seconds: Time window in seconds

    Returns:
        Number of messages sent in the window
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*) as count FROM contacts
            WHERE ip_address = ?
            AND created_at >= datetime('now', ?)
            """,
            (ip_address, f"-{window_seconds} seconds")
        )

        result = cursor.fetchone()
        conn.close()

        return result["count"] if result else 0
    except Exception as e:
        print(f"[DB ERROR] Rate limit check failed: {e}")
        return 0
