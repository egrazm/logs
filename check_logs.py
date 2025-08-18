import sqlite3
from pprint import pprint

with sqlite3.connect("logs.db") as conn:
    c = conn.cursor()
    c.execute("SELECT id, timestamp, service, severity, message, received_at FROM logs ORDER BY id DESC LIMIT 10")
    rows = c.fetchall()

print(f"Total últimos {len(rows)} registros:")
for r in rows:
    pprint({
        "id": r[0],
        "timestamp": r[1],
        "service": r[2],
        "severity": r[3],
        "message": r[4],
        "received_at": r[5]
    })
