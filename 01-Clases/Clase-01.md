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

> 📝 Esta nota va **teoría seguida de su práctica**: cada sección numerada trae, justo
> debajo, los ejercicios reales que la ponen en práctica (`02-Ejercicios/Clase-01/`).
> Las secciones "PARA IR MÁS ALLÁ" (9-15) son profundización propia sin ejercicio
> asociado — ver el aviso antes de esa parte.

# 📖 TEORÍA Y PRÁCTICA

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

### 🖊️ Práctica: variables e `input()`
Aparte del reto, practiqué por mi cuenta variables y la función `input()` — que se ve
más adelante de pasada en el ejemplo de `try`/`except` de la teoría (sección 8), pero
acá la uso directamente para pedirle datos al usuario por consola.

| Archivo | Qué practica |
|---|---|
| [`02-Ejercicios/Clase-01/variables.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-01/variables.py) | Declarar variables, `print()` con varios argumentos, sumar variables numéricas |
| [`02-Ejercicios/Clase-01/input.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-01/input.py) | `input()` para leer texto del usuario y concatenarlo con `+` |
| [`02-Ejercicios/Clase-01/temperatura.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-01/temperatura.py) | `input()` + conversión a `float` + `str()` para insertar un número en un texto |
| [`02-Ejercicios/Clase-01/calenda.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-01/calenda.py) | Módulo `calendar` de la librería estándar — imprime el calendario de un mes |

> 📌 `input()` **siempre devuelve texto (`str`)**, aunque el usuario escriba un número —
> por eso `temperatura.py` lo envuelve en `float(...)` antes de usarlo como número (el
> mismo patrón de conversión de tipos de esta sección).

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

## 📦 5. Agrupando información relacionada
| Estructura | Qué es | Ejemplo |
|---|---|---|
| Lista (`list`) | Colección **ordenada**, se accede por índice, es mutable | `categories = ["Hardware", "Software", "Accesos"]` |
| Diccionario (`dict`) | Pares **clave-valor**, acceso por nombre, es mutable | `request = {"id": 1001, "priority": "Alta"}` |
| Lista de diccionarios | Colección de registros — ideal para varias entidades del mismo tipo | `requests = [{"id": 1001, "priority": "Alta"}, {"id": 1002, "priority": "Media"}]` |

### 📋 Ejemplo: lista (`list`)
Guarda varios valores en un **orden** que se mantiene, y se accede por **índice**
(posición numérica, empezando en `0`) — sirve para "varias cosas del mismo tipo":
categorías, tareas, nombres. Es **mutable**: se puede modificar después de creada
(agregar, quitar, reemplazar elementos) sin crear una lista nueva.

```python
categories = ["Hardware", "Software", "Accesos"]

print(categories[0])        # acceso por índice (posición 0)
categories.append("Redes")  # agrega al final — la lista es mutable
print(categories)
print(len(categories))      # cantidad de elementos
```
```
Hardware
['Hardware', 'Software', 'Accesos', 'Redes']
4
```

### 🗂️ Ejemplo: diccionario (`dict`)
Guarda pares **clave → valor** y se accede por **clave** (un nombre elegido por quien
escribe el código), no por posición — sirve para "describir una cosa con varios
datos": una solicitud tiene `id`, `title`, `priority`. También es **mutable**: agregar
una clave nueva o cambiar el valor de una existente no crea un diccionario nuevo.

```python
request = {
    "id": 1001,
    "title": "Error de acceso",
    "priority": "Alta",
    "active": True,
}

print(request["title"])        # acceso por clave, no por posición
request["priority"] = "Media"  # sobrescribe el valor de una clave existente
print(request)
```
```
Error de acceso
{'id': 1001, 'title': 'Error de acceso', 'priority': 'Media', 'active': True}
```

### 📊 Ejemplo: lista de diccionarios
Combina ambas: una colección **ordenada** donde cada elemento es, a su vez, un
**registro completo** (un diccionario). Es el patrón que más se repite en Backend —
así se representa, por ejemplo, el resultado de una consulta a una base de datos (una
fila = un diccionario, varias filas = una lista).

```python
requests = [
    {"id": 1001, "title": "Error de acceso", "priority": "Alta"},
    {"id": 1002, "title": "Lentitud del sistema", "priority": "Media"},
]

print(requests[0]["priority"])  # primero el índice de la lista, después la clave

for r in requests:
    print(r["id"], "-", r["title"])
```
```
Alta
1001 - Error de acceso
1002 - Lentitud del sistema
```

> 💡 La lista de diccionarios es el patrón que más se repite en Backend: así se
> representa, por ejemplo, el resultado de una consulta a una base de datos (una fila =
> un diccionario, varias filas = una lista).

> 🧪 Tip de entrevista: ¿por qué un diccionario y no una lista para representar una
> solicitud? Porque cada dato tiene un **nombre** (`id`, `priority`) y el orden en que
> se escriben no importa para acceder a ellos — con una lista habría que recordar "la
> prioridad está en la posición 2", algo frágil si el orden cambia.

### 🖊️ Práctica: variables sueltas, listas y diccionarios
Siguiendo con la práctica libre, repetí el mismo dato (una "solicitud") de tres formas
distintas — primero como variables sueltas, después agrupado en una lista y en un
diccionario, y por último combinando lista + diccionario — para comparar en carne propia
la diferencia que explica la teoría de esta sección.

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
> de esta sección: con variables sueltas, si tuviera 10 solicitudes necesitaría 50
> variables con nombres distintos (`request_id_1`, `request_id_2`...); con un `dict`
> por solicitud y una `list` para agruparlas (`listadediccionarios.py`), agregar una
> solicitud más es solo agregar un elemento a la lista — el `for` ya sabe recorrerlas
> todas sin importar cuántas sean.

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
> `str()` explícito (mismo patrón ya usado en `diccionario.py` y en la teoría de
> funciones, sección 7).

### 🦸 Práctica: `superheroes.py` — añadir, eliminar y reemplazar en una lista
Enunciado: dada la lista de héroes de los Vengadores, (1) agregar a Spider-Man, (2)
eliminar a Thor y (3) reemplazar a Capitán América por Pantera Negra. Métodos usados
(ver también el ejemplo de lista de más arriba): `.append(x)`, `.remove(x)` y
`.index(x)` para reemplazar por posición.

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

## 🔀 6. Tomando decisiones y repitiendo procesos
| Estructura | Qué hace |
|---|---|
| `if` / `elif` / `else` | Decide según una condición. |
| `for` | Recorre una colección elemento a elemento. |
| `while` | Repite mientras se cumpla una condición. |

**`if` / `elif` / `else`** ejecutan un bloque de código solo si se cumple una
condición (una comparación, un booleano). Python evalúa las condiciones **en orden**
y ejecuta el primer bloque cuya condición dé `True` — el resto ni se evalúa.

**`for`** recorre una colección (lista, diccionario, string, `range(...)`...)
**elemento a elemento**, ejecutando el bloque una vez por cada uno. Se usa cuando se
sabe de antemano **sobre qué** se va a iterar — el `for` mismo se encarga de saber
cuántas vueltas dar, sin necesidad de contarlas a mano.

**`while`** repite un bloque de código **mientras** una condición se mantenga
verdadera — la condición se vuelve a evaluar **antes de cada vuelta**, y en cuanto da
`False` el bucle termina. Se usa cuando no se sabe de antemano cuántas repeticiones
van a hacer falta (depende de que algo cambie durante la ejecución), y por eso
necesita alguna variable que controle el corte (un contador, una bandera) actualizada
a mano dentro del bloque — si se olvida actualizarla, el bucle **nunca termina**
(bucle infinito).

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

# while: repite mientras la condición sea verdadera — hay que
# actualizar 'index' a mano en cada vuelta, o nunca se corta
index = 0
while index < len(requests):
    print(requests[index]["id"])
    index += 1
```

> ⚠️ Con `requests` de 2 elementos, el `for` de la línea 8 y el `while` de más abajo
> imprimen exactamente lo mismo (`1001`, `1002`) — misma tarea, dos formas de
> recorrer. La diferencia está en **quién controla el corte**: el `for` lo hace solo
> (recorre hasta el último elemento y para), el `while` depende de que `index` se
> incremente a mano dentro del bloque.

> 🧪 Tip de entrevista (pregunta de la clase): si `priorities = ["Alta", "Baja", "Alta"]`
> y por cada `"Alta"` se suma 1 a `total`, ¿cuántas veces se suma? **Respuesta: 2** (solo
> cuenta las veces que la condición del `if` se cumple, no el largo de la lista).

### 🔐 Práctica: `contrasena.py` — comparar strings ignorando mayúsculas
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

### 👤 Práctica: `main.py` — condicional simple: ¿puede jubilarse?
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

### 💰 Práctica: `impuestos.py` — condicional con cálculo
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

### 🔁 Práctica: `ciclos.py` — recorrer una lista con `while`
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

### 📋 Práctica: `listasolicitudes.py` — recorrer una lista con `for`
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

> 📝 **`request_utils.py` sin documentar:** este archivo real de
> `02-Ejercicios/Clase-01/` implementaba justo esta idea (función movida a su propio
> módulo), pero el "reto de cierre" que la usaba (`main.py` original, "procesador de
> solicitudes de soporte") no correspondía en realidad a esta clase — al revisar la
> grabación, `main.py` era el ejercicio de jubilación de más arriba. `request_utils.py`
> queda en la carpeta sin usarse por ahora; se retoma si el reto real aparece en una
> clase siguiente.

### 🧮 Práctica: `calculadora.py` — función con `if/elif` por operador
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

### 🚨 Práctica: `try-except.py` — capturar `ValueError` al convertir un dato
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

> 💡 Es la versión mínima, hecha a mano, del mismo patrón de la teoría de esta sección y
> de `contrasena.py`/`impuestos.py` más arriba: cualquier `int(input(...))` puede fallar
> si el usuario escribe texto, y `try`/`except ValueError` evita que ese error tumbe
> todo el programa.

# 🔬 PARA IR MÁS ALLÁ — profundizando rumbo a Backend

> 📌 Esto **no se vio en esta clase** — lo agrego por mi cuenta sobre la misma
> base de la Clase 1, porque son los primeros huecos que aparecen apenas se empieza a
> pensar en construir un backend de verdad (una API, una base de datos, un servicio en
> producción). Todo el código está verificado en terminal. Ninguna de estas secciones
> tiene un ejercicio propio en `02-Ejercicios/Clase-01/` — son profundización teórica.

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

# 🏋️ EJERCICIOS CON SOLUCIÓN

> 📌 30 ejercicios que repasan **toda la teoría de esta clase** (secciones 1 a 15), de
> lo más básico a lo más completo. Cada uno tiene un desplegable **"💡 ¿Sabías que…?"**
> con el repaso del concepto + un ejemplo de referencia (otro dominio, mismo patrón) y
> un desplegable **"Ver solución"** — todo el código fue corrido en terminal antes de
> documentarlo. Los ejercicios 1-20 son de un solo concepto; del 21 en adelante
> combinan varios, hasta el ejercicio integrador final (30).

### Ejercicio 1 — Tipos de datos y conversión
Crea `request_id` (`1001`), `title` (`"No puedo acceder"`) y, sabiendo que el precio
llega como texto `"49.90"`, conviértelo a decimal en `price`. Imprime `price` y su
tipo con `print(price, type(price))`. Salida esperada: `49.9` y la clase `float`.

<details><summary>💡 ¿Sabías que…? — conversión de tipos (str → número), sección 4</summary>

Python no convierte automáticamente un texto en número: hay que hacerlo explícito con
`int()` (entero) o `float()` (decimal), según el caso.

```python
product_id = 2001
name = "Teclado mecánico"
stock_text = "15"
stock = int(stock_text)
in_promo = False
supplier = None

print(stock, type(stock))
```
```
15 <class 'int'>
```
</details>

<details><summary>Ver solución</summary>

```python
request_id = 1001
title = "No puedo acceder"
price_text = "49.90"
price = float(price_text)
is_paid = True
assigned_to = None

print(price, type(price))
```
```
49.9 <class 'float'>
```
</details>

### Ejercicio 2 — Booleanos y `None`
Crea `is_active` (`True`) y `assigned_user` (`None`). Escribe un `if` que imprima
`"Solicitud sin asignar"` cuando no haya usuario asignado, comparando con `is None`
(no `== None`).

<details><summary>💡 ¿Sabías que…? — comparar contra `None` con `is`, sección 4</summary>

Para comparar contra `None` se usa `is None` / `is not None`, no `==`. `None` es un
único valor especial en memoria, no algo que se compara por igualdad como un número.

```python
manager = None
if manager is None:
    print("Producto sin encargado")
```
```
Producto sin encargado
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
```
Solicitud sin asignar
Activa: True
```
</details>

### Ejercicio 3 — Lista: crear, indexar, `len()`
Crea `categories` con `"Hardware"`, `"Software"` y `"Accesos"`. Imprime el primer
elemento, el último (con índice negativo) y la cantidad total.

<details><summary>💡 ¿Sabías que…? — índices negativos, sección 5</summary>

`lista[-1]` accede al **último** elemento sin necesitar saber cuántos hay
(`lista[len(lista) - 1]` daría lo mismo, pero es más largo e innecesario).

```python
colors = ["Rojo", "Verde", "Azul", "Amarillo"]
print(colors[0])
print(colors[-1])
print(len(colors))
```
```
Rojo
Amarillo
4
```
</details>

<details><summary>Ver solución</summary>

```python
categories = ["Hardware", "Software", "Accesos"]
print(categories[0])
print(categories[-1])
print(len(categories))
```
```
Hardware
Accesos
3
```
</details>

### Ejercicio 4 — Diccionario: acceder y actualizar
Crea `request` con `id` (`1001`), `title` (`"Error de acceso"`) y `priority`
(`"Alta"`). Imprime `title`, después cambia `priority` a `"Media"` e imprime el
diccionario completo.

<details><summary>💡 ¿Sabías que…? — actualizar una clave existente, sección 5</summary>

Asignar a una clave que ya existe la **sobrescribe** (no la duplica). Si la clave no
existiera, `dict["clave"] = valor` la crearía.

```python
product = {"id": 2001, "name": "Teclado", "stock": 15}
print(product["name"])
product["stock"] = 12
print(product)
```
```
Teclado
{'id': 2001, 'name': 'Teclado', 'stock': 12}
```
</details>

<details><summary>Ver solución</summary>

```python
request = {"id": 1001, "title": "Error de acceso", "priority": "Alta"}
print(request["title"])
request["priority"] = "Media"
print(request)
```
```
Error de acceso
{'id': 1001, 'title': 'Error de acceso', 'priority': 'Media'}
```
</details>

### Ejercicio 5 — Lista de diccionarios: sumar un campo
Con `requests = [{"id": 1001, "hours": 2}, {"id": 1002, "hours": 8}, {"id": 1003,
"hours": 5}]`, recorre la lista con `for` y suma el campo `hours` de todas. Salida
esperada: `Total horas: 15`.

<details><summary>💡 ¿Sabías que…? — acumular un total con `for`, sección 5</summary>

Patrón muy común: una variable acumuladora en `0` antes del `for`, que se le suma un
campo del diccionario en cada vuelta.

```python
orders = [{"id": 1, "amount": 100}, {"id": 2, "amount": 250}, {"id": 3, "amount": 75}]
total = 0
for o in orders:
    total += o["amount"]
print("Total monto:", total)
```
```
Total monto: 425
```
</details>

<details><summary>Ver solución</summary>

```python
requests = [
    {"id": 1001, "hours": 2},
    {"id": 1002, "hours": 8},
    {"id": 1003, "hours": 5},
]
total = 0
for r in requests:
    total += r["hours"]
print("Total horas:", total)
```
```
Total horas: 15
```
</details>

### Ejercicio 6 — Condicionales `if`/`elif`/`else`
Dado `hours = 30`, clasifica la carga de trabajo: menos de 20 → `"Baja"`; hasta 40
(inclusive) → `"Normal"`; más de 40 → `"Sobrecarga"`. Salida esperada:
`Carga: Normal`.

<details><summary>💡 ¿Sabías que…? — rangos con `elif`, sección 6</summary>

`elif condicion <= limite` funciona porque Python ya descartó el `if` anterior — no
hace falta repetir el límite inferior (`20 <= score <= 40`), alcanza con la condición
superior.

```python
score = 65
if score < 50:
    grade = "Insuficiente"
elif score <= 79:
    grade = "Aprobado"
else:
    grade = "Sobresaliente"
print("Nota:", grade)
```
```
Nota: Aprobado
```
</details>

<details><summary>Ver solución</summary>

```python
hours = 30
if hours < 20:
    load = "Baja"
elif hours <= 40:
    load = "Normal"
else:
    load = "Sobrecarga"
print("Carga:", load)
```
```
Carga: Normal
```
</details>

### Ejercicio 7 — Ciclo `for` con condición
Con la lista de solicitudes del ejercicio 5 (usa `priority` en vez de `hours`: Alta,
Baja, Alta), imprime `f"Urgente: {r['id']}"` solo para las de prioridad `"Alta"`.

<details><summary>💡 ¿Sabías que…? — `if` dentro de un `for`, sección 6</summary>

El `if` adentro del `for` no "salta" vueltas — se evalúa en **cada** vuelta, y el
`print` solo se ejecuta cuando la condición de esa vuelta específica es verdadera.

```python
products = [{"id": 1, "stock": 0}, {"id": 2, "stock": 5}, {"id": 3, "stock": 0}]
for p in products:
    if p["stock"] == 0:
        print(f"Sin stock: {p['id']}")
```
```
Sin stock: 1
Sin stock: 3
```
</details>

<details><summary>Ver solución</summary>

```python
requests = [
    {"id": 1001, "priority": "Alta"},
    {"id": 1002, "priority": "Baja"},
    {"id": 1003, "priority": "Alta"},
]
for r in requests:
    if r["priority"] == "Alta":
        print(f"Urgente: {r['id']}")
```
```
Urgente: 1001
Urgente: 1003
```
</details>

### Ejercicio 8 — Ciclo `while`
Con `tickets_pendientes = 5`, usa un `while` para "atenderlos" uno por uno
(decrementando el contador) y cuenta cuántos se atendieron. Salida esperada:
`Tickets atendidos: 5`.

<details><summary>💡 ¿Sabías que…? — `while` que consume un contador, sección 6</summary>

Patrón alternativo al de "contador que sube": acá el `while` corre **mientras quede
algo por consumir**, restando 1 en cada vuelta hasta llegar a `0` (que es "falsy" al
evaluarse como condición implícita, aunque acá se compara explícito con `> 0`).

```python
saldo = 3
retiros = 0
while saldo > 0:
    retiros += 1
    saldo -= 1
print("Retiros realizados:", retiros)
```
```
Retiros realizados: 3
```
</details>

<details><summary>Ver solución</summary>

```python
tickets_pendientes = 5
atendidos = 0
while tickets_pendientes > 0:
    atendidos += 1
    tickets_pendientes -= 1
print("Tickets atendidos:", atendidos)
```
```
Tickets atendidos: 5
```
</details>

### Ejercicio 9 — Función simple con `def`
Escribe `saludar(nombre)` que **devuelva** (no imprima) el string `f"Hola, {nombre}!"`.
Guarda el resultado en una variable e imprímelo.

<details><summary>💡 ¿Sabías que…? — guardar el resultado de una función, sección 7</summary>

Como la función usa `return` (no `print`), el valor queda disponible para guardarlo en
una variable y reutilizarlo — a diferencia de una función que solo imprime.

```python
def despedir(nombre):
    return f"Chau, {nombre}!"

mensaje = despedir("Luis")
print(mensaje)
```
```
Chau, Luis!
```
</details>

<details><summary>Ver solución</summary>

```python
def saludar(nombre):
    return f"Hola, {nombre}!"

mensaje = saludar("Ana")
print(mensaje)
```
```
Hola, Ana!
```
</details>

### Ejercicio 10 — Función con type hints y varias ramas
Escribe `calcular_envio(peso: float, distancia_km: float) -> float`: hasta 10 km,
`peso * 500`; hasta 50 km, `peso * 800`; más de 50 km, `peso * 1200`. Pruébala con
`peso=2` en las 3 distancias (`5`, `30`, `100`).

<details><summary>💡 ¿Sabías que…? — varias ramas `if`/`elif`/`else` con `return`, sección 7</summary>

Cada rama termina la función apenas hace `return` — no hace falta `else` explícito
después de un `if`/`elif` que ya retornó, pero se agrega igual por claridad (mismo
criterio que `calculadora.py`).

```python
def calcular_comision(monto: float, tipo: str) -> float:
    if tipo == "bronce":
        return monto * 0.02
    elif tipo == "plata":
        return monto * 0.05
    else:
        return monto * 0.08

print(calcular_comision(1000, "bronce"))
print(calcular_comision(1000, "plata"))
print(calcular_comision(1000, "oro"))
```
```
20.0
50.0
80.0
```
</details>

<details><summary>Ver solución</summary>

```python
def calcular_envio(peso: float, distancia_km: float) -> float:
    if distancia_km <= 10:
        return peso * 500
    elif distancia_km <= 50:
        return peso * 800
    else:
        return peso * 1200

print(calcular_envio(2, 5))
print(calcular_envio(2, 30))
print(calcular_envio(2, 100))
```
```
1000
1600
2400
```
</details>

### Ejercicio 11 — `try`/`except` al convertir tipos
Escribe `to_hours(value)` que intente convertir `value` a `float`; si falla, imprime
`"Debe ingresar un número"` y devuelve `None`. Pruébala con `"3.5"` y con `"tres"`.

<details><summary>💡 ¿Sabías que…? — capturar solo el error esperado, sección 8</summary>

`except ValueError` captura específicamente el error de `int()`/`float()` con texto no
numérico. Un `except:` sin tipo también atraparía errores que no tienen nada que ver,
ocultando bugs reales.

```python
def to_edad(value):
    try:
        return int(value)
    except ValueError:
        print("Debe ingresar un número")
        return None

print(to_edad("30"))
print(to_edad("treinta"))
```
```
30
Debe ingresar un número
None
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
```
3.5
Debe ingresar un número
None
```
</details>

### Ejercicio 12 — `raise` manual con mensaje de negocio
Escribe `registrar_horas(horas)`: si `horas <= 0`, lanza `ValueError("Las horas deben
ser positivas")`; si no, imprime `f"Horas registradas: {horas}"`. Pruébala con `5` y
con `-2` (capturando el error con `try`/`except`).

<details><summary>💡 ¿Sabías que…? — `raise` propio vs. `raise` que lanza Python solo, sección 8</summary>

Acá **el código decide** que `-5` es inválido y lanza el error a propósito (con
`raise`) — no es un error que Python detecte solo (como sí pasa con `int("texto")`).
Es la forma de aplicar una **regla de negocio**.

```python
def registrar_stock(cantidad):
    if cantidad < 0:
        raise ValueError("El stock no puede ser negativo")
    print(f"Stock registrado: {cantidad}")

registrar_stock(10)
try:
    registrar_stock(-5)
except ValueError as e:
    print("Error:", e)
```
```
Stock registrado: 10
Error: El stock no puede ser negativo
```
</details>

<details><summary>Ver solución</summary>

```python
def registrar_horas(horas):
    if horas <= 0:
        raise ValueError("Las horas deben ser positivas")
    print(f"Horas registradas: {horas}")

registrar_horas(5)
try:
    registrar_horas(-2)
except ValueError as e:
    print("Error:", e)
```
```
Horas registradas: 5
Error: Las horas deben ser positivas
```
</details>

### Ejercicio 13 — Función + lista de diccionarios + condición combinadas
Escribe `contar_por_prioridad(requests, prioridad)` que devuelva cuántas solicitudes
de la lista tienen esa prioridad. Pruébala contando las `"Alta"` de una lista de 3
solicitudes (2 Altas, 1 Media).

<details><summary>💡 ¿Sabías que…? — combinar función + `for` + `if` + acumulador, secciones 5-7</summary>

Es la unión de tres cosas ya practicadas por separado: la función (sección 7) envuelve
un `for` con `if` (sección 6) que recorre una lista de diccionarios (sección 5) —
ninguna es nueva, lo nuevo es **combinarlas**.

```python
def contar_por_categoria(products, categoria):
    total = 0
    for p in products:
        if p["category"] == categoria:
            total += 1
    return total

products = [
    {"id": 1, "category": "Hardware"},
    {"id": 2, "category": "Software"},
    {"id": 3, "category": "Hardware"},
]
print(contar_por_categoria(products, "Hardware"))
```
```
2
```
</details>

<details><summary>Ver solución</summary>

```python
def contar_por_prioridad(requests, prioridad):
    total = 0
    for r in requests:
        if r["priority"] == prioridad:
            total += 1
    return total

requests = [
    {"id": 1, "priority": "Alta"},
    {"id": 2, "priority": "Media"},
    {"id": 3, "priority": "Alta"},
]
print(contar_por_prioridad(requests, "Alta"))
```
```
2
```
</details>

### Ejercicio 14 — Lista: `.append()`/`.remove()`/reemplazo por índice
Con `tareas = ["Revisar PR", "Actualizar docs", "Deploy"]`: agrega `"Code review"`,
elimina `"Deploy"` y reemplaza `"Actualizar docs"` por `"Actualizar README"`.

<details><summary>💡 ¿Sabías que…? — mismo patrón que `superheroes.py`, sección 5</summary>

`.index(x)` busca la posición de `x` para poder reemplazarlo sin hardcodear el índice
— si el orden de la lista cambiara, el reemplazo seguiría apuntando al elemento
correcto (busca por **valor**, no por posición fija).

```python
invitados = ["Ana", "Luis", "Carlos", "Marta"]
invitados.append("Sofía")
invitados.remove("Carlos")
invitados[invitados.index("Luis")] = "Luis Fernando"
print(invitados)
```
```
['Ana', 'Luis Fernando', 'Marta', 'Sofía']
```
</details>

<details><summary>Ver solución</summary>

```python
tareas = ["Revisar PR", "Actualizar docs", "Deploy"]
tareas.append("Code review")
tareas.remove("Deploy")
tareas[tareas.index("Actualizar docs")] = "Actualizar README"
print(tareas)
```
```
['Revisar PR', 'Actualizar README', 'Code review']
```
</details>

### Ejercicio 15 — Comparar strings ignorando mayúsculas
Con `usuario_bd = "admin"` y `usuario_input = "ADMIN"`, imprime `"Usuario válido"` si
coinciden **sin distinguir mayúsculas/minúsculas**, o `"Usuario inválido"` si no.

<details><summary>💡 ¿Sabías que…? — mismo patrón que `contrasena.py`, sección 6</summary>

`"ADMIN" == "admin"` da `False` — `==` sobre strings **sí** distingue mayúsculas. Hay
que normalizar ambos lados con `.lower()` (o `.upper()`, cualquiera de los dos, con
que sean consistentes) antes de comparar.

```python
codigo_bd = "promo10"
codigo_input = "PROMO10"
if codigo_input.lower() == codigo_bd.lower():
    print("Código válido")
else:
    print("Código inválido")
```
```
Código válido
```
</details>

<details><summary>Ver solución</summary>

```python
usuario_bd = "admin"
usuario_input = "ADMIN"
if usuario_input.lower() == usuario_bd.lower():
    print("Usuario válido")
else:
    print("Usuario inválido")
```
```
Usuario válido
```
</details>

### Ejercicio 16 — `for` vs. `while`: mismo resultado
Con `ids = [101, 102, 103, 104]`, imprime todos los elementos **dos veces**: primero
recorriendo con `for`, después con `while` (usando un índice manual).

<details><summary>💡 ¿Sabías que…? — comparar ambos enfoques lado a lado, sección 6</summary>

Ambos recorridos producen exactamente la misma salida — la diferencia no está en el
resultado, sino en **quién controla el corte** (ver la teoría de la sección 6): el
`for` lo hace solo, el `while` depende del índice que se actualiza a mano.

```python
nombres = ["Ana", "Luis", "Carla"]

for n in nombres:
    print(n)

indice = 0
while indice < len(nombres):
    print(nombres[indice])
    indice += 1
```
```
Ana
Luis
Carla
Ana
Luis
Carla
```
</details>

<details><summary>Ver solución</summary>

```python
ids = [101, 102, 103, 104]

for i in ids:
    print(i)

indice = 0
while indice < len(ids):
    print(ids[indice])
    indice += 1
```
```
101
102
103
104
101
102
103
104
```
</details>

### Ejercicio 17 — Función que calcula un promedio
Escribe `promedio_horas(requests)` que devuelva el promedio del campo `hours` de una
lista de diccionarios (usa `{"hours": 2}, {"hours": 8}, {"hours": 5}`). Salida
esperada: `Promedio: 5.0`.

<details><summary>💡 ¿Sabías que…? — dividir un acumulador por `len()`, sección 7</summary>

El promedio es el mismo patrón acumulador del ejercicio 5, solo que al final se divide
el total entre `len(lista)` — la cantidad de elementos, no un número fijo (así sirve
para cualquier tamaño de lista).

```python
def promedio_precios(products):
    total = 0
    for p in products:
        total += p["price"]
    return total / len(products)

products = [{"price": 10.0}, {"price": 25.0}, {"price": 15.0}]
promedio = promedio_precios(products)
print(f"Promedio: {round(promedio, 2)}")
```
```
Promedio: 16.67
```
</details>

<details><summary>Ver solución</summary>

```python
def promedio_horas(requests):
    total = 0
    for r in requests:
        total += r["hours"]
    return total / len(requests)

requests = [{"hours": 2}, {"hours": 8}, {"hours": 5}]
promedio = promedio_horas(requests)
print(f"Promedio: {promedio}")
```
```
Promedio: 5.0
```
</details>

### Ejercicio 18 — Mutabilidad: modificar una lista "en el lugar"
Escribe `marcar_revisadas(requests_list)` que le agregue la clave `"revisado": True`
a cada diccionario de la lista (sin crear una lista nueva) y la devuelva. Comprueba
que la lista **original** también quedó modificada, y que `resultado is original`
da `True`.

<details><summary>💡 ¿Sabías que…? — el bug de mutabilidad más común, sección 9</summary>

Como los diccionarios son mutables, modificarlos **dentro** de la función (sin
reasignar la lista completa) afecta también a la variable de quien llamó a la
función — no hizo falta ningún `return` para que el cambio "se vea afuera".

```python
def aplicar_descuento(products_list):
    for p in products_list:
        p["con_descuento"] = True
    return products_list

original = [{"id": 1}, {"id": 2}]
resultado = aplicar_descuento(original)
print(original)
print(resultado is original)
```
```
[{'id': 1, 'con_descuento': True}, {'id': 2, 'con_descuento': True}]
True
```
</details>

<details><summary>Ver solución</summary>

```python
def marcar_revisadas(requests_list):
    for r in requests_list:
        r["revisado"] = True
    return requests_list

original = [{"id": 1}, {"id": 2}]
resultado = marcar_revisadas(original)
print(original)
print(resultado is original)
```
```
[{'id': 1, 'revisado': True}, {'id': 2, 'revisado': True}]
True
```
</details>

### Ejercicio 19 — Mutabilidad: reasignación local (no afecta afuera)
Escribe `resetear(requests_list)` que **reasigne** el parámetro a una lista nueva
(`requests_list = []`), le agregue un elemento y la devuelva. Comprueba que la lista
**original** queda intacta.

<details><summary>💡 ¿Sabías que…? — la otra cara de la mutabilidad, sección 9</summary>

A diferencia del ejercicio 18, acá `requests_list = []` crea una lista **nueva y
local** — deja de apuntar a la lista original, así que nada de lo que se haga después
sobre ese nombre afecta a la variable de quien llamó a la función.

```python
def reiniciar(products_list):
    products_list = []
    products_list.append({"id": 8888})
    return products_list

original = [{"id": 1}]
nueva = reiniciar(original)
print(original)
print(nueva)
```
```
[{'id': 1}]
[{'id': 8888}]
```
</details>

<details><summary>Ver solución</summary>

```python
def resetear(requests_list):
    requests_list = []
    requests_list.append({"id": 9999})
    return requests_list

original = [{"id": 1}]
nueva = resetear(original)
print(original)
print(nueva)
```
```
[{'id': 1}]
[{'id': 9999}]
```
</details>

### Ejercicio 20 — Parámetro opcional con `| None`
Escribe `resumen_ticket(title: str, hours: float | None = None) -> str`: si `hours`
es `None`, devuelve `f"{title} (sin estimar)"`; si no, `f"{title} ({hours}h)"`. Pruébala
sin pasar `hours` y pasando `3.5`.

<details><summary>💡 ¿Sabías que…? — valor por defecto + tipo opcional, sección 10</summary>

`hours: float | None = None` dice dos cosas a la vez: el tipo puede ser `float` **o**
`None` (opcional), y si no se pasa nada al llamar la función, toma `None` por
defecto — no hace falta pasar el parámetro siempre.

```python
def resumen_producto(name: str, stock: int | None = None) -> str:
    if stock is None:
        return f"{name} (sin stock registrado)"
    return f"{name} ({stock} unidades)"

print(resumen_producto("Teclado"))
print(resumen_producto("Mouse", 20))
```
```
Teclado (sin stock registrado)
Mouse (20 unidades)
```
</details>

<details><summary>Ver solución</summary>

```python
def resumen_ticket(title: str, hours: float | None = None) -> str:
    if hours is None:
        return f"{title} (sin estimar)"
    return f"{title} ({hours}h)"

print(resumen_ticket("Error de acceso"))
print(resumen_ticket("Falla de red", 3.5))
```
```
Error de acceso (sin estimar)
Falla de red (3.5h)
```
</details>

### Ejercicio 21 — `dataclass` básica
Define `Ticket` con `id: int`, `title: str` y `priority: str` usando `@dataclass`.
Crea una instancia e imprímela completa, y también solo su `priority`.

<details><summary>💡 ¿Sabías que…? — qué gana un `dataclass` frente a un `dict`, sección 11</summary>

`print(objeto)` de un `dataclass` ya muestra todos los campos con nombre, sin que haya
que escribir un `__repr__` a mano — y a diferencia de un `dict`, si escribís mal un
nombre de campo (`p1.preico`), el editor o Python avisan, en vez de fallar en
silencio recién en producción.

```python
from dataclasses import dataclass

@dataclass
class Producto:
    id: int
    nombre: str
    precio: float

p1 = Producto(id=1, nombre="Teclado", precio=25000)
print(p1)
print(p1.precio)
```
```
Producto(id=1, nombre='Teclado', precio=25000)
25000
```
</details>

<details><summary>Ver solución</summary>

```python
from dataclasses import dataclass

@dataclass
class Ticket:
    id: int
    title: str
    priority: str

t1 = Ticket(id=1001, title="Error de acceso", priority="Alta")
print(t1)
print(t1.priority)
```
```
Ticket(id=1001, title='Error de acceso', priority='Alta')
Alta
```
</details>

### Ejercicio 22 — `dataclass` con lista mutable (`field(default_factory=list)`)
Agrega a `Ticket` un campo `tags: list[str] = field(default_factory=list)`. Crea dos
tickets distintos, agrégale un tag solo al primero, e imprime ambos `tags` para
comprobar que **no** se comparten entre instancias.

<details><summary>💡 ¿Sabías que…? — por qué no `tags: list[str] = []` a secas, sección 11</summary>

Si el valor por defecto fuera literalmente `[]` (sin `field(default_factory=...)`),
**todas** las instancias compartirían la **misma** lista en memoria — modificar la de
una afectaría a las demás. `default_factory` le dice a Python "creá una lista nueva
por cada instancia", evitando ese bug clásico.

```python
from dataclasses import dataclass, field

@dataclass
class Pedido:
    id: int
    cliente: str
    items: list[str] = field(default_factory=list)

p1 = Pedido(id=1, cliente="Ana")
p1.items.append("Teclado")
print(p1)

p2 = Pedido(id=2, cliente="Luis")
print(p2.items)
```
```
Pedido(id=1, cliente='Ana', items=['Teclado'])
[]
```
</details>

<details><summary>Ver solución</summary>

```python
from dataclasses import dataclass, field

@dataclass
class Ticket:
    id: int
    title: str
    tags: list[str] = field(default_factory=list)

t1 = Ticket(id=1001, title="Error de acceso")
t1.tags.append("urgente")
print(t1)

t2 = Ticket(id=1002, title="Falla de red")
print(t2.tags)
```
```
Ticket(id=1001, title='Error de acceso', tags=['urgente'])
[]
```
</details>

### Ejercicio 23 — `dataclass` inmutable (`frozen=True`)
Define `TicketId` con un solo campo `valor: int`, marcada `frozen=True`. Crea una
instancia, imprime su valor, e intenta modificarlo — capturá el error con
`try`/`except FrozenInstanceError`.

<details><summary>💡 ¿Sabías que…? — cuándo usar `frozen=True`, sección 11</summary>

`frozen=True` sirve para datos que **no deberían cambiar** después de creados (un ID
ya asignado, una configuración cargada una sola vez). Intentar reasignar cualquier
campo lanza `FrozenInstanceError` en vez de dejarlo pasar en silencio.

```python
from dataclasses import dataclass
from dataclasses import FrozenInstanceError

@dataclass(frozen=True)
class DNI:
    numero: str

dni = DNI("12345678")
print(dni.numero)
try:
    dni.numero = "87654321"
except FrozenInstanceError as e:
    print("Error:", e)
```
```
12345678
Error: cannot assign to field 'numero'
```
</details>

<details><summary>Ver solución</summary>

```python
from dataclasses import dataclass
from dataclasses import FrozenInstanceError

@dataclass(frozen=True)
class TicketId:
    valor: int

tid = TicketId(1001)
print(tid.valor)
try:
    tid.valor = 2002
except FrozenInstanceError as e:
    print("Error:", e)
```
```
1001
Error: cannot assign to field 'valor'
```
</details>

### Ejercicio 24 — Excepciones propias: jerarquía con 2 subclases
Define `DomainError(Exception)`, y dos subclases: `TicketNotFoundError` (con
`__init__(self, ticket_id)` que arma el mensaje) e `InvalidPriorityError` (vacía).
Escribe `buscar_ticket(tickets, ticket_id)` que recorra la lista y lance
`TicketNotFoundError` si no lo encuentra. Pruébala con un ID que no existe.

<details><summary>💡 ¿Sabías que…? — por qué una jerarquía y no solo `ValueError`, sección 12</summary>

Con una jerarquía propia se puede distinguir **qué tipo** de error de negocio pasó
(no encontrado vs. dato inválido) y capturarlos por separado — cada uno se puede
mapear después a un código HTTP distinto en una API (404 vs. 400).

```python
class DomainError(Exception):
    pass

class ProductoNoEncontradoError(DomainError):
    def __init__(self, product_id: int):
        super().__init__(f"Producto {product_id} no encontrado")

class StockInvalidoError(DomainError):
    pass

def buscar_producto(productos, product_id):
    for p in productos:
        if p["id"] == product_id:
            return p
    raise ProductoNoEncontradoError(product_id)

productos = [{"id": 1, "stock": 5}]
try:
    buscar_producto(productos, 999)
except ProductoNoEncontradoError as e:
    print(e)
```
```
Producto 999 no encontrado
```
</details>

<details><summary>Ver solución</summary>

```python
class DomainError(Exception):
    pass

class TicketNotFoundError(DomainError):
    def __init__(self, ticket_id: int):
        super().__init__(f"Ticket {ticket_id} no encontrado")

class InvalidPriorityError(DomainError):
    pass

def buscar_ticket(tickets, ticket_id):
    for t in tickets:
        if t["id"] == ticket_id:
            return t
    raise TicketNotFoundError(ticket_id)

tickets = [{"id": 1001, "priority": "Alta"}]
try:
    buscar_ticket(tickets, 9999)
except TicketNotFoundError as e:
    print(e)
```
```
Ticket 9999 no encontrado
```
</details>

### Ejercicio 25 — Capturar por la clase base (`except DomainError`)
Con la misma jerarquía del ejercicio 24, escribe `validar_prioridad(priority)` que
lance `InvalidPriorityError` si `priority` no es `"Alta"`/`"Media"`/`"Baja"`. Capturá
el error con `except DomainError` (la clase **base**, no la subclase exacta) e
imprime que se capturó.

<details><summary>💡 ¿Sabías que…? — `except` sobre la clase padre captura también las hijas, sección 12</summary>

Como `InvalidPriorityError` **hereda** de `DomainError`, un `except DomainError`
también la atrapa — así se puede tener un único manejador para "cualquier error de
negocio" sin listar cada subclase una por una.

```python
class DomainError(Exception):
    pass

class ProductoNoEncontradoError(DomainError):
    pass

class StockInvalidoError(DomainError):
    pass

def validar_stock(stock):
    if stock < 0:
        raise StockInvalidoError(f"Stock inválido: {stock}")

try:
    validar_stock(-3)
except DomainError as e:
    print("Error de dominio capturado:", e)
```
```
Error de dominio capturado: Stock inválido: -3
```
</details>

<details><summary>Ver solución</summary>

```python
class DomainError(Exception):
    pass

class TicketNotFoundError(DomainError):
    pass

class InvalidPriorityError(DomainError):
    pass

def validar_prioridad(priority):
    if priority not in ("Alta", "Media", "Baja"):
        raise InvalidPriorityError(f"Prioridad inválida: {priority}")

try:
    validar_prioridad("Urgentisima")
except DomainError as e:
    print("Error de dominio capturado:", e)
```
```
Error de dominio capturado: Prioridad inválida: Urgentisima
```
</details>

### Ejercicio 26 — `logging` con niveles
Configura `logging` con nivel `INFO` y formato `"%(levelname)s: %(message)s"`. Registra
un `logger.info(...)` para "Ticket 1001 creado" y un `logger.warning(...)` para
"Ticket 1002 sin prioridad asignada".

<details><summary>💡 ¿Sabías que…? — por qué `logging` y no `print`, sección 13</summary>

`print()` solo sirve si alguien está mirando la consola en vivo. `logging` deja un
registro con **nivel de severidad** (para poder filtrar después "solo errores", por
ejemplo) — necesario en un servicio corriendo en un servidor sin nadie mirando.

```python
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("inventario")

logger.info("Producto 2001 agregado al inventario")
logger.warning("Producto 2002 con stock bajo")
```
```
INFO: Producto 2001 agregado al inventario
WARNING: Producto 2002 con stock bajo
```
</details>

<details><summary>Ver solución</summary>

```python
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("tickets")

logger.info("Ticket 1001 creado")
logger.warning("Ticket 1002 sin prioridad asignada")
```
```
INFO: Ticket 1001 creado
WARNING: Ticket 1002 sin prioridad asignada
```
</details>

### Ejercicio 27 — Variables de entorno con valor por defecto
Lee `DB_HOST` y `DB_PORT` del entorno con `os.environ.get(...)`, con valores por
defecto `"127.0.0.1"` y `"5432"` si no existen. Imprime
`f"Conectando a {db_host}:{db_port}"`.

<details><summary>💡 ¿Sabías que…? — segundo argumento de `.get()` como valor por defecto, sección 14</summary>

`os.environ.get("CLAVE", "valor_por_defecto")` nunca lanza error aunque la variable no
exista — a diferencia de `os.environ["CLAVE"]`, que lanzaría `KeyError` si no está
definida. Útil para que el programa funcione igual en desarrollo sin configurar nada.

```python
import os

api_key = os.environ.get("API_KEY", "clave-de-desarrollo")
api_url = os.environ.get("API_URL", "http://localhost:8000")
print(f"Usando {api_url} con clave {api_key}")
```
```
Usando http://localhost:8000 con clave clave-de-desarrollo
```
</details>

<details><summary>Ver solución</summary>

```python
import os

db_host = os.environ.get("DB_HOST", "127.0.0.1")
db_port = os.environ.get("DB_PORT", "5432")
print(f"Conectando a {db_host}:{db_port}")
```
```
Conectando a 127.0.0.1:5432
```
</details>

### Ejercicio 28 — List comprehension: filtrar
Con la lista de tickets del ejercicio 24, arma `solo_altas` (lista de `id`) usando
una **comprehension**, solo con los de `priority == "Alta"`.

<details><summary>💡 ¿Sabías que…? — la comprehension "es" el `for`+`if`+`append()`, sección 15</summary>

`[t["id"] for t in tickets if t["priority"] == "Alta"]` hace exactamente lo mismo que
un `for` con `if` y `.append()` en 3 líneas — no es magia nueva, es la versión
compacta del mismo patrón ya practicado en el ejercicio 7.

```python
productos = [
    {"id": 1, "stock": 0},
    {"id": 2, "stock": 5},
    {"id": 3, "stock": 0},
]
sin_stock = [p["id"] for p in productos if p["stock"] == 0]
print(sin_stock)
```
```
[1, 3]
```
</details>

<details><summary>Ver solución</summary>

```python
tickets = [
    {"id": 1001, "priority": "Alta"},
    {"id": 1002, "priority": "Media"},
    {"id": 1003, "priority": "Alta"},
]
solo_altas = [t["id"] for t in tickets if t["priority"] == "Alta"]
print(solo_altas)
```
```
[1001, 1003]
```
</details>

### Ejercicio 29 — Dict comprehension: transformar
Con `tickets = [{"id": 1001, "priority": "Alta"}, {"id": 1002, "priority":
"Media"}]`, arma un diccionario `{id: priority}` usando una **dict comprehension**.

<details><summary>💡 ¿Sabías que…? — comprehension de diccionario, no solo de lista, sección 15</summary>

La sintaxis `{clave: valor for ... in ...}` (con `{}` y `:`) arma un `dict` en vez de
una `list` — mismo principio de "azúcar sintáctico para un `for`", pero acumulando
pares clave-valor en vez de elementos sueltos.

```python
productos = [
    {"id": 1, "nombre": "Teclado"},
    {"id": 2, "nombre": "Mouse"},
]
mapa_nombres = {p["id"]: p["nombre"] for p in productos}
print(mapa_nombres)
```
```
{1: 'Teclado', 2: 'Mouse'}
```
</details>

<details><summary>Ver solución</summary>

```python
tickets = [
    {"id": 1001, "priority": "Alta"},
    {"id": 1002, "priority": "Media"},
]
mapa_prioridades = {t["id"]: t["priority"] for t in tickets}
print(mapa_prioridades)
```
```
{1001: 'Alta', 1002: 'Media'}
```
</details>

### Ejercicio 30 — Integrador: `dataclass` + excepciones propias + `logging` + comprehension
Junta todo lo anterior: una `dataclass` `Ticket` (`id`, `priority`,
`tags: list[str] = field(default_factory=list)`), una excepción propia
`InvalidPriorityError(DomainError)`, una función `validar(ticket)` que la lance si la
prioridad no es válida, y `procesar_tickets(tickets)` que recorra la lista, valide
cada uno con `try`/`except`, registre con `logger.info`/`logger.warning` según el
caso, y devuelva los `id` válidos. Al final, arma también `solo_altas` con una
comprehension. Prueba con 3 tickets (uno con prioridad inválida).

<details><summary>💡 ¿Sabías que…? — por qué este es el ejercicio "más completo" de la clase</summary>

No hay ningún concepto nuevo acá — es la **combinación** de 4 secciones ya
practicadas por separado: `dataclass` (11) da la forma del dato, la jerarquía de
excepciones (12) modela qué puede salir mal, `logging` (13) deja registro de cada
caso, y la comprehension (15) arma el resumen final. Así se ve, en un solo lugar, cómo
estas piezas se combinan en un backend real. Ejemplo de referencia (mismo patrón,
otro dominio — productos e inventario):

```python
from dataclasses import dataclass, field
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("resumen")

class DomainError(Exception):
    pass

class StockInvalidoError(DomainError):
    pass

@dataclass
class Producto:
    id: int
    stock: int
    etiquetas: list[str] = field(default_factory=list)

def validar(producto: Producto) -> None:
    if producto.stock < 0:
        raise StockInvalidoError(f"Producto {producto.id}: stock inválido")

def procesar_productos(productos: list[Producto]) -> list[int]:
    validos = []
    for p in productos:
        try:
            validar(p)
            validos.append(p.id)
            logger.info(f"Producto {p.id} válido")
        except StockInvalidoError as e:
            logger.warning(str(e))
    return validos

productos = [
    Producto(id=1, stock=10),
    Producto(id=2, stock=-5),
    Producto(id=3, stock=0),
]
ids_validos = procesar_productos(productos)
print("IDs válidos:", ids_validos)

sin_stock = [p.id for p in productos if p.stock == 0]
print("Sin stock:", sin_stock)
```
```
INFO: Producto 1 válido
WARNING: Producto 2: stock inválido
INFO: Producto 3 válido
IDs válidos: [1, 3]
Sin stock: [3]
```
</details>

<details><summary>Ver solución</summary>

```python
from dataclasses import dataclass, field
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("resumen")

class DomainError(Exception):
    pass

class InvalidPriorityError(DomainError):
    pass

@dataclass
class Ticket:
    id: int
    priority: str
    tags: list[str] = field(default_factory=list)

def validar(ticket: Ticket) -> None:
    if ticket.priority not in ("Alta", "Media", "Baja"):
        raise InvalidPriorityError(f"Ticket {ticket.id}: prioridad inválida")

def procesar_tickets(tickets: list[Ticket]) -> list[int]:
    validos = []
    for t in tickets:
        try:
            validar(t)
            validos.append(t.id)
            logger.info(f"Ticket {t.id} válido")
        except InvalidPriorityError as e:
            logger.warning(str(e))
    return validos

tickets = [
    Ticket(id=1001, priority="Alta"),
    Ticket(id=1002, priority="Urgentisima"),
    Ticket(id=1003, priority="Media"),
]
ids_validos = procesar_tickets(tickets)
print("IDs válidos:", ids_validos)

solo_altas = [t.id for t in tickets if t.priority == "Alta"]
print("Solo altas:", solo_altas)
```
```
INFO: Ticket 1001 válido
WARNING: Ticket 1002: prioridad inválida
INFO: Ticket 1003 válido
IDs válidos: [1001, 1003]
Solo altas: [1001]
```
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
