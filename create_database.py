import sqlite3


conn = sqlite3.connect('/app/database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE IF NOT EXISTS my_table (id INTEGER PRIMARY KEY, name TEXT)')
print("Table created successfully")

conn.close()