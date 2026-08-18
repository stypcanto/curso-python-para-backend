---
sidebar: "Clase 1 · Fundamentos de Python"
---

# 📙 Clase 1 — Fundamentos de Python para Backend

> Python para Backend · 2026-07-30 · Carpeta: `02-Ejercicios/Clase-01`
> ⬅️ Volver al [índice de clases](00-Indice.md)
> 📎 Material: [Presentación de la Clase 1](../04-Recursos/presentaciones/Clase1.pdf)

## 🎯 Qué aprendí
- Qué hace realmente el Backend (lo que el usuario no ve).
- Por qué Python es una buena tecnología para Backend.
- Preparar un entorno de desarrollo con entorno virtual (`venv`) y `pip`.
- Representar información con los tipos de datos básicos (`int`, `str`, `float`, `bool`, `None`).
- Agrupar información con listas, diccionarios y listas de diccionarios.
- Tomar decisiones y repetir procesos (`if`/`elif`/`else`, `for`, `while`).
- Organizar la lógica en funciones tipadas y módulos separados.
- Manejar errores con `try`/`except`/`raise` en vez de dejar que el programa se detenga.
- *(profundización propia)* Mutabilidad/aliasing, tipos opcionales, `dataclass`,
  excepciones propias, `logging`, variables de entorno y comprehensions.
- *(práctica libre)* `input()` para leer datos del usuario por consola, combinado con
  conversión de tipos (`float`) para trabajar el dato como número.
- *(práctica libre)* El módulo `calendar` de la librería estándar (no se instala con
  `pip`) y la diferencia entre variables sueltas vs. agruparlas en un `dict`/lista de
  `dict`s para el mismo dato.
- *(práctica libre)* Comparación de strings ignorando mayúsculas (`.lower()`),
  condicionales aplicados a casos reales (jubilación, tributación), listas
  (`.append()`/`.remove()`/`.index()`), `while` vs. `for` para recorrer una colección,
  una función propia con varias ramas `if`/`elif`, y `try`/`except` a mano.

# 📖 PARTE TEÓRICA

## 🖥️ 1. El Backend: la lógica detrás de una aplicación
El Backend es el motor invisible de toda aplicación: la parte que el usuario final nunca
ve pero que hace posible que todo funcione. Con mis palabras, se encarga de:

- Recibir y procesar la información que llega (de un formulario, una API, etc.).
- Aplicar reglas de negocio y validar que los datos tengan sentido.
- Consultar o almacenar información (bases de datos, archivos, otros servicios).
- Gestionar usuarios y permisos (quién puede hacer qué).
- Responder a otras aplicaciones (no solo a personas — también a otros sistemas).

> 💡 Ejemplo visto en clase: al registrar una solicitud de soporte, el Backend verifica los
> datos, determina la prioridad, registra la solicitud y genera una respuesta. Todo eso
> pasa "detrás" sin que el usuario lo vea — solo ve el resultado final.

## 🐍 2. Por qué Python como tecnología de Backend
| Ventaja | Qué significa |
|---|---|
| Sintaxis clara | Legible y accesible para desarrolladores de cualquier nivel. |
| Gran ecosistema | Librerías para APIs, datos, automatización e inteligencia artificial. |
| Multiplataforma | Compatible con distintos sistemas operativos y servicios externos. |
| Integración | Conexión nativa con bases de datos y APIs de terceros. |

> 📌 Principio clave de la clase: **antes de construir una API, hay que dominar la lógica
> que esa API va a ejecutar.** Todo lo que se ve en esta clase (tipos, condicionales,
> funciones, errores) es la base sobre la que después se arma una API.

## ⚙️ 3. Preparando el entorno
Herramientas necesarias: Python 3, un editor (VS Code o PyCharm), una terminal, un
**entorno virtual** (`venv`) y el administrador de paquetes `pip`.

> 💡 El entorno virtual mantiene aisladas las dependencias de cada proyecto — así un
> proyecto no "contamina" las librerías de otro.

```bash
mkdir backend_python
cd backend_python
python -m venv .venv          # crea el entorno virtual en la carpeta .venv/

# Activación en macOS/Linux (mi caso)
source .venv/bin/activate
# Activación en Windows (como lo mostró la diapositiva, de referencia)
.\.venv\Scripts\activate

# Verificación
python --version
python -m pip --version
```

Estructura inicial sugerida en clase:
```
backend_python/
├── .venv/
├── main.py
└── requirements.txt
```

> 📝 La diapositiva solo mostraba la activación en Windows (`.\.venv\Scripts\activate`).
> Trabajo en macOS, así que documento primero `source .venv/bin/activate` (ver
> `CLAUDE.md` — comandos de sistema siempre en macOS/Linux primero).

### 🎬 Qué hizo el profesor, paso a paso (y para qué sirve cada comando)

| Comando | Qué hace | Para qué |
|---|---|---|
| `python3 -m venv .venv` | Crea la carpeta `.venv/` con una copia aislada del intérprete de Python y su propio `pip` | Que las librerías de este proyecto no se mezclen con las de otro (ni con las del sistema) |
| `source .venv/bin/activate` | Activa ese entorno **en la terminal actual** | Que `python` y `pip` (sin el "3") apunten al Python del proyecto, no al del sistema |
| `deactivate` | Sale del entorno virtual activo | Volver a usar el Python "normal" del sistema |

> 📝 **¿Por qué `source` y no correr `activate` directo?** `activate` es un script que
> modifica variables de entorno (`PATH`, `VIRTUAL_ENV`). Si lo corrés sin `source`
> (`.venv/bin/activate` a secas), zsh lo ejecuta en un **subshell**: ese subshell activa
> el venv y se cierra al instante, sin que tu terminal se entere del cambio — por eso el
> prompt nunca muestra `(.venv)`. `source` (o su alias `.`) le dice al shell "ejecutá
> este script **en mí mismo**, no en un proceso aparte" — así el cambio de variables
> queda en tu sesión actual.
>
> ⚠️ Tropiezo real durante la clase: si hacés `cd` hacia **adentro** de la carpeta
> `.venv` (en vez de quedarte en `Clase-01/`), `source .venv/bin/activate` deja de
> encontrar la ruta — `.venv` no está dentro de sí misma. Verificá con `pwd` que estás
> un nivel **arriba** de `.venv` antes de activar — ver
> [[2026-08-14-activate-sin-source-no-funciona]].

### 🧩 Extensiones de VS Code recomendadas en clase
| Extensión | Publisher (id) | Para qué sirve |
|---|---|---|
| [Python Indent](https://marketplace.visualstudio.com/items?itemName=KevinRose.vsc-python-indent) | Kevin Rose (`KevinRose.vsc-python-indent`) | Corrige la indentación automática al presionar Enter — analiza el código hasta el cursor para calcular el nivel correcto (la indentación por defecto de VS Code para Python falla seguido en `if`, `for`, listas multilínea, etc.). |
| [Python Debugger](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy) | Microsoft (`ms-python.debugpy`) | Debugger de Python basado en `debugpy`: poner breakpoints, ejecutar paso a paso, inspeccionar variables. Se separó de la extensión "Python" principal de Microsoft para poder actualizarse de forma independiente. |

> 💡 Ambas se instalan igual que cualquier extensión: `Cmd+Shift+X` en VS Code, buscar por
> nombre e instalar (o `code --install-extension KevinRose.vsc-python-indent` /
> `code --install-extension ms-python.debugpy` desde la terminal).

### 🐍 ¿Qué versión de Python instalar?
En clase se recomendó instalar la **versión más estable**, no la última a secas — se
mostró la página oficial de descargas para explicarlo. Python mantiene varias versiones
"vivas" en paralelo, cada una en una etapa distinta de su ciclo de vida:

| Etapa | Qué significa |
|---|---|
| 🟡 `bugfix` | Versión activa y recomendada: recibe correcciones de bugs además de parches de seguridad. |
| 🟨 `security` | Ya no recibe nuevas funciones ni bugfixes — solo parches de seguridad críticos. |
| 🟢 `prerelease` / `feature` | Todavía en desarrollo (alfa/beta/RC) — **no** es para producción ni para aprender recién. |
| 🔴 `end-of-life` | Sin soporte de ningún tipo — no debería usarse. |

> 📌 La "versión más estable" es la que está en etapa `bugfix` (o `security` si querés
> algo muy probado) — **no** la última `prerelease` que aparece más a la derecha del
> gráfico, aunque tenga el número más alto.

### 🗺️ Diagrama: ciclo de vida de las versiones de Python (python.org/downloads)
![Gráfico de python.org con las versiones activas de Python y su etapa de soporte (bugfix, security, prerelease, end-of-life)](/clase-01-python-versiones-estables.png)

> 💡 Fuente: [python.org/downloads](https://www.python.org/downloads/) — captura tomada en
> clase. Guardada también en
> [`04-Recursos/imagenes/clase-01-python-versiones-estables.png`](../04-Recursos/imagenes/clase-01-python-versiones-estables.png)
> por si la imagen del sitio se pierde.

## 🔢 4. Tipos de datos básicos
Cada dato del mundo real tiene un tipo en Python, y el tipo determina qué operaciones se
pueden hacer con él.

| Información | Tipo | Ejemplo |
|---|---|---|
| Código de solicitud | `int` | `1001` |
| Título | `str` | `"Error de acceso"` |
| Tiempo estimado | `float` | `2.5` |
| Solicitud activa | `bool` | `True` |
| Valor inexistente | `None` | `None` |

```python
request_id = 1001
title = "No puedo acceder"
estimated_hours = 2.5
is_active = True
assigned_user = None

# Conversión de tipos: un texto no es lo mismo que un número
hours_text = "3"
estimated_hours = int(hours_text)   # "3" (str) -> 3 (int)
```

> 🧪 Tip de entrevista: `type("1001")` es `str` (son comillas, es texto) y `type(2.5)` es
> `float`. Es un error común confundir un número "parecido" con el tipo real del dato.

## 📦 5. Agrupando información relacionada
| Estructura | Qué es | Ejemplo |
|---|---|---|
| Lista (`list`) | Colección **ordenada**, se accede por índice, es mutable | `categories = ["Hardware", "Software", "Accesos"]` |
| Diccionario (`dict`) | Pares **clave-valor**, acceso por nombre, es mutable | `request = {"id": 1001, "priority": "Alta"}` |
| Lista de diccionarios | Colección de registros — ideal para varias entidades del mismo tipo | `requests = [{"id": 1001, "priority": "Alta"}, {"id": 1002, "priority": "Media"}]` |

```python
categories = ["Hardware", "Software", "Accesos"]

request = {
    "id": 1001,
    "title": "Error de acceso",
    "priority": "Alta",
    "active": True,
}

requests = [
    {"id": 1001, "priority": "Alta"},
    {"id": 1002, "priority": "Media"},
]
```

> 💡 La lista de diccionarios es el patrón que más se repite en Backend: así se
> representa, por ejemplo, el resultado de una consulta a una base de datos (una fila =
> un diccionario, varias filas = una lista).

## 🔀 6. Tomando decisiones y repitiendo procesos
| Estructura | Qué hace |
|---|---|
| `if` / `elif` / `else` | Decide según una condición. |
| `for` | Recorre una colección elemento a elemento. |
| `while` | Repite mientras se cumpla una condición. |

```python
if priority == "Alta":
    response_time = 2
elif priority == "Media":
    response_time = 8
else:
    response_time = 24

for request in requests:
    print(request["id"])

for request in requests:
    if request["priority"] == "Alta":
        print(f"Crítica: {request['id']}")
```

> 🧪 Tip de entrevista (pregunta de la clase): si `priorities = ["Alta", "Baja", "Alta"]`
> y por cada `"Alta"` se suma 1 a `total`, ¿cuántas veces se suma? **Respuesta: 2** (solo
> cuenta las veces que la condición del `if` se cumple, no el largo de la lista).

## 🧩 7. Organizando y reutilizando la lógica: funciones y módulos
Una función con **type hints** (`priority: str` y `-> int`) deja explícito qué tipo de
dato espera recibir y qué tipo va a devolver — ayuda a leer el código y a detectar
errores antes de ejecutar.

```python
def calculate_response_time(priority: str) -> int:
    if priority == "Alta":
        return 2
    if priority == "Media":
        return 8
    return 24

hours = calculate_response_time("Alta")
print(hours)  # 2
```

Cuando una función se va a reutilizar en varios archivos, conviene moverla a su propio
**módulo** (un archivo `.py` separado) e importarla:
```
backend_python/
├── main.py
└── request_utils.py
```
```python
# request_utils.py
def calculate_response_time(priority):
    # Lógica de cálculo
    pass

# main.py
from request_utils import calculate_response_time
```

> 📌 Buen criterio (regla vista en clase): una función debe tener **un propósito
> definido**, recibir **solo los datos necesarios** y retornar **un resultado claro**.

## 🚨 8. Evitar que un error detenga todo el programa
Una **excepción** es una situación que impide que el programa siga normalmente (por
ejemplo, convertir `"tres"` a número). Manejarla con `try`/`except` evita que el programa
se caiga de golpe; `raise` sirve para lanzar una excepción propia cuando una regla de
negocio se rompe.

```python
try:
    estimated_hours = int(input("Horas estimadas: "))
    print(f"Horas: {estimated_hours}")
except ValueError:
    print("Debe ingresar un número")

if estimated_hours <= 0:
    raise ValueError("Las horas deben ser positivas")
```

| Buena práctica | Por qué |
|---|---|
| Captura excepciones específicas (`except ValueError`) | `except:` genérico también atrapa errores que no esperabas y esconde bugs reales. |
| Mensajes claros | El usuario debe entender qué salió mal y cómo corregirlo. |
| No ocultar errores inesperados | Los errores silenciosos dificultan el diagnóstico más adelante. |

> ⚠️ `except:` sin especificar el tipo de error es una mala práctica común — atrapa
> absolutamente todo (incluso errores de programación) y hace muy difícil depurar.

# 🔬 PARA IR MÁS ALLÁ — profundizando rumbo a Backend

> 📌 Esto **no se vio en esta clase** — lo agrego por mi cuenta sobre la misma
> base de la Clase 1, porque son los primeros huecos que aparecen apenas se empieza a
> pensar en construir un backend de verdad (una API, una base de datos, un servicio en
> producción). Todo el código está verificado en terminal.

## 🧬 9. Mutabilidad y aliasing: el bug más común en backend
En la teoría vimos que las listas y diccionarios son mutables. La consecuencia práctica
(y la fuente de un bug clásico) es que **una variable no "contiene" el dato: apunta a
él**. Si paso una lista/diccionario a una función y la función lo modifica *en el mismo
lugar* (sin reasignarlo), el cambio se ve también afuera — aunque nunca hice `return`.

```python
def add_processed_tag(requests_list):
    for r in requests_list:
        r["tag"] = "revisado"   # modifica el diccionario EN SU LUGAR
    return requests_list

original = [{"id": 1001, "priority": "Alta"}]
result = add_processed_tag(original)

print(original)          # también quedó con 'tag' — no hizo falta reasignar nada
print(result is original)  # True: es el MISMO objeto en memoria, no una copia
```
```
[{'id': 1001, 'priority': 'Alta', 'tag': 'revisado'}]
True
```

En cambio, si dentro de la función **reasigno** el parámetro a algo nuevo (`requests_list
= []`), esa reasignación es local — no afecta a la variable de quien llamó a la función:

```python
def try_replace(requests_list):
    requests_list = []              # esto crea una lista NUEVA, solo local
    requests_list.append({"id": 9999})
    return requests_list

other = [{"id": 1}]
new_list = try_replace(other)
print(other)     # [{'id': 1}]  -- sin cambios
print(new_list)  # [{'id': 9999}]
```

> ⚠️ En una API, este es el bug que aparece cuando una función "de validación" termina
> modificando el payload original sin querer, y otro endpoint más adelante recibe datos
> ya alterados. La regla de oro: si no querés efectos secundarios, trabajá sobre una
> copia (`list(original)`, `dict(original)`, o el módulo `copy` para copias profundas).

## 🏷️ 10. Tipos más expresivos: `Optional` y anotaciones modernas
En la teoría usamos `priority: str -> int`. En backend real, muchos campos son
**opcionales** (pueden no venir en la petición). Desde Python 3.10 se anota así, con `|
None` en vez de `Optional[...]` de `typing`:

```python
def build_summary(title: str, hours: float | None = None) -> str:
    if hours is None:
        return f"{title} (sin estimar)"
    return f"{title} ({hours}h)"

print(build_summary("Error de acceso"))
print(build_summary("Falla de red", 2.5))
```
```
Error de acceso (sin estimar)
Falla de red (2.5h)
```

> 🧪 Tip de entrevista: `str | None` y `Optional[str]` (de `from typing import Optional`)
> significan exactamente lo mismo — la sintaxis con `|` es la forma moderna (3.10+) y la
> que vas a ver en proyectos con FastAPI/Pydantic.

## 📦 11. `dataclass`: estructurar una entidad sin tanto diccionario suelto
Hasta ahora representamos una solicitud como `dict`. Funciona, pero nada impide escribir
`request["titel"]` (con un typo) y que Python no avise hasta que falle en producción. Una
**`dataclass`** define la forma de un objeto una sola vez, con tipos, y el editor avisa
si te equivocás de nombre de campo:

```python
from dataclasses import dataclass, field

@dataclass
class SupportRequest:
    id: int
    title: str
    priority: str
    tags: list[str] = field(default_factory=list)  # evita el bug del valor por defecto mutable

r1 = SupportRequest(id=1001, title="Error de acceso", priority="Alta")
print(r1)             # SupportRequest(id=1001, title='Error de acceso', priority='Alta', tags=[])
r1.tags.append("urgente")
print(r1.tags)         # ['urgente']
```

Y si necesito que un objeto **no se pueda modificar después de creado** (útil para datos
que no deberían cambiar, como un ID ya asignado), existe la variante `frozen`:

```python
@dataclass(frozen=True)
class ImmutableRequest:
    id: int
    title: str

r2 = ImmutableRequest(id=1, title="Solo lectura")
r2.id = 2   # FrozenInstanceError: cannot assign to field 'id'
```

> 💡 Esto es, literalmente, el paso previo a los `BaseModel` de **Pydantic** que vamos a
> usar en la Clase 3 (FastAPI) — misma idea (definir la forma de los datos con tipos),
> pero Pydantic además valida en tiempo de ejecución (por ejemplo, rechaza un `priority`
> que no sea texto).

## 🚨 12. Excepciones propias: modelar errores del dominio
En la teoría usamos `ValueError` para todo. En un backend más grande conviene crear
**excepciones propias**, organizadas en una jerarquía, para poder distinguir "no
encontrado" de "dato inválido" y capturarlas por separado (o todas juntas, por el error
base):

```python
class DomainError(Exception):
    """Error base para reglas de negocio del dominio."""

class RequestNotFoundError(DomainError):
    def __init__(self, request_id: int):
        self.request_id = request_id
        super().__init__(f"Solicitud {request_id} no encontrada")

class InvalidPriorityError(DomainError):
    pass

def find_request(requests_list, request_id):
    for r in requests_list:
        if r["id"] == request_id:
            return r
    raise RequestNotFoundError(request_id)

requests_db = [{"id": 1001, "priority": "Alta"}]
try:
    find_request(requests_db, 9999)
except RequestNotFoundError as e:
    print(e)   # Solicitud 9999 no encontrada
```

> 📌 Como `RequestNotFoundError` **hereda** de `DomainError`, un `except DomainError`
> también la captura — así una API puede tener un único manejador para "cualquier error
> de negocio" y devolver el código HTTP correcto según el tipo exacto de excepción
> (`RequestNotFoundError` → 404, `InvalidPriorityError` → 400). Esto es exactamente lo
> que se arma con los `exception_handlers` de FastAPI más adelante en el curso.

## 🪵 13. `logging` en vez de `print` en servicios reales
`print()` está perfecto para practicar, pero un backend corriendo en un servidor no tiene
a nadie mirando la consola en vivo — necesita **quedar registrado**, con nivel de
severidad y timestamp, en un log que se pueda revisar después.

```python
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("soporte")

logger.info("Solicitud 1001 procesada")
logger.warning("Solicitud 1002 sin prioridad asignada")
```
```
INFO: Solicitud 1001 procesada
WARNING: Solicitud 1002 sin prioridad asignada
```

| Nivel | Cuándo usarlo |
|---|---|
| `DEBUG` | Detalle solo útil mientras se desarrolla/depura. |
| `INFO` | Eventos normales del negocio ("solicitud creada", "usuario autenticado"). |
| `WARNING` | Algo raro pero el programa sigue funcionando. |
| `ERROR` | Algo falló y hay que revisarlo. |
| `CRITICAL` | El servicio no puede seguir operando. |

## 🔐 14. Variables de entorno: no hardcodear configuración sensible
La URL de una base de datos, una API key, una contraseña — **nunca** van escritas
directamente en el código. Se leen del entorno del sistema operativo con `os.environ`,
normalmente cargadas desde un archivo `.env` (que **no** se sube a git):

```python
import os

db_host = os.environ.get("DB_HOST", "127.0.0.1")  # usa un valor por defecto si no existe
db_port = os.environ.get("DB_PORT", "5432")
print(f"Conectando a {db_host}:{db_port}")
```

> ⚠️ Si algún día ves un `.env` con credenciales reales, va en el `.gitignore` — **nunca**
> se commitea. En este mismo repo el `.gitignore` (raíz del proyecto) ya excluye
> archivos que no deben ir a git (entornos virtuales, cachés, etc.).

## ⚡ 15. Comprehensions: transformar listas de diccionarios sin tanto `for`
Es el patrón que más se repite al procesar el resultado de una consulta (una lista de
diccionarios, como vimos en la teoría): filtrar y/o transformar en una sola línea.

```python
requests_list = [
    {"id": 1001, "priority": "Alta"},
    {"id": 1002, "priority": "Media"},
    {"id": 1003, "priority": "Alta"},
]

solo_altas = [r["id"] for r in requests_list if r["priority"] == "Alta"]
print(solo_altas)  # [1001, 1003]

mapa_prioridades = {r["id"]: r["priority"] for r in requests_list}
print(mapa_prioridades)  # {1001: 'Alta', 1002: 'Media', 1003: 'Alta'}
```

> 💡 Es exactamente el mismo resultado que el `for` con `if` y `append()` de la teoría
> (sección 6/7) — una comprehension no es "magia", es azúcar sintáctico para ese mismo
> patrón, más compacto.

# 💻 PARTE PRÁCTICA

> 📝 **`request_utils.py` sin documentar:** el reto de cierre que se documentaba acá
> (`request_utils.py` + `main.py`, "procesador de solicitudes de soporte") no
> correspondía en realidad a esta clase — al revisar la grabación, `main.py` era otro
> ejercicio (ver más abajo). `request_utils.py` queda en la carpeta sin usarse por
> ahora; se retoma si el reto real aparece en una clase siguiente.

## 🖊️ Práctica libre: variables e `input()`
Aparte del reto, practiqué por mi cuenta variables y la función `input()` — que ya había
aparecido de pasada en el ejemplo de `try`/`except` de la teoría (sección 8), pero acá la
uso directamente para pedirle datos al usuario por consola.

| Archivo | Qué practica |
|---|---|
| [`02-Ejercicios/Clase-01/variables.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-01/variables.py) | Declarar variables, `print()` con varios argumentos, sumar variables numéricas |
| [`02-Ejercicios/Clase-01/input.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-01/input.py) | `input()` para leer texto del usuario y concatenarlo con `+` |
| [`02-Ejercicios/Clase-01/temperatura.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-01/temperatura.py) | `input()` + conversión a `float` + `str()` para insertar un número en un texto |
| [`02-Ejercicios/Clase-01/calenda.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-01/calenda.py) | Módulo `calendar` de la librería estándar — imprime el calendario de un mes |

> 📌 `input()` **siempre devuelve texto (`str`)**, aunque el usuario escriba un número —
> por eso `temperatura.py` lo envuelve en `float(...)` antes de usarlo como número (el
> mismo patrón de conversión de tipos de la sección 4 de la teoría).

```python
# calenda.py
import calendar

print(calendar.month(2026, 8))
```
```
    August 2026
Mo Tu We Th Fr Sa Su
                1  2
 3  4  5  6  7  8  9
10 11 12 13 14 15 16
17 18 19 20 21 22 23
24 25 26 27 28 29 30
31
```

> 📝 `calendar` es parte de la **librería estándar** de Python — viene incluido, se usa
> con `import` directo, sin `pip install`. Intenté antes `pip install python3-calendar`
> y falló (`Could not find a version that satisfies the requirement`): ese nombre
> `python3-algo` es la convención de paquetes de **apt/Debian/Ubuntu**, no de
> PyPI/`pip` — dos ecosistemas de paquetes distintos. Ver [00-Notas/01-Comandos.md](../00-Notas/01-Comandos.md).

<div class="terminal-shot">
  <div class="terminal-shot__titlebar">
    <span class="terminal-shot__dot terminal-shot__dot--red"></span>
    <span class="terminal-shot__dot terminal-shot__dot--yellow"></span>
    <span class="terminal-shot__dot terminal-shot__dot--green"></span>
    <span class="terminal-shot__title">zsh · variables.py / input.py / temperatura.py</span>
  </div>
  <pre class="terminal-shot__screen"><code><span class="terminal-shot__prompt">$</span> python3 variables.py
<span class="terminal-shot__output">Mi edad es: 25
La suma de edades es: 55
El valor total es de: 30</span>
<span class="terminal-shot__prompt">$</span> python3 input.py
Ingrese su nombre: Styp
<span class="terminal-shot__output">Hola, Styp! Bienvenido/a a la clase de Python.</span>
<span class="terminal-shot__prompt">$</span> python3 temperatura.py
Ingrese la temperatura del lunes: 18.5
<span class="terminal-shot__output">La temperatura del lunes es: 18.5°C</span></code></pre>
</div>

## 🖊️ Práctica libre: variables sueltas, listas y diccionarios
Siguiendo con la práctica libre, repetí el mismo dato (una "solicitud") de tres formas
distintas — primero como variables sueltas, después agrupado en una lista y en un
diccionario, y por último combinando lista + diccionario — para comparar en carne propia
la diferencia que explica la teoría (sección 5: "Agrupando información relacionada").

| Archivo | Qué practica |
|---|---|
| [`02-Ejercicios/Clase-01/main2.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-01/main2.py) | Variables sueltas (`request_id`, `request_title`, ...) — el dato **sin agrupar**, cada pieza en su propia variable |
| [`02-Ejercicios/Clase-01/lista.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-01/lista.py) | Una `list` simple (`categoria`) y cómo imprimirla dentro de un texto con `str(...)` |
| [`02-Ejercicios/Clase-01/diccionario.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-01/diccionario.py) | Un `dict` (`request`) — el mismo dato de `main2.py`, pero agrupado y accedido por clave (`request['id']`) |
| [`02-Ejercicios/Clase-01/listadediccionarios.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-01/listadediccionarios.py) | Una **lista de diccionarios** (dos solicitudes) recorrida con `for` — el patrón que más se repite en Backend |

```python
# main2.py — variables sueltas, sin agrupar
request_id = 1001
request_title = "Clase 01 - Ejercicios"
request_estimated_hours = 2.5
request_is_active = True
request_assigned_user = "styp"

print(f"Request ID: {request_id}")
```

```python
# diccionario.py — el mismo dato, pero agrupado en un dict
request = {
    "id": 1001,
    "title": "Clase 01 - Ejercicios",
    "estimated_hours": 2.5,
    "is_active": True,
    "assigned_user": "styp"}

print(f"Request ID: {request['id']}")
print(f"Request Title: {request['title']}")
print(f"Estimated Hours: {request['estimated_hours']}")
```

```python
# listadediccionarios.py — varias solicitudes, cada una un dict, recorridas con for
request = [
    {"id": 1001, "title": "Clase 01 - Ejercicios", "estimated_hours": 2.5,
     "is_active": True, "assigned_user": "styp"},
    {"id": 1002, "title": "Clase 02 - Ejercicios", "estimated_hours": 3.0,
     "is_active": False, "assigned_user": "jdoe"},
]

for req in request:
    print(f"Request ID: {req['id']}")
    print(f"Request Title: {req['title']}")
    print(f"Estimated Hours: {req['estimated_hours']}")
    print(f"Is Active: {req['is_active']}")
    print(f"Assigned User: {req['assigned_user']}")
    print()
```

> 📌 Comparando `main2.py` con `diccionario.py` se ve exactamente lo que dice la teoría
> (sección 5): con variables sueltas, si tuviera 10 solicitudes necesitaría 50 variables
> con nombres distintos (`request_id_1`, `request_id_2`...); con un `dict` por solicitud
> y una `list` para agruparlas (`listadediccionarios.py`), agregar una solicitud más es
> solo agregar un elemento a la lista — el `for` ya sabe recorrerlas todas sin importar
> cuántas sean.

<div class="terminal-shot">
  <div class="terminal-shot__titlebar">
    <span class="terminal-shot__dot terminal-shot__dot--red"></span>
    <span class="terminal-shot__dot terminal-shot__dot--yellow"></span>
    <span class="terminal-shot__dot terminal-shot__dot--green"></span>
    <span class="terminal-shot__title">zsh · main2.py / lista.py / diccionario.py / listadediccionarios.py</span>
  </div>
  <pre class="terminal-shot__screen"><code><span class="terminal-shot__prompt">$</span> python3 main2.py
<span class="terminal-shot__output">Request ID: 1001</span>
<span class="terminal-shot__prompt">$</span> python3 lista.py
<span class="terminal-shot__output">Categorías disponibles:['Electrónica', 'Ropa', 'Libros']</span>
<span class="terminal-shot__prompt">$</span> python3 diccionario.py
<span class="terminal-shot__output">Request ID: 1001
Request Title: Clase 01 - Ejercicios
Estimated Hours: 2.5</span>
<span class="terminal-shot__prompt">$</span> python3 listadediccionarios.py
<span class="terminal-shot__output">Request ID: 1001
Request Title: Clase 01 - Ejercicios
Estimated Hours: 2.5
Is Active: True
Assigned User: styp
&nbsp;
Request ID: 1002
Request Title: Clase 02 - Ejercicios
Estimated Hours: 3.0
Is Active: False
Assigned User: jdoe</span></code></pre>
</div>

> 💡 Detalle de estilo en `lista.py`: `"texto" + str(categoria)` funciona, pero mezclar
> `+` con `str(...)` a mano es justo lo que resuelve más limpio un f-string —
> `f"Categorías disponibles: {categoria}"` da el mismo resultado sin el `+` ni el
> `str()` explícito (mismo patrón ya usado en `diccionario.py` y en la teoría, sección 7).

## 🔐 `contrasena.py` — comparar strings ignorando mayúsculas
Enunciado: almacenar la cadena `holamundo` en una variable, pedirle al usuario su
contraseña e imprimir si coincide con la guardada, **sin distinguir mayúsculas de
minúsculas**.

```python
contrasena_bd = "holamundo"
contrasena_usuario = input("Ingrese la contraseña del usuario: ")

if contrasena_usuario.lower() == contrasena_bd.lower():
    print("La contraseña es correcta")
else:
    print("La contraseña es incorrecta")
```

<div class="terminal-shot">
  <div class="terminal-shot__titlebar">
    <span class="terminal-shot__dot terminal-shot__dot--red"></span>
    <span class="terminal-shot__dot terminal-shot__dot--yellow"></span>
    <span class="terminal-shot__dot terminal-shot__dot--green"></span>
    <span class="terminal-shot__title">zsh · contrasena.py</span>
  </div>
  <pre class="terminal-shot__screen"><code><span class="terminal-shot__prompt">$</span> python3 contrasena.py
Ingrese la contraseña del usuario: holamundo
<span class="terminal-shot__output">La contraseña es correcta</span>
<span class="terminal-shot__prompt">$</span> python3 contrasena.py
Ingrese la contraseña del usuario: HOLAMUNDO
<span class="terminal-shot__output">La contraseña es correcta</span>
<span class="terminal-shot__prompt">$</span> python3 contrasena.py
Ingrese la contraseña del usuario: otraclave
<span class="terminal-shot__output">La contraseña es incorrecta</span></code></pre>
</div>

> 📝 **Corrección aplicada al revisar el enunciado:** la primera versión comparaba
> `contrasena_usuario == contrasena_bd` directo, que **sí distingue mayúsculas de
> minúsculas** — con `"HOLAMUNDO"` daba "incorrecta" cuando el enunciado pedía que diera
> "correcta". Se corrigió normalizando ambos lados con `.lower()` antes de comparar
> (`.casefold()` sería la alternativa más robusta si hubiera tildes/ñ).

> ⚠️ Comparar texto plano contra texto plano es perfecto para practicar `==` con
> strings, pero **nunca** así en un backend real: las contraseñas se guardan
> **hasheadas** (nunca en texto plano) y se comparan con funciones resistentes a
> *timing attacks* (p. ej. `bcrypt`, o `hmac.compare_digest` en la librería estándar).
> Este patrón de "hashear y verificar credenciales" se retoma en las clases de
> autenticación/JWT del curso (Clase 7).

## 👤 `main.py` — condicional simple: ¿puede jubilarse?
Enunciado: dada la edad de un empleado, indicar si puede jubilarse (regla: 65 años o
más).

```python
input_edad = input("Ingrese la edad del empleado: ")
edad = int(input_edad)

if edad >= 65:
    print("El empleado puede jubilarse")
    print("El empleado tiene " + str(edad) + " años")
else:
    print("El empleado no puede jubilarse")
    print("El empleado tiene " + str(edad) + " años")
```

<div class="terminal-shot">
  <div class="terminal-shot__titlebar">
    <span class="terminal-shot__dot terminal-shot__dot--red"></span>
    <span class="terminal-shot__dot terminal-shot__dot--yellow"></span>
    <span class="terminal-shot__dot terminal-shot__dot--green"></span>
    <span class="terminal-shot__title">zsh · main.py</span>
  </div>
  <pre class="terminal-shot__screen"><code><span class="terminal-shot__prompt">$</span> python3 main.py
Ingrese la edad del empleado: 70
<span class="terminal-shot__output">El empleado puede jubilarse
El empleado tiene 70 años</span>
<span class="terminal-shot__prompt">$</span> python3 main.py
Ingrese la edad del empleado: 50
<span class="terminal-shot__output">El empleado no puede jubilarse
El empleado tiene 50 años</span></code></pre>
</div>

> 📌 `edad = int(input_edad)` repite el patrón de conversión de tipos de la sección 4 de
> la teoría (`input()` siempre devuelve `str`, hay que convertirlo explícito antes de
> comparar con `>= 65`).

## 💰 `impuestos.py` — condicional con cálculo
Enunciado: para tributar un impuesto hay que ser mayor de 16 años y tener ingresos
mensuales — el programa pregunta la edad y el salario, y muestra si corresponde
tributar (18% del salario) o no.

```python
salario = float(input("Ingrese su salario: "))
edad = int(input("Ingrese su edad: "))

if edad >= 16:
    print(f"Tiene que tributar, le corresponde {salario * 0.18} soles")
else:
    print("Aun no tiene que tributar")
```

<div class="terminal-shot">
  <div class="terminal-shot__titlebar">
    <span class="terminal-shot__dot terminal-shot__dot--red"></span>
    <span class="terminal-shot__dot terminal-shot__dot--yellow"></span>
    <span class="terminal-shot__dot terminal-shot__dot--green"></span>
    <span class="terminal-shot__title">zsh · impuestos.py</span>
  </div>
  <pre class="terminal-shot__screen"><code><span class="terminal-shot__prompt">$</span> python3 impuestos.py
Ingrese su salario: 1500
Ingrese su edad: 20
<span class="terminal-shot__output">Tiene que tributar, le corresponde 270.0 soles</span>
<span class="terminal-shot__prompt">$</span> python3 impuestos.py
Ingrese su salario: 1500
Ingrese su edad: 10
<span class="terminal-shot__output">Aun no tiene que tributar</span></code></pre>
</div>

> 💡 Mismo patrón que `main.py`: un `if`/`else` sobre un valor convertido con
> `int()`/`float()` — acá además se **calcula** un resultado (`salario * 0.18`) dentro
> de la rama verdadera, en vez de solo imprimir un mensaje fijo.

## 🦸 `superheroes.py` — añadir, eliminar y reemplazar en una lista

> 📚 **¿Qué es una lista y para qué sirve?** Una `list` en Python es una **colección
> ordenada y mutable** de elementos — guarda varios valores (strings, números, lo que
> sea) en una sola variable, en un orden que se mantiene, y se puede modificar después
> de creada (a diferencia de un `str` o una `tuple`). Sirve para cualquier caso donde
> tengas "varias cosas del mismo tipo": una lista de tareas, de héroes, de solicitudes,
> de nombres de usuarios. Se accede por **índice** (posición), empezando en `0`:
> ```python
> avengers = ["Iron Man", "Thor", "Hulk"]
> avengers[0]        # "Iron Man" (primer elemento, índice 0)
> len(avengers)       # 3 (cantidad de elementos)
> ```
> Definición completa (con tabla comparando `list` vs. `dict`) en
> [[Clase-01#🖊️-practica-libre-variables-sueltas-listas-y-diccionarios]] más arriba.
>
> Métodos usados en este ejercicio:
>
> | Método | Qué hace |
> |---|---|
> | `.append(x)` | Agrega `x` al **final** de la lista. |
> | `.remove(x)` | Elimina la **primera aparición** del valor `x` (no por posición). |
> | `.index(x)` | Devuelve la **posición** (índice) donde está `x`, para poder reemplazarlo: `lista[lista.index(x)] = nuevo_valor`. |

Enunciado: dada la lista de héroes de los Vengadores, (1) agregar a Spider-Man, (2)
eliminar a Thor y (3) reemplazar a Capitán América por Pantera Negra.

> 📝 **Bug del editor de la plataforma:** al reiniciar el ejercicio, el editor fue
> devolviendo distintas listas de arranque en cada intento — ninguna coincidía del todo
> con el enunciado (`["Iron Man", "pantera negra", "spider man", ...]`,
> `["Iron Man", "Pantera negra", ..., "Spider Man"]`, etc., con nombres mal escritos o
> sin Thor/Capitán América). La versión final se resolvió con la lista original que da
> por sentada el enunciado de texto, para poder aplicar los tres pasos pedidos
> literalmente (agregar, eliminar, reemplazar) en vez de ir parchando errores de
> tipeo del editor.

```python
# Lista original de héroes de los Vengadores
avengers = ["Iron Man", "Capitán América", "Thor", "Hulk", "Viuda Negra"]

# Agregar a Spider-Man
avengers.append("Spider-Man")

# Eliminar a Thor
avengers.remove("Thor")

# Reemplazar a Capitán América con Pantera Negra
avengers[avengers.index("Capitán América")] = "Pantera Negra"

# La lista final de héroes de los Vengadores
print("La lista final de héroes:", avengers)
```

<div class="terminal-shot">
  <div class="terminal-shot__titlebar">
    <span class="terminal-shot__dot terminal-shot__dot--red"></span>
    <span class="terminal-shot__dot terminal-shot__dot--yellow"></span>
    <span class="terminal-shot__dot terminal-shot__dot--green"></span>
    <span class="terminal-shot__title">zsh · superheroes.py</span>
  </div>
  <pre class="terminal-shot__screen"><code><span class="terminal-shot__prompt">$</span> python3 superheroes.py
<span class="terminal-shot__output">La lista final de héroes: ['Iron Man', 'Pantera Negra', 'Hulk', 'Viuda Negra', 'Spider-Man']</span></code></pre>
</div>

| Método | Qué hace | Detalle a notar |
|---|---|---|
| `.append("Spider-Man")` | Agrega al final de la lista. | Coincide con la salida esperada: Spider-Man queda último. |
| `.remove("Thor")` | Elimina la **primera aparición** del valor dado. | No hace falta saber la posición, solo el valor exacto. |
| `avengers[avengers.index("Capitán América")] = "Pantera Negra"` | Busca el índice del valor y reemplaza en ese lugar. | `.index()` evita hardcodear la posición (`avengers[1] = ...` también funcionaría, pero es frágil si el orden cambia). |

## 🔁 `ciclos.py` — recorrer una lista con `while`
Enunciado: dada una lista de solicitudes (diccionarios con `id` y `title`), imprimir el
`id` de cada una usando un bucle `while` (no `for`).

```python
lista_solicitudes = [
    {"id": 1001, "title": "Error de acceso 1"},
    {"id": 1002, "title": "Error de acceso 2"},
    {"id": 1003, "title": "Error de acceso 3"},
]

contador = 0
while contador < 3:
    print(lista_solicitudes[contador].get("id"))
    contador = contador + 1
```

<div class="terminal-shot">
  <div class="terminal-shot__titlebar">
    <span class="terminal-shot__dot terminal-shot__dot--red"></span>
    <span class="terminal-shot__dot terminal-shot__dot--yellow"></span>
    <span class="terminal-shot__dot terminal-shot__dot--green"></span>
    <span class="terminal-shot__title">zsh · ciclos.py</span>
  </div>
  <pre class="terminal-shot__screen"><code><span class="terminal-shot__prompt">$</span> python3 ciclos.py
<span class="terminal-shot__output">1001
1002
1003</span></code></pre>
</div>

> 💡 `.get("id")` devuelve el valor de la clave `"id"` igual que `["id"]`, pero sin
> lanzar `KeyError` si la clave no existiera (devolvería `None`) — más seguro cuando no
> se está 100% seguro de que la clave siempre está presente.
>
> ⚠️ El `while` acá funciona porque el largo de la lista (`3`) está *hardcodeado* en la
> condición — si `lista_solicitudes` tuviera un elemento más, el bucle lo ignoraría. La
> versión robusta sería `while contador < len(lista_solicitudes):`, o directamente usar
> `for` (ver `listasolicitudes.py` a continuación), que no depende de un contador manual.

## 📋 `listasolicitudes.py` — recorrer una lista con `for`
Enunciado: la misma lista de solicitudes de `ciclos.py`, pero recorrida con `for` en vez
de `while`, imprimiendo el `title` de cada una.

```python
lista_solicitudes = [
    {"id": 1001, "title": "Error de acceso 1"},
    {"id": 1002, "title": "Error de acceso 2"},
    {"id": 1003, "title": "Error de acceso 3"},
]

for solicitud in lista_solicitudes:
    print(solicitud["title"])
```

<div class="terminal-shot">
  <div class="terminal-shot__titlebar">
    <span class="terminal-shot__dot terminal-shot__dot--red"></span>
    <span class="terminal-shot__dot terminal-shot__dot--yellow"></span>
    <span class="terminal-shot__dot terminal-shot__dot--green"></span>
    <span class="terminal-shot__title">zsh · listasolicitudes.py</span>
  </div>
  <pre class="terminal-shot__screen"><code><span class="terminal-shot__prompt">$</span> python3 listasolicitudes.py
<span class="terminal-shot__output">Error de acceso 1
Error de acceso 2
Error de acceso 3</span></code></pre>
</div>

> 📌 Comparado con `ciclos.py`: el `for` no necesita contador ni condición de corte —
> recorre exactamente los elementos que haya, ni uno más ni uno menos. Por eso en
> Python se prefiere `for` sobre `while` para recorrer colecciones, y se reserva `while`
> para "repetir hasta que pase algo" sin saber de antemano cuántas vueltas van a ser.

## 🧮 `calculadora.py` — función con `if/elif` por operador
Enunciado: definir una función que reciba dos números (`a`, `b`) y una operación
(`+`, `-`, `*`, `/`), y devuelva el resultado. La rama de `/` ya venía en el código
como referencia, con el caso de división por cero.

```python
def calculadora(a, b, operation):
    if operation == '/':
        if b != 0:
            # a % b es el resto de la división. Si el resto es 0, "a" se
            # divide exacto entre "b" (ej: 8 / 4 = 2.0, resto 0).
            # Si el resto NO es 0, la división no es exacta (ej: 37 / 8 =
            # 4.625, resto 5) -> avisamos en vez de solo mostrar el decimal.
            if a % b == 0:
                return a / b
            else:
                return f"{a} no es divisible entre {b}"
        else:
            return "Error: ¡Intentando dividir por cero!"
    elif operation == '+':
        return a + b
    elif operation == '-':
        return a - b
    elif operation == '*':
        return a * b
    else:
        # Si el usuario escribe algo distinto de +, -, *, /, ninguno de los
        # if/elif de arriba se cumple. Sin este 'else', la función no haría
        # ningún 'return' y devolvería None -> se imprimiría "Resultado: None"
        # sin explicar qué pasó. Mismo patrón que el error de división por
        # cero: devolver un mensaje claro en vez de un None silencioso.
        return "Error: operación no válida. Usa +, -, * o /."

# Solicitar al usuario los números y el tipo de operación
a = float(input("Ingresa el primer número: "))
b = float(input("Ingresa el segundo número: "))
operation = input("Especifica la operación que deseas realizar (+, -, *, /): ")

# Llamando a la función 'calculadora' y mostrando el resultado
result = calculadora(a, b, operation)
print("Resultado:", result)
```

<div class="terminal-shot">
  <div class="terminal-shot__titlebar">
    <span class="terminal-shot__dot terminal-shot__dot--red"></span>
    <span class="terminal-shot__dot terminal-shot__dot--yellow"></span>
    <span class="terminal-shot__dot terminal-shot__dot--green"></span>
    <span class="terminal-shot__title">zsh · calculadora.py</span>
  </div>
  <pre class="terminal-shot__screen"><code><span class="terminal-shot__prompt">$</span> python3 calculadora.py
Ingresa el primer número: 34
Ingresa el segundo número: 12
Especifica la operación que deseas realizar (+, -, *, /): *
<span class="terminal-shot__output">Resultado: 408.0</span>
<span class="terminal-shot__prompt">$</span> python3 calculadora.py
Ingresa el primer número: 37
Ingresa el segundo número: 8
Especifica la operación que deseas realizar (+, -, *, /): /
<span class="terminal-shot__output">Resultado: 37.0 no es divisible entre 8.0</span></code></pre>
</div>

| Caso | Qué pasa | Detalle a notar |
|---|---|---|
| `b == 0` en `/` | Devuelve `"Error: ¡Intentando dividir por cero!"` | Venía como referencia en el enunciado original. |
| `a % b != 0` en `/` | Devuelve `"{a} no es divisible entre {b}"` en vez del decimal. | `%` es el operador **módulo** (resto de la división); si el resto no es 0, la división no es exacta. Mejora agregada sobre el enunciado original. |
| `operation` no es `+ - * /` | Devuelve `"Error: operación no válida..."` | Sin este `else`, la función devolvía `None` de forma silenciosa (ningún `if/elif` se cumplía) y el programa imprimía `Resultado: None` sin explicar qué pasó. |

> 📝 **Detalle de nombres:** la función se llama `calculadora` (no `calculate`, como
> sugería el enunciado en inglés) — mismo comportamiento, nombre en español para ser
> consistente con el resto de los ejercicios de la clase.

## 🚨 `try-except.py` — capturar `ValueError` al convertir un dato
Enunciado: pedir la edad del usuario y convertirla a número, avisando (sin cortar el
programa) si el valor ingresado no es numérico.

```python
try:
    edad = int(input("Ingrese su edad: "))
except ValueError:
    print("Debe ingresar un valor numérico")
```

<div class="terminal-shot">
  <div class="terminal-shot__titlebar">
    <span class="terminal-shot__dot terminal-shot__dot--red"></span>
    <span class="terminal-shot__dot terminal-shot__dot--yellow"></span>
    <span class="terminal-shot__dot terminal-shot__dot--green"></span>
    <span class="terminal-shot__title">zsh · try-except.py</span>
  </div>
  <pre class="terminal-shot__screen"><code><span class="terminal-shot__prompt">$</span> python3 try-except.py
Ingrese su edad: 25
<span class="terminal-shot__prompt">$</span> python3 try-except.py
Ingrese su edad: veinticinco
<span class="terminal-shot__output">Debe ingresar un valor numérico</span></code></pre>
</div>

> 💡 Es la versión mínima, hecha a mano, del mismo patrón de la teoría (sección 8) y de
> `contrasena.py`/`impuestos.py` más arriba: cualquier `int(input(...))` puede fallar si
> el usuario escribe texto, y `try`/`except ValueError` evita que ese error tumbe todo
> el programa.

## ❓ Preguntas y respuestas (autoevaluación)

**1. ¿Qué es el Backend, con tus palabras?**
> Es la parte de una aplicación que el usuario no ve directamente: recibe datos, aplica
> reglas de negocio, valida, consulta o guarda información, gestiona permisos y responde.

**2. ¿Por qué se usa un entorno virtual (`venv`) en vez de instalar las librerías
directamente en el sistema?**
> Para aislar las dependencias de cada proyecto — así dos proyectos pueden usar versiones
> distintas de una misma librería sin chocar entre sí.

**3. ¿Qué tipo devuelve `type("1001")`? ¿Y `type(2.5)`?**
> `str` (porque tiene comillas, es texto) y `float` respectivamente.

**4. ¿Cuál es la diferencia entre una lista y un diccionario?**
> La lista es una colección **ordenada** que se accede por posición (índice); el
> diccionario se accede por **clave** (nombre), no por posición.

**5. Si `priorities = ["Alta", "Baja", "Alta"]` y sumo 1 a `total` por cada `"Alta"`,
¿cuántas veces se suma?**
> 2 veces — solo cuando la condición del `if` dentro del `for` se cumple.

**6. ¿Cuál es la diferencia entre `for` y `while`?**
> `for` recorre una colección elemento a elemento (se sabe de antemano cuántas vueltas
> da); `while` repite mientras una condición sea verdadera (no se sabe de antemano
> cuántas vueltas van a ser).

**7. ¿Para qué sirven los type hints (`priority: str`, `-> int`) en una función?**
> Para dejar explícito qué tipo de dato espera la función y qué tipo devuelve — ayuda a
> leer el código y a que el editor avise de errores antes de ejecutar. No son obligatorios
> ni Python los valida en tiempo de ejecución.

**8. ¿Por qué es mala práctica usar `except:` sin especificar el tipo de error?**
> Porque atrapa absolutamente cualquier error (incluso errores de programación que no
> tienen que ver con lo que se quería manejar) y eso hace muy difícil detectar bugs reales.

**9. ¿Cuándo conviene mover una función a un módulo separado en vez de dejarla en
`main.py`?**
> Cuando se va a reutilizar en más de un archivo — por ejemplo, la misma función de
> cálculo que usa un script de consola después la puede usar una API.

**10. En `contrasena.py`, ¿por qué `contrasena_usuario == contrasena_bd` no era
suficiente para cumplir el enunciado, y qué lo corrige?**
> Porque `==` sobre strings distingue mayúsculas de minúsculas — `"HOLAMUNDO" ==
> "holamundo"` da `False`. El enunciado pedía ignorar esa diferencia, así que hay que
> normalizar ambos lados antes de comparar: `contrasena_usuario.lower() ==
> contrasena_bd.lower()`.

## 📎 Apuntes relacionados
- [00-Notas/02-Conceptos.md](../00-Notas/02-Conceptos.md) — tabla de conceptos (tipos de
  datos, entorno virtual, manejo de errores).
- [00-Notas/01-Comandos.md](../00-Notas/01-Comandos.md) — comandos de `venv` y `pip`.

## ➡️ Siguiente
[Clase 2](Clase-02.md)
