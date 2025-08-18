import requests
import datetime
import random
import time


SERVER_URL = "http://127.0.0.1:5000/logs"
TOKEN = "abc123"


SERVICIOS = ["servicio_a", "servicio_b"]
SEVERITIES = ["INFO", "DEBUG", "WARNING", "ERROR"]


def generar_log():
    return {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "service": random.choice(SERVICIOS),
        "severity": random.choice(SEVERITIES),
        "message": f"Evento simulado {random.randint(1, 100)}"
    }

def enviar_logs(cantidad=1, delay=0):
    for _ in range(cantidad):
        log = generar_log()
        try:
            r = requests.post(
                SERVER_URL,
                json=log,
                headers={"Authorization": f"Token {TOKEN}"}
            )
            if r.status_code == 200:
                print(f"✅ Log enviado: {log['message']}")
            else:
                print(f"❌ Error {r.status_code}: {r.text}")
        except Exception as e:
            print(f"💥 Error de conexión: {e}")
        time.sleep(delay)

if __name__ == "__main__":
    # Ejemplo: enviar 10 logs con 0.5 segundos de intervalo
    enviar_logs(cantidad=10, delay=0.5)