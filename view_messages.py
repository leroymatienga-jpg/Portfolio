"""
Quick viewer script for Leroy Matienga to view all contact form messages in portfolio.db.
Usage:
    python view_messages.py
"""

import sys
import os
import sqlite3
from datetime import datetime

# Configure UTF-8 output if supported on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

DB_PATH = "portfolio.db"

def display_messages():
    if not os.path.exists(DB_PATH):
        print(f"\n[!] Database '{DB_PATH}' not found. No messages have been received yet.\n")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM contacts ORDER BY id DESC")
        rows = cursor.fetchall()

        if not rows:
            print("\n=======================================================")
            print("  LEROY MATIENGA PORTFOLIO -- INBOX")
            print("=======================================================")
            print("  No messages found in the database yet.\n")
            return

        print("\n" + "=" * 65)
        print(f"  LEROY MATIENGA PORTFOLIO -- INBOX ({len(rows)} Messages)")
        print("=" * 65)

        for i, row in enumerate(rows, 1):
            date_str = row["created_at"]
            try:
                dt = datetime.fromisoformat(date_str)
                formatted_date = dt.strftime("%b %d, %Y at %I:%M %p")
            except Exception:
                formatted_date = date_str

            print(f"\n[{i}] Message ID: #{row['id']}  |  Date: {formatted_date}")
            print(f"    From:    {row['name']} <{row['email']}>")
            print(f"    IP:      {row['ip_address'] or 'N/A'}")
            print(f"    Subject: {row['subject']}")
            print(f"    Message:\n        {row['message']}")
            print("-" * 65)

        print("\n[OK] All messages loaded successfully from portfolio.db.\n")

    except Exception as e:
        print(f"\n[!] Error reading messages from database: {e}\n")
    finally:
        conn.close()

if __name__ == "__main__":
    display_messages()
