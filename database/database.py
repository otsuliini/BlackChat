import sqlite3
from datetime import datetime

# This will create 'chat.db' if it doesn't already exist
conn = sqlite3.connect('chat_logs.db')
cursor = conn.cursor()

# Create a table (if it doesn't already exist)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT NOT NULL,
        message TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()  # Commit changes
conn.close()   # Close the connection

def store_message(sender, message):
    try:
        conn = sqlite3.connect('chat_logs.db')  # Connect to SQLite database
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (sender, message, timestamp) VALUES (?, ?, ?)",
                       (sender, message, datetime.now()))
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

# Example usage
# store_message("Alice", "Hello, World!")
