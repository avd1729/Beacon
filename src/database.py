import sqlite3

conn = sqlite3.connect('db/peer_registry.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS PEERS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip TEXT NOT NULL,
    port TEXT NOT NULL,
    UNIQUE(ip, port)
)
''')

conn.commit()
conn.close()
