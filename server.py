from flask import Flask, request, jsonify
import sqlite3
import datetime
import requests

app = Flask(__name__)

DB_PATH = "logs.db"

# Tokens válidos (uno por servicio)
TOKENS_VALIDOS = {
    "pagos": "abc123",
    "notificaciones": "xyz789",
    "reportes": "def456"

}

# ---------- utilidades de DB ----------
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            service TEXT NOT NULL,
            severity TEXT NOT NULL,
            message TEXT NOT NULL,
            received_at TEXT NOT NULL
        )""")

        conn.commit()

def insert_logs(logs):
    now_utc = datetime.datetime.utcnow().isoformat() + "Z"
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.executemany(
            "INSERT INTO logs (timestamp, service, severity, message, received_at) VALUES (?,?,?,?,?)",
            [(log["timestamp"], log["service"], log["severity"], log["message"], now_utc) for log in logs]
        )
        conn.commit()

def validar_token(header_value: str) -> bool:
    if not header_value or not header_value.startswith("Token "):
        return False
    token = header_value.split(" ", 1)[1]
    return token in TOKENS_VALIDOS.values()

def validar_log_dict(d: dict) -> tuple[bool, str]:
    requeridos = ["timestamp", "service", "severity", "message"]
    for k in requeridos:
        if k not in d:
            return False, f"Falta el campo requerido: {k}"
        if not isinstance(d[k], str) or not d[k].strip():
            return False, f"Campo vacío o inválido: {k}"
    return True, ""

# ---------- endpoints ----------
@app.route("/ping", methods=["GET"]) 
def ping():
    return jsonify({"status": "ok"})

@app.route("/logs", methods=["POST"])
def recibir_logs():
    # 1) Autenticación por token
    if not validar_token(request.headers.get("Authorization", "")):
        return jsonify({"error": "Quién sos, bro?"}), 401

    # 2) Parseo JSON
    data = request.get_json(silent=True)  # que es e lsilent true
    if data is None:
        return jsonify({"error": "JSON inválido o faltante"}), 400

    # Normalizar a lista
    if isinstance(data, dict):  #inverstigar
        data = [data]
    elif not isinstance(data, list):
        return jsonify({"error": "El cuerpo debe ser un objeto o una lista de objetos"}), 400 

    # 3) Validación de cada log
    logs_validados = []
    for idx, log in enumerate(data, start=1): #investigar
        if not isinstance(log, dict):
            return jsonify({"error": f"Elemento #{idx} no es un objeto JSON"}), 400
        ok, msg = validar_log_dict(log)
        if not ok:
            return jsonify({"error": f"Log #{idx}: {msg}"}), 400
        logs_validados.append(log)

    # 4) Insertar en DB
    try:
        insert_logs(logs_validados)
    except Exception as e:
        return jsonify({"error": f"Error guardando en DB: {e}"}), 500

    # 5) Respuesta
    return jsonify({"status": "ok", "count": len(logs_validados)}), 200


@app.route("/logs", methods=["GET"])
def consultar_logs():
    params = request.args
    service = params.get("service")  # 👈 parámetro para filtrar por servicio

    query = "SELECT id, timestamp, service, severity, message, received_at FROM logs WHERE 1=1"
    values = []

    if service:
        query += " AND service = ?".lower()   # 👈 filtro por servicio
        values.append(service)

    query += " ORDER BY id ASC"

    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(query, values)
        rows = c.fetchall()

    logs = []
    for r in rows:
        logs.append({
            "id": r[0],
            "timestamp": r[1],
            "service": r[2],
            "severity": r[3],
            "message": r[4],
            "received_at": r[5]
        })

    return jsonify({"count": len(logs), "logs": logs})



if __name__ == "__main__":
    init_db()
    # debug=True para desarrollo; en prod usar un WSGI server (gunicorn/uwsgi)
    app.run(debug=True)
