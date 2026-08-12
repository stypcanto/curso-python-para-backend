---
sidebar: "🖥️ Comandos"
---

# 🖥️ Comandos — Python para Backend

> Comandos de terminal, Python, pip, entornos virtuales, etc. que voy usando en el curso.

| Comando | Qué hace | Ejemplo |
|---|---|---|
| `python3 -m venv .venv` | Crea un entorno virtual en la carpeta `.venv/` para aislar las dependencias del proyecto (en macOS es `python3`, no `python` — ver [[python-command-not-found]]) | `python3 -m venv .venv` |
| `source .venv/bin/activate` | Activa el entorno virtual en macOS/Linux | `source .venv/bin/activate` |
| `.\.venv\Scripts\activate` | Activa el entorno virtual en Windows (referencia — no aplica en tu Mac) | `.\.venv\Scripts\activate` |
| `python3 --version` | Muestra la versión de Python instalada | `python3 --version` |
| `pip --version` | Muestra la versión de pip **del entorno virtual activo** (falla con "command not found" si el venv no está activado — ver [[pip-command-not-found-venv-inactivo]]) | `pip --version` |
| `pip install <paquete>` | Instala una librería en el venv activo | `pip install fastapi "uvicorn[standard]"` |
| `pip show <paquete>` | Muestra la versión instalada de una librería (para no reinstalar de más) | `pip show fastapi` |
| `pip freeze > requirements.txt` | Congela todas las dependencias instaladas y sus versiones exactas en un archivo | `pip freeze > requirements.txt` |
| `pip install -r requirements.txt` | Instala todas las dependencias listadas en el archivo (lo que corre alguien que clona el repo) | `pip install -r requirements.txt` |
| `python3 archivo.py` | Ejecuta un script de Python | `python3 main.py` |
