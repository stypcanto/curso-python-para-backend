---
sidebar: "🧠 Conceptos"
---

# 🧠 Conceptos — Python para Backend

> Ideas y teoría del curso, explicadas con mis propias palabras. Cada concepto enlaza a la
> clase donde se vio.

| Concepto | Qué es | Clase |
|---|---|---|
| Backend | La lógica invisible de una app: recibe, valida, procesa, almacena y responde | [Clase 1](../01-Clases/Clase-01.md) |
| Entorno virtual (`venv`) | Aísla las dependencias de cada proyecto Python | [Clase 1](../01-Clases/Clase-01.md) |
| Tipos de datos básicos | `int`, `str`, `float`, `bool`, `None` — determinan qué operaciones se pueden hacer con un dato | [Clase 1](../01-Clases/Clase-01.md) |
| Lista vs. diccionario | Lista: colección ordenada por índice. Diccionario: pares clave-valor | [Clase 1](../01-Clases/Clase-01.md) |
| Type hints (`-> int`, `param: str`) | Pistas de tipo en una función; ayudan a leer el código, no se validan en ejecución | [Clase 1](../01-Clases/Clase-01.md) |
| Módulo | Archivo `.py` separado con funciones reutilizables, se importa con `from archivo import funcion` | [Clase 1](../01-Clases/Clase-01.md) |
| `try` / `except` / `raise` | Manejo de errores: capturar excepciones esperadas y lanzar las propias sin detener el programa | [Clase 1](../01-Clases/Clase-01.md) |
| Mutabilidad / aliasing | Listas y dicts se pasan "por referencia": modificarlos dentro de una función afecta al objeto original | [Clase 1 §9](../01-Clases/Clase-01.md#🧬-9-mutabilidad-y-aliasing-el-bug-mas-comun-en-backend) |
| `dataclass` | Define la forma de una entidad con tipos (antesala de los `BaseModel` de Pydantic) | [Clase 1 §11](../01-Clases/Clase-01.md#📦-11-dataclass-estructurar-una-entidad-sin-tanto-diccionario-suelto) |
| Excepciones propias (jerarquía) | Clases de error del dominio (`class MiError(Exception)`) para distinguir tipos de fallo y mapearlos a códigos HTTP | [Clase 1 §12](../01-Clases/Clase-01.md#🚨-12-excepciones-propias-modelar-errores-del-dominio) |
| `logging` | Registro de eventos con nivel de severidad (INFO/WARNING/ERROR), reemplaza a `print` en servicios reales | [Clase 1 §13](../01-Clases/Clase-01.md#🪵-13-logging-en-vez-de-print-en-servicios-reales) |
| Variables de entorno | Configuración sensible (host de BD, API keys) fuera del código, vía `os.environ` / `.env` | [Clase 1 §14](../01-Clases/Clase-01.md#🔐-14-variables-de-entorno-no-hardcodear-configuracion-sensible) |
| Comprehensions | Forma compacta de filtrar/transformar listas y diccionarios en una línea | [Clase 1 §15](../01-Clases/Clase-01.md#⚡-15-comprehensions-transformar-listas-de-diccionarios-sin-tanto-for) |
