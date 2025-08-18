import sqlite3

conn=sqlite3.connect("logs.db")
c= conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    service TEXT NOT NULL,
    severity TEXT NOT NULL,
    message TEXT NOT NULL,
    received_at TEXT NOT NULL
)
""")

conn.commit()
conn.close()
print("✅ Base de datos creada: logs.db")
