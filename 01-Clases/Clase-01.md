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

El reto de cierre de la clase: **procesador de solicitudes de soporte**. Un programa que
recorre una lista de solicitudes y determina, para cada una, su tiempo máximo de
respuesta — juntando todo lo visto (listas de diccionarios, `for`, función en módulo
separado, `try`/`except`).

Archivos: `02-Ejercicios/Clase-01/request_utils.py` (la función) y
`02-Ejercicios/Clase-01/main.py` (el programa principal).

Para correrlo:
```bash
cd 02-Ejercicios/Clase-01
python3 main.py
```

<div class="terminal-shot">
  <div class="terminal-shot__titlebar">
    <span class="terminal-shot__dot terminal-shot__dot--red"></span>
    <span class="terminal-shot__dot terminal-shot__dot--yellow"></span>
    <span class="terminal-shot__dot terminal-shot__dot--green"></span>
    <span class="terminal-shot__title">zsh · main.py</span>
  </div>
  <pre class="terminal-shot__screen"><code><span class="terminal-shot__prompt">$</span> python3 main.py
<span class="terminal-shot__output">Solicitud 1001 (Error de acceso): responder en 2h
Solicitud 1002 (Lentitud del sistema): responder en 8h
Solicitud 1003 (Duda de uso): responder en 24h
Solicitud 1004: Prioridad desconocida: Urgentisima</span></code></pre>
</div>

> 💡 Reflexión de cierre: ¿qué parte de este programa se podría reutilizar dentro de
> una API? **La función que valida la prioridad y calcula el tiempo de respuesta** — la
> lógica de negocio no cambia, solo cambia cómo se recibe y se entrega el resultado
> (consola vs. una respuesta HTTP).

## 🖊️ Práctica libre: variables e `input()`
Aparte del reto, practiqué por mi cuenta variables y la función `input()` — que ya había
aparecido de pasada en el ejemplo de `try`/`except` de la teoría (sección 8), pero acá la
uso directamente para pedirle datos al usuario por consola.

| Archivo | Qué practica |
|---|---|
| [`02-Ejercicios/Clase-01/variables.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-01/variables.py) | Declarar variables, `print()` con varios argumentos, sumar variables numéricas |
| [`02-Ejercicios/Clase-01/input.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-01/input.py) | `input()` para leer texto del usuario y concatenarlo con `+` |
| [`02-Ejercicios/Clase-01/temperatura.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-01/temperatura.py) | `input()` + conversión a `float` + `str()` para insertar un número en un texto |

> 📌 `input()` **siempre devuelve texto (`str`)**, aunque el usuario escriba un número —
> por eso `temperatura.py` lo envuelve en `float(...)` antes de usarlo como número (el
> mismo patrón de conversión de tipos de la sección 4 de la teoría).

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

# 🏋️ EJERCICIOS CON SOLUCIÓN

### Ejercicio 1 — Tipos de datos y conversión
Crea variables para representar una solicitud de soporte: `request_id` (1001), `title`
("No puedo acceder") y `estimated_hours`, sabiendo que el dato llega como texto `"2.5"` y
debe guardarse como número decimal. Imprime `estimated_hours` y su tipo.
Salida esperada: `2.5 <class 'float'>`.

<details><summary>💡 ¿Sabías que…? — conversión de tipos (str → número)</summary>

Python no convierte automáticamente un texto en número: `"2.5" + 1` da error. Hay que
convertir explícitamente con `int()` (a entero) o `float()` (a decimal) según el caso.

```python
minutes_text = "45"
estimated_minutes = int(minutes_text)
print(estimated_minutes, type(estimated_minutes))  # 45 <class 'int'>
```
</details>

<details><summary>Ver solución</summary>

```python
request_id = 1001
title = "No puedo acceder"
hours_text = "2.5"
estimated_hours = float(hours_text)
print(estimated_hours, type(estimated_hours))
```
</details>

### Ejercicio 2 — Booleanos y `None`
Crea `is_active` (`True`) y `assigned_user` (`None`, porque todavía no se asignó a
nadie). Escribe un `if` que imprima `"Solicitud sin asignar"` cuando no haya usuario
asignado, usando `is None` (no `== None`).

<details><summary>💡 ¿Sabías que…? — comparar contra `None` con `is`</summary>

Para comparar contra `None` se usa `is None` / `is not None`, no `==`. Es la forma
"correcta" en Python porque `None` es un valor único en memoria, no algo que se compara
por igualdad como un número o texto.

```python
owner = None
if owner is None:
    print("Ticket sin dueño")
```
</details>

<details><summary>Ver solución</summary>

```python
is_active = True
assigned_user = None
if assigned_user is None:
    print("Solicitud sin asignar")
print("Activa:", is_active)
```
</details>

### Ejercicio 3 — Listas
Crea una lista `categories` con `"Hardware"`, `"Software"` y `"Accesos"`, e imprime
cuántos elementos tiene usando `len()`.
Salida esperada: `Cantidad de categorias: 3`.

<details><summary>💡 ¿Sabías que…? — `len()` funciona sobre cualquier colección</summary>

`len()` no es exclusivo de listas: también funciona con `dict`, `str` y otras
colecciones — siempre devuelve "cuántos elementos hay".

```python
departments = ["Ventas", "Soporte", "TI", "RRHH"]
print("Cantidad de departamentos:", len(departments))
```
</details>

<details><summary>Ver solución</summary>

```python
categories = ["Hardware", "Software", "Accesos"]
print("Cantidad de categorias:", len(categories))
```
</details>

### Ejercicio 4 — Diccionarios
Crea el diccionario `request` con `id` (1001), `title` ("Error de acceso"), `priority`
("Alta") y `active` (`True`). Luego cambia `priority` a `"Media"` (un diccionario es
mutable) e imprime el diccionario completo.

<details><summary>💡 ¿Sabías que…? — actualizar una clave existente</summary>

Asignar a una clave que ya existe la sobrescribe (no la duplica). Si la clave no existe
todavía, `dict["clave"] = valor` la crea.

```python
ticket = {"id": 77, "title": "Impresora no responde", "priority": "Baja", "active": True}
ticket["priority"] = "Alta"
print(ticket)
```
</details>

<details><summary>Ver solución</summary>

```python
request = {"id": 1001, "title": "Error de acceso", "priority": "Alta", "active": True}
request["priority"] = "Media"
print(request)
```
</details>

### Ejercicio 5 — Lista de diccionarios
Con `requests = [{"id": 1001, "priority": "Alta"}, {"id": 1002, "priority": "Media"},
{"id": 1003, "priority": "Alta"}]`, cuenta cuántas solicitudes tienen prioridad
`"Alta"` recorriendo la lista con `for`.
Salida esperada: `Total Alta: 2`.

<details><summary>💡 ¿Sabías que…? — acumular un conteo con `for`</summary>

Un patrón muy común: crear una variable contador en 0 antes del `for`, y sumarle 1 cada
vez que se cumple la condición dentro del ciclo (ver también el ejercicio de predicción
de la teoría, sección 6).

```python
tickets = [{"id": 10, "priority": "Baja"}, {"id": 11, "priority": "Baja"}, {"id": 12, "priority": "Media"}]
bajas = 0
for t in tickets:
    if t["priority"] == "Baja":
        bajas += 1
print("Total Baja:", bajas)
```
</details>

<details><summary>Ver solución</summary>

```python
requests = [
    {"id": 1001, "priority": "Alta"},
    {"id": 1002, "priority": "Media"},
    {"id": 1003, "priority": "Alta"},
]
altas = 0
for r in requests:
    if r["priority"] == "Alta":
        altas += 1
print("Total Alta:", altas)
```
</details>

### Ejercicio 6 — Condicionales `if`/`elif`/`else`
Dada `priority = "Media"`, asigna `response_time` según la tabla de la teoría (Alta→2,
Media→8, cualquier otro caso→24) usando `if`/`elif`/`else`, e imprímelo.
Salida esperada: `response_time: 8`.

<details><summary>💡 ¿Sabías que…? — `elif` evita comparaciones innecesarias</summary>

Con `elif` (en vez de varios `if` sueltos), en cuanto una condición se cumple las demás
ni se evalúan — es más claro y evita bugs si dos condiciones podrían cumplirse a la vez.

```python
urgencia = "Baja"
if urgencia == "Alta":
    tiempo = 1
elif urgencia == "Media":
    tiempo = 4
else:
    tiempo = 12
print("tiempo:", tiempo)
```
</details>

<details><summary>Ver solución</summary>

```python
priority = "Media"
if priority == "Alta":
    response_time = 2
elif priority == "Media":
    response_time = 8
else:
    response_time = 24
print("response_time:", response_time)
```
</details>

### Ejercicio 7 — Ciclos `for`
Usando la lista `requests` del ejercicio 5, imprime `"Critica: <id>"` por cada solicitud
con prioridad `"Alta"`.
Salida esperada:
```
Critica: 1001
Critica: 1003
```

<details><summary>💡 ¿Sabías que…? — f-strings dentro de un `for`</summary>

Los f-strings (`f"..."`) permiten insertar variables directo en el texto con `{}` — es
más legible que concatenar con `+`, y se puede combinar con acceso a diccionario dentro
de las llaves: `f"{r['id']}"`.

```python
for t in tickets:
    if t["priority"] == "Baja":
        print(f"Sin urgencia: {t['id']}")
```
</details>

<details><summary>Ver solución</summary>

```python
for r in requests:
    if r["priority"] == "Alta":
        print(f"Critica: {r['id']}")
```
</details>

### Ejercicio 8 — Funciones con tipado
Escribe `calculate_response_time(priority: str) -> int` que devuelva el tiempo de
respuesta (Alta→2, Media→8, cualquier otro caso→24), e imprime el resultado para
`"Alta"`, `"Media"` y `"Baja"`.
Salida esperada:
```
2
8
24
```

<details><summary>💡 ¿Sabías que…? — los type hints no son obligatorios ni se validan solos</summary>

`priority: str` y `-> int` son *pistas* para quien lee el código (y para el editor) —
Python no lanza error si en la práctica le pasas otro tipo. Sirven para claridad y para
que herramientas como VS Code avisen antes de ejecutar, ver la sección "🧩 7. Organizando
y reutilizando la lógica" de esta misma clase.

```python
def calcular_prioridad_dias(nivel: str) -> int:
    if nivel == "Critico":
        return 1
    if nivel == "Normal":
        return 5
    return 15

print(calcular_prioridad_dias("Critico"))
```
</details>

<details><summary>Ver solución</summary>

```python
def calculate_response_time(priority: str) -> int:
    if priority == "Alta":
        return 2
    if priority == "Media":
        return 8
    return 24

print(calculate_response_time("Alta"))
print(calculate_response_time("Media"))
print(calculate_response_time("Baja"))
```
</details>

### Ejercicio 9 — Manejo de errores con `try`/`except`
Escribe una función `to_hours(value)` que intente convertir `value` a `float` y lo
devuelva; si falla (por ejemplo si `value` es `"tres"`), debe imprimir
`"Debe ingresar un número"` y devolver `None`. Pruébala con `"3.5"` y con `"tres"`.

<details><summary>💡 ¿Sabías que…? — capturar solo el error esperado</summary>

`except ValueError` captura específicamente el error que lanza `int()`/`float()` cuando
el texto no es un número válido. Un `except:` sin tipo también atraparía otros errores
que no tienen nada que ver (por ejemplo un typo en el código) y ocultaría bugs reales.

```python
def a_entero(valor):
    try:
        return int(valor)
    except ValueError:
        print("Valor invalido")
        return None

print(a_entero("diez"))
```
</details>

<details><summary>Ver solución</summary>

```python
def to_hours(value):
    try:
        return float(value)
    except ValueError:
        print("Debe ingresar un número")
        return None

print(to_hours("3.5"))
print(to_hours("tres"))
```
</details>

### Ejercicio 10 — Reto integrador: procesador de solicitudes
Junta todo lo anterior: dada una lista de solicitudes (cada una con `id`, `title` y
`priority`), recórrelas con `for`, calcula el tiempo de respuesta con una función que
lance `ValueError` si la prioridad no es `"Alta"`, `"Media"` o `"Baja"`, captura ese
error con `try`/`except` para que el programa no se detenga, e imprime un resultado
formateado por cada solicitud (incluida la de prioridad desconocida).
Salida esperada (usa las mismas 4 solicitudes del ejemplo de la parte práctica):
```
Solicitud 1001 (Error de acceso): responder en 2h
Solicitud 1002 (Lentitud del sistema): responder en 8h
Solicitud 1003 (Duda de uso): responder en 24h
Solicitud 1004: Prioridad desconocida: Urgentisima
```

<details><summary>💡 ¿Sabías que…? — `raise` dentro de una función que después se captura con `except`</summary>

`raise` "lanza" el error hacia quien llamó a la función; si esa función se llama dentro
de un `for` envuelto en `try`/`except`, el `for` puede seguir con la siguiente vuelta en
vez de cortar todo el programa. Es el mismo patrón que en la parte práctica de esta
clase, con otro caso de negocio (validar un código de país en vez de una prioridad):

```python
def obtener_prefijo(pais: str) -> str:
    prefijos = {"Peru": "+51", "Chile": "+56"}
    if pais not in prefijos:
        raise ValueError(f"País no soportado: {pais}")
    return prefijos[pais]

for nombre in ["Peru", "Marte"]:
    try:
        print(obtener_prefijo(nombre))
    except ValueError as e:
        print(e)
```
</details>

<details><summary>Ver solución</summary>

```python
# request_utils.py
def calculate_response_time(priority: str) -> int:
    if priority == "Alta":
        return 2
    if priority == "Media":
        return 8
    if priority == "Baja":
        return 24
    raise ValueError(f"Prioridad desconocida: {priority}")


# main.py
from request_utils import calculate_response_time

support_requests = [
    {"id": 1001, "title": "Error de acceso", "priority": "Alta"},
    {"id": 1002, "title": "Lentitud del sistema", "priority": "Media"},
    {"id": 1003, "title": "Duda de uso", "priority": "Baja"},
    {"id": 1004, "title": "Solicitud rara", "priority": "Urgentisima"},
]

for request in support_requests:
    try:
        hours = calculate_response_time(request["priority"])
        print(f"Solicitud {request['id']} ({request['title']}): responder en {hours}h")
    except ValueError as error:
        print(f"Solicitud {request['id']}: {error}")
```

(código real, verificado corriendo `python3 main.py` — ver `02-Ejercicios/Clase-01/`)
</details>

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

**10. En el reto de la clase, ¿qué parte del programa se podría reutilizar dentro de una
API?**
> La función que valida la prioridad y calcula el tiempo de respuesta — la lógica de
> negocio no cambia, solo cambia cómo entra el dato y cómo se entrega la respuesta.

## 📎 Apuntes relacionados
- [00-Notas/02-Conceptos.md](../00-Notas/02-Conceptos.md) — tabla de conceptos (tipos de
  datos, entorno virtual, manejo de errores).
- [00-Notas/01-Comandos.md](../00-Notas/01-Comandos.md) — comandos de `venv` y `pip`.

## ➡️ Siguiente
[Clase 2](Clase-02.md)
