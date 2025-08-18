# 🐧 The Huddle - Sistema de Logging Distribuido

Este proyecto implementa un **sistema distribuido de logging** en Python.  
Permite que múltiples clientes envíen registros (logs) a un servidor central, que los guarda en una base de datos SQLite para su consulta posterior.

---

## 📂 Estructura del Proyecto

```
the-huddle/
├── server.py       # Servidor Flask que recibe y almacena logs
├── cliente.py      # Cliente que simula y envía logs al servidor
├── check_logs.py   # Script para consultar logs desde la base de datos
├── logs.db         # Base de datos SQLite (se crea automáticamente)
├── venv/           # Entorno virtual de Python (opcional)
└── README.md       # Documentación del proyecto
```

---

## ⚙️ Requisitos

- Python 3.10 o superior (probado en 3.13)
- Pip instalado
- Dependencias:
  ```bash
  pip install flask requests
  ```

---

## ▶️ Uso

### 1. Crear y activar entorno virtual
```bash
python -m venv venv
# Windows
.env\Scriptsctivate
# Linux/Mac
source venv/bin/activate
```

### 2. Instalar dependencias
```bash
pip install flask requests
```

### 3. Iniciar el servidor
```bash
python server.py
```
👉 El servidor quedará en `http://127.0.0.1:5000`

### 4. Enviar logs con el cliente
En otra terminal:
```bash
python cliente.py
```
Esto enviará 10 logs de prueba (uno cada 0.5 segundos).

Ejemplo de salida:
```
✅ Log enviado: Evento simulado 42
✅ Log enviado: Evento simulado 77
```

### 5. Consultar logs desde la API
```bash
Invoke-RestMethod -Uri "http://127.0.0.1:5000/logs" -Method Get
```

### 6. Revisar la base de datos directamente
```bash
python check_logs.py
```

---

## 🔐 Autenticación

El servidor requiere un **token de autorización** en cada request:

```http
Authorization: Token abc123
```

⚠️ El cliente (`cliente.py`) ya envía este token automáticamente.

---

## 🛠 Próximos pasos

- [ ] Filtros por severidad y servicio en la API  
- [ ] Dashboards de visualización en tiempo real  
- [ ] Manejo de múltiples clientes concurrentes  

---

## 👨‍💻 Autor

Proyecto educativo para **Penguin Academy 🐧**
