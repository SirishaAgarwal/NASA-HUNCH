import sqlite3

conn = sqlite3.connect("database.db")
conn.close()

print("database.db created successfully")