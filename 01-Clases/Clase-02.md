---
sidebar: "Clase 2 · POO y arquitectura"
---

# 📙 Clase 2 — Programación orientada a objetos y arquitectura

> Python para Backend · 2026-08-04 · Carpeta: `02-Ejercicios/Clase-02`
> ⬅️ Volver al [índice de clases](00-Indice.md)
> 📎 Material: [Presentación de la Clase 2](../04-Recursos/presentaciones/Clase%202.pdf) —
> "Programación Orientada a Objetos y Arquitectura en Python" (Tecylab)

## 🎯 Qué aprendí
- Por qué mover la lógica de diccionarios sueltos a objetos con estado y comportamiento.
- Clases, objetos, atributos y métodos (`Ticket`, `assign()`, `close()`, `get_summary()`).
- Encapsulamiento con `_atributo` + `@property` para impedir estados inválidos.
- Abstracción con `ABC` / `@abstractmethod` (`NotificationChannel`).
- Herencia ("es un") con `User` → `Technician`.
- Composición ("tiene un") con `TicketService`, que usa un `NotificationChannel`.
- Los 5 principios SOLID aplicados al dominio de tickets.
- Organización de un proyecto Python en módulos (`domain/`, `services/`,
  `notifications/`, `policies/`).
- *(profundización propia)* Los patrones Singleton, Factory y Strategy con ejemplos
  completos — la presentación solo los menciona de pasada.

# 📖 PARTE TEÓRICA

> 📌 Esta teoría viene de la presentación **real** de la Clase 2 ("Programación
> Orientada a Objetos y Arquitectura en Python", Tecylab —
> [`04-Recursos/presentaciones/Clase 2.pdf`](../04-Recursos/presentaciones/Clase%202.pdf)).
> Todo el código de las diapositivas está reproducido tal cual y verificado en terminal;
> las tablas y callouts son mi resumen "con mis propias palabras".

## 📚 1. Definiciones clave

### 🐍 Mecánica de Python (POO)
| Término | Qué es | Se profundiza en |
|---|---|---|
| `class` | Define el molde: qué datos y qué operaciones tendrá cada objeto creado a partir de ella. | sección 3 |
| `__init__` | El **constructor** — se ejecuta al crear el objeto y arma su estado inicial. | sección 3 |
| `self` | Referencia al propio objeto — así cada método sabe sobre cuál instancia trabaja. | sección 3 |
| Atributo | Dato que vive dentro del objeto (`self.title`). | sección 4 |
| Método | Función que vive en la clase y opera sobre el objeto (`assign()`, `close()`). | sección 4 |
| `@property` | Decorador que expone un método como si fuera un atributo de solo lectura (`ticket.status`, sin paréntesis). | sección 5 |
| `_atributo` (guion bajo) | Convención "protegido": señal de que es uso interno, Python no lo bloquea de verdad. | sección 5 |
| `ABC` / `@abstractmethod` | Clase base abstracta y decorador que obliga a las subclases a implementar un método, o Python no deja instanciarlas. | sección 6 |
| `super()` | Llama al método de la **clase padre** desde una subclase (`super().__init__(...)`). | sección 7 |
| `isinstance(obj, Clase)` | Verifica si un objeto es instancia de una clase (o de una subclase suya). | sección 7 |

### 🧱 Principios y patrones de diseño
| Término | Qué es | Se profundiza en |
|---|---|---|
| SOLID | Acrónimo de 5 principios de diseño orientado a objetos para reducir el costo del cambio. | sección 9 |
| Strategy | Patrón: cambia el algoritmo/regla usada sin modificar quien lo usa. | sección 11 |
| Factory | Patrón: centraliza en un solo lugar la lógica de "qué clase instanciar". | sección 11 |
| Singleton | Patrón: garantiza que exista una única instancia compartida de una clase. | sección 11 |

## 🧭 2. De datos aislados a objetos: por qué POO
En la Clase 1 representamos una solicitud como un `dict` suelto. Funciona mientras el
programa es chico, pero al crecer aparecen problemas estructurales:

| Problema | Qué significa |
|---|---|
| Reglas distribuidas | La lógica de negocio queda dispersa por todo el programa, no en un solo lugar. |
| Modificaciones sin control | Cualquier parte del código puede alterar el diccionario directamente, sin pasar por ninguna validación. |
| Lógica repetida | El mismo comportamiento (por ejemplo, "cerrar un ticket") se duplica en varios puntos. |
| Responsabilidades difusas | No queda claro qué parte del sistema es responsable de qué. |

> 💡 Pregunta que abrió la clase: **¿dónde debería vivir la lógica que permite cerrar
> una solicitud?** Con un `dict`, la respuesta es "en cualquier lado" — y ese es
> justamente el problema. La POO responde: **dentro del objeto que representa esa
> solicitud.**

## 🏗️ 3. La clase como plantilla
Una **clase** establece qué datos tendrá un elemento, qué operaciones podrá realizar y
qué reglas deberá respetar. Un **objeto** es una instancia concreta, con su propio
estado.

```python
class Ticket:
    def __init__(
        self, ticket_id: int,
        title: str, priority: str,
    ):
        self.ticket_id = ticket_id
        self.title = title
        self.priority = priority
        self.status = "Pendiente"


ticket_1 = Ticket(
    1001, "Error al iniciar sesión", "Alta"
)
```

> 📌 Mensaje clave de la clase: **la clase describe una estructura; cada objeto contiene
> su propio estado.** Dos `Ticket(...)` creados a partir de la misma clase son objetos
> distintos en memoria, aunque compartan la misma "forma" (mismo principio de identidad
> vs. igualdad que ya apareció con mutabilidad/aliasing en la Clase 1).

## ⚙️ 4. Estado y comportamiento: atributos y métodos
Un objeto no debería ser un contenedor pasivo de información — combina **atributos**
(el estado: identificador, título, prioridad, técnico asignado) con **métodos** (el
comportamiento: qué puede hacer ese objeto).

```python
class Ticket:
    def assign(self, technician: str) -> None:
        self.technician = technician
        self.status = "Asignado"

    def close(self) -> None:
        self.status = "Cerrado"

    def get_summary(self) -> str:
        return (
            f"{self.ticket_id} - "
            f"{self.title} - "
            f"{self.status}"
        )
```

| Método | Qué hace |
|---|---|
| `assign(technician)` | Asigna un técnico al ticket y cambia su estado a `"Asignado"`. |
| `close()` | Cierra el ticket. |
| `get_summary()` | Devuelve un resumen legible del ticket. |

## 🔒 5. Encapsulamiento: proteger el estado interno
El **encapsulamiento** centraliza las reglas de modificación y evita estados inválidos.
En vez de dejar que cualquiera reasigne `ticket.status = "lo que sea"` desde afuera, el
estado se guarda en un atributo "protegido" (`_status`) y se expone de solo lectura con
`@property`; los **cambios** de estado solo pueden pasar por los métodos de la clase.

```python
class Ticket:
    def __init__(self, ticket_id: int, title: str):
        self.ticket_id = ticket_id
        self.title = title
        self._status = "Pendiente"

    @property
    def status(self) -> str:
        return self._status

    def close(self) -> None:
        if self._status == "Cerrado":
            raise ValueError("Ya está cerrada")
        self._status = "Cerrado"
```
```python
t = Ticket(1001, "Error al iniciar sesión")
print(t.status)     # Pendiente (se lee como atributo, sin paréntesis)
t.close()
print(t.status)      # Cerrado
t.close()             # ValueError: Ya está cerrada
```

| Beneficio | Qué significa |
|---|---|
| Reglas centralizadas | Toda la lógica de validación vive en un único lugar (el método `close()`, no repartida por el programa). |
| Estados inválidos imposibles | Las transiciones incorrectas (cerrar dos veces) se previenen con excepciones. |
| Mantenimiento sencillo | Los cambios afectan solo a la clase, no a quienes la consumen. |

> ⚠️ Igual que se documentó como profundización en la Clase 1: Python **no tiene
> encapsulamiento estricto** como Java. `_status` es una convención — nada impide
> escribir `t._status = "lo que sea"` desde afuera, pero la señal para quien lee el
> código es clara: "no lo toques directo, usá los métodos".

## 🎭 6. Abstracción: mostrar lo necesario, ocultar la implementación
Una **abstracción** define **qué** operación debe existir, sin obligar al consumidor a
conocer sus detalles internos. En Python se formaliza con clases abstractas (`ABC`).

```python
from abc import ABC, abstractmethod

class NotificationChannel(ABC):
    @abstractmethod
    def send(
        self, recipient: str, message: str
    ) -> None:
        pass


class EmailNotification(NotificationChannel):
    def send(
        self, recipient: str, message: str
    ) -> None:
        print(
            f"Correo enviado a {recipient}: {message}"
        )
```

```python
NotificationChannel()   # TypeError: no se puede instanciar una clase abstracta
```

> 💡 **¿Por qué importa?** El sistema conoce la operación `send()`, pero ignora cómo se
> realiza el envío. Esto permite añadir nuevos canales (SMS, consola, webhook) **sin
> modificar** el código que ya los usa — la pregunta de cierre de esta sección en clase
> fue justo esa: *¿qué habría que tocar para agregar notificaciones por SMS?* Respuesta:
> solo crear `SMSNotification(NotificationChannel)` — nada más.

## 🧬 7. Herencia: especializar comportamientos existentes
La herencia modela una relación **"es un"**: una subclase reutiliza automáticamente el
comportamiento de su clase base y puede agregar el suyo propio.

```python
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email


class Technician(User):
    def __init__(
        self, name: str, email: str, specialty: str
    ):
        super().__init__(name, email)
        self.specialty = specialty

    def attend_ticket(self, ticket: Ticket) -> None:
        ticket.assign(self.name)
```

> 📌 `Technician` **es un** `User` con comportamiento adicional (`attend_ticket`) —
> `super().__init__(name, email)` reutiliza el constructor del padre en vez de repetir
> `self.name = name` / `self.email = email` a mano.

| Ventaja / riesgo | Qué significa |
|---|---|
| ✅ Reutilización | Las características comunes se heredan automáticamente. |
| ✅ Polimorfismo | Las subclases pueden usarse donde se espera la clase base (`isinstance(tech, User)` da `True`). |
| ⚠️ Jerarquías profundas | Demasiada herencia genera acoplamiento rígido y difícil de mantener. |

## 🧩 8. Composición: construir objetos a partir de otros objetos
La composición representa una relación **"tiene un"** y ofrece más flexibilidad que la
herencia: un objeto no *es* otro, sino que *usa* uno para funcionar.

```python
class TicketService:
    def __init__(
        self, notification: NotificationChannel
    ):
        self.notification = notification

    def register(
        self, ticket: Ticket, requester_email: str
    ) -> None:
        message = f"Solicitud {ticket.ticket_id} registrada"
        self.notification.send(
            requester_email, message
        )


service = TicketService(EmailNotification())
```

| | Herencia | Composición |
|---|---|---|
| Relación | "Es un" | "Tiene un" |
| Acoplamiento | Rígido | Flexible |
| Propósito | Especialización | Colaboración |
| Resultado | Clases relacionadas (jerarquía) | Objetos intercambiables |

> 💡 Regla del profe: **preferir composición cuando el comportamiento deba poder
> cambiarse** — `TicketService` no sabe (ni le importa) si `notification` es un email o
> un SMS, solo que cumple el contrato `NotificationChannel` (la abstracción de la
> sección 6). Si mañana cambia el canal, `TicketService` no se toca.

> 🧪 Tip de entrevista: ¿cuándo herencia y cuándo composición? Herencia si el objeto **es
> un tipo más específico** del padre (`Technician` sigue siendo, ante todo, un `User`);
> composición si el objeto **usa el servicio de otro** para funcionar (`TicketService`
> usa un `NotificationChannel`, pero no "es" uno).

## 🧱 9. Principios SOLID
Cinco principios de diseño orientado a objetos que buscan **reducir el costo del
cambio** — código fácil de extender sin romper lo que ya funciona.

| Letra | Principio | Idea principal | Ejemplo del dominio de tickets |
|---|---|---|---|
| **S** | Single Responsibility | Una clase, un solo motivo para cambiar | `Ticket` no envía correos |
| **O** | Open/Closed | Extender sin modificar lo existente | Agregar `SMSNotification` sin tocar las demás clases |
| **L** | Liskov Substitution | Toda subclase debe respetar el contrato de la base | Todo canal ejecuta `send()` igual |
| **I** | Interface Segregation | Contratos pequeños y específicos | Sin métodos innecesarios que una clase no vaya a usar |
| **D** | Dependency Inversion | Depender de abstracciones, no de clases concretas | `TicketService` depende de `NotificationChannel`, no de `EmailNotification` |

**Ejemplo incorrecto (viola SRP)** — una sola clase con tres motivos distintos para
cambiar (guardar en BD, enviar correo, generar PDF):
```python
class Ticket:
    def save_database(self): pass
    def send_email(self): pass
    def generate_pdf(self): pass
```

> ⚠️ Error común (ya señalado en la teoría de referencia previa): confundir "clase
> pequeña" (S) con "clase de un solo método". SRP habla de **una sola razón de
> negocio para cambiar**, no de un límite de líneas.

## 📁 10. Organización del proyecto
La convención de la clase separa el proyecto por **responsabilidad** (parecido al
principio S, pero a nivel de carpetas):

```
helpdesk/
├── main.py
├── domain/
│   ├── ticket.py
│   └── user.py
├── services/
│   └── ticket_service.py
├── notifications/
│   ├── base.py
│   ├── email.py
│   └── console.py
└── policies/
    └── response_time.py
```

| Carpeta | Qué contiene |
|---|---|
| `domain/` | Las entidades del dominio — `Ticket`, `User`/`Technician` (secciones 3, 4, 7). |
| `services/` | La lógica que coordina objetos del dominio — `TicketService` (sección 8). |
| `notifications/` | La abstracción `NotificationChannel` y sus implementaciones concretas (sección 6). |
| `policies/` | Reglas de negocio aisladas (p. ej. tiempos de respuesta según prioridad). |

> 💡 Esta separación es la antesala del **Repository Pattern** que se formaliza en la
> Clase 4 (PostgreSQL + SQLAlchemy) — la idea de aislar responsabilidades por carpeta ya
> aparece acá, solo que todavía sin base de datos real.

## 🧰 11. Patrones de diseño (profundización propia)
La diapositiva de cierre solo menciona de pasada **Strategy** (cambia reglas sin
modificar el consumidor) y **Factory** (centraliza la creación de objetos), con la idea
de fondo: *"un patrón es una solución reutilizable, no código para copiar"*. Amplío acá
con ejemplos completos y verificados, más un tercer patrón muy usado (Singleton), porque
son los que más se repiten en entrevistas de backend.

### Singleton — una sola instancia compartida
```python
class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.settings = {"env": "dev"}
        return cls._instance

c1 = ConfigManager()
c2 = ConfigManager()
c1.settings["env"] = "prod"
print(c2.settings)      # ve el cambio: es el MISMO objeto
print(c1 is c2)
```
```
{'env': 'prod'}
True
```
> 💡 Uso típico: un logger o una configuración global que debe ser **una sola** en toda
> la aplicación.

### Factory — centralizar la creación de objetos
```python
class EmailChannel:
    def send(self, message: str) -> None:
        print(f"Email: {message}")

class SMSChannel:
    def send(self, message: str) -> None:
        print(f"SMS: {message}")

def channel_factory(kind: str):
    channels = {"email": EmailChannel, "sms": SMSChannel}
    if kind not in channels:
        raise ValueError(f"Canal no soportado: {kind}")
    return channels[kind]()

channel = channel_factory("sms")
channel.send("Ticket 1001 actualizado")
```
```
SMS: Ticket 1001 actualizado
```
> 💡 Se usa cuando el código empieza a llenarse de `if`/`elif` para decidir qué clase
> instanciar — la Factory concentra esa decisión en un solo lugar. Es exactamente la
> respuesta a la pregunta de la sección 6 (¿qué tocar para agregar SMS?): un `Factory`
> centralizaría también esa decisión.

### Strategy — intercambiar el algoritmo sin tocar quien lo usa
```python
def by_priority(ticket: dict) -> int:
    order = {"Alta": 0, "Media": 1, "Baja": 2}
    return order[ticket["priority"]]

def by_id(ticket: dict) -> int:
    return ticket["id"]

def sort_tickets(tickets: list[dict], strategy) -> list[dict]:
    return sorted(tickets, key=strategy)

tickets = [
    {"id": 1001, "priority": "Baja"},
    {"id": 1002, "priority": "Alta"},
    {"id": 1003, "priority": "Media"},
]

print([t["id"] for t in sort_tickets(tickets, by_priority)])
print([t["id"] for t in sort_tickets(tickets, by_id)])
```
```
[1002, 1003, 1001]
[1001, 1002, 1003]
```
> 💡 `sort_tickets` no cambia — solo cambia **qué función de estrategia** le paso. Es el
> mismo espíritu que `NotificationChannel` (sección 6): el consumidor programa contra un
> contrato, no contra el detalle de cómo se resuelve.

| Patrón | Problema que resuelve |
|---|---|
| Singleton | Necesito una única instancia compartida (config, conexión a BD en la Clase 4+). |
| Factory | Necesito crear objetos sin acoplarme a la clase exacta. |
| Strategy | Necesito intercambiar un algoritmo/regla sin tocar el código que lo usa (Repository Pattern, Clase 4). |

> 🧪 Tip de entrevista: ¿diferencia entre Factory y Strategy? Factory decide **qué
> objeto crear**; Strategy decide **qué algoritmo ejecutar** sobre un objeto que ya
> existe. Se pueden combinar (una Factory que devuelve la Strategy correcta según el
> caso).

# 💻 PARTE PRÁCTICA

## 🧪 Laboratorio de la clase
Repasa conceptos de la Clase 1 (conversión de tipos con `int()`, condicionales
`if`/`else`, comparación de strings) aplicados a casos nuevos, antes de avanzar a los
ejercicios de POO.

| Archivo | Qué practica |
|---|---|
| [`02-Ejercicios/Clase-02/main.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-02/main.py) | Dado un empleado y su edad, determina si puede jubilarse (regla: 65 años o más). |
| [`02-Ejercicios/Clase-02/contrasena.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-02/contrasena.py) | Compara la contraseña ingresada contra una guardada de referencia con `==`, ignorando mayúsculas/minúsculas (`.lower()`). |
| [`02-Ejercicios/Clase-02/funciones.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-02/funciones.py) | Primera función propia (`def`), con parámetros y un `if`/`else` que devuelve un booleano. |
| [`02-Ejercicios/Clase-02/gestortarea.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-02/gestortarea.py) | Gestor de tareas por consola: 3 funciones independientes (`mostrar_tarea`, `agregar_tarea`, `eliminar_tarea`) + un menú en bucle `while True`. |
| [`02-Ejercicios/Clase-02/superheroes.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-02/superheroes.py) | Manipulación de listas: `.append()`, `.remove()` y reemplazo por índice con `.index()`. |

**Enunciado original de `contrasena.py`** (tal como lo planteó el ejercicio):
> Escribir un programa que almacene la cadena de caracteres `holamundo` en una variable,
> pregunte al usuario por la contraseña e imprima por pantalla si la contraseña
> introducida por el usuario coincide con la guardada en la variable **sin tener en
> cuenta mayúsculas y minúsculas**.

<div class="terminal-shot">
  <div class="terminal-shot__titlebar">
    <span class="terminal-shot__dot terminal-shot__dot--red"></span>
    <span class="terminal-shot__dot terminal-shot__dot--yellow"></span>
    <span class="terminal-shot__dot terminal-shot__dot--green"></span>
    <span class="terminal-shot__title">zsh · main.py / contrasena.py</span>
  </div>
  <pre class="terminal-shot__screen"><code><span class="terminal-shot__prompt">$</span> python3 main.py
Ingrese la edad del empleado: 70
<span class="terminal-shot__output">El empleado puede jubilarse
El empleado tiene 70 años</span>
<span class="terminal-shot__prompt">$</span> python3 contrasena.py
Ingrese la contraseña del usuario: holamundo
<span class="terminal-shot__output">La contraseña es correcta</span>
<span class="terminal-shot__prompt">$</span> python3 contrasena.py
Ingrese la contraseña del usuario: HOLAMUNDO
<span class="terminal-shot__output">La contraseña es correcta</span>
<span class="terminal-shot__prompt">$</span> python3 contrasena.py
Ingrese la contraseña del usuario: otraclave
<span class="terminal-shot__output">La contraseña es incorrecta</span></code></pre>
</div>

> 📌 `edad = int(input_edad)` repite el patrón de conversión de tipos de la Clase 1
> (`input()` siempre devuelve `str`, hay que convertirlo explícito antes de comparar con
> `>= 65`).

> 📝 **Corrección aplicada al revisar el enunciado:** la primera versión usaba
> `contrasena_usuario == contrasena_bd`, que **sí distingue mayúsculas de minúsculas** —
> pero el enunciado pide ignorarlas. Con `"HOLAMUNDO"` daba "incorrecta" cuando debía dar
> "correcta". Se corrigió normalizando ambos lados con `.lower()` antes de comparar
> (`.casefold()` es la alternativa más robusta si hubiera tildes/ñ):
> ```python
> if contrasena_usuario.lower() == contrasena_bd.lower():
>     print("La contraseña es correcta")
> else:
>     print("La contraseña es incorrecta")
> ```

> ⚠️ `contrasena.py` compara texto plano contra texto plano — perfecto para practicar
> `==` con strings, pero **nunca** así en un backend real: las contraseñas se guardan
> **hasheadas** (nunca en texto plano) y se comparan con funciones especiales resistentes
> a *timing attacks* (p. ej. `bcrypt`, o `hmac.compare_digest` en la librería estándar).
> Este patrón de "hashear y verificar credenciales" se retoma en las clases de
> autenticación/JWT del curso (Clase 7).

### 🔧 `funciones.py` — primera función propia con `def`
```python
def mi_primera_funcion(dato1, dato2):
    if dato1 > dato2:
        print(True)
    else:
        print(False)

mi_primera_funcion(10, 5)
```
<div class="terminal-shot">
  <div class="terminal-shot__titlebar">
    <span class="terminal-shot__dot terminal-shot__dot--red"></span>
    <span class="terminal-shot__dot terminal-shot__dot--yellow"></span>
    <span class="terminal-shot__dot terminal-shot__dot--green"></span>
    <span class="terminal-shot__title">zsh · funciones.py</span>
  </div>
  <pre class="terminal-shot__screen"><code><span class="terminal-shot__prompt">$</span> python3 funciones.py
<span class="terminal-shot__output">True</span></code></pre>
</div>

> 📝 **Error corregido:** la primera versión escribía `print(true)` / `print(false)` en
> minúscula, lo que da `NameError: name 'true' is not defined` (Python incluso sugiere
> el error: *"Did you mean: 'True'?"*). A diferencia de JavaScript/Java, en Python los
> booleanos son **`True`/`False` con mayúscula inicial** — ver
> [[2026-08-14-nameerror-true-false-minuscula]].

### 📋 `gestortarea.py` — funciones independientes + menú en bucle
Enunciado: construir un gestor de tareas dividido en **funciones independientes**
(mostrar / agregar / eliminar), reutilizadas desde un menú interactivo en `while True`.

```python
def mostrar_tarea(lista):
    """Imprime todas las tareas de la lista, numeradas desde 1."""
    if len(lista) == 0:
        print("No hay tareas pendientes.")
    else:
        print(f"Tienes {len(lista)} tareas pendientes:")
        for i, t in enumerate(lista, start=1):
            print(f'{i}. []{t}')


def agregar_tarea(lista, nueva_tarea):
    """Agrega una tarea nueva al final de la lista (modifica la lista original)."""
    lista.append(nueva_tarea)
    print(f'Tarea "{nueva_tarea}" agregada correctamente.')


def eliminar_tarea(lista, numero):
    """Elimina la tarea en la posición `numero` (numeración 1..N, no 0..N-1)."""
    if 1 <= numero <= len(lista):
        borrada = lista.pop(numero - 1)
        print(f'Tarea "{borrada}" eliminada correctamente.')
    else:
        print("Número de tarea inválido. No se pudo eliminar la tarea.")
```

| Función | Qué hace | Detalle a notar |
|---|---|---|
| `mostrar_tarea(lista)` | Imprime cada tarea numerada. | `enumerate(lista, start=1)` da el índice **empezando en 1**, para que el usuario vea "1. tarea" en vez de "0. tarea". |
| `agregar_tarea(lista, nueva_tarea)` | Agrega al final con `.append()`. | Modifica la lista **en el mismo lugar** (mismo concepto de mutabilidad de la Clase 1) — no hace falta `return`. |
| `eliminar_tarea(lista, numero)` | Borra por posición con `.pop()`. | `numero - 1`: el usuario piensa "tarea 1, 2, 3...", pero las listas empiezan en índice `0` — hay que restar 1 para llegar al índice real. |

<div class="terminal-shot">
  <div class="terminal-shot__titlebar">
    <span class="terminal-shot__dot terminal-shot__dot--red"></span>
    <span class="terminal-shot__dot terminal-shot__dot--yellow"></span>
    <span class="terminal-shot__dot terminal-shot__dot--green"></span>
    <span class="terminal-shot__title">zsh · gestortarea.py</span>
  </div>
  <pre class="terminal-shot__screen"><code><span class="terminal-shot__prompt">$</span> python3 gestortarea.py
&nbsp;
Gestor de Tareas
1. Mostrar tareas
2. Agregar tarea
3. Eliminar tarea
4. Salir
Seleccione una opción: 1
<span class="terminal-shot__output">Tienes 3 tareas pendientes:
1. []Programar en Python
2. []Hacer ejercicio
3. []Leer un libro</span>
&nbsp;
Gestor de Tareas
1. Mostrar tareas
2. Agregar tarea
3. Eliminar tarea
4. Salir
Seleccione una opción: 3
Ingrese el número de la tarea a eliminar: abc
<span class="terminal-shot__output">Eso no es un número válido. Intenta de nuevo.</span>
&nbsp;
Gestor de Tareas
1. Mostrar tareas
2. Agregar tarea
3. Eliminar tarea
4. Salir
Seleccione una opción: 3
Ingrese el número de la tarea a eliminar: 3
<span class="terminal-shot__output">Tarea "Programar en Python" eliminada correctamente.</span>
&nbsp;
Gestor de Tareas
1. Mostrar tareas
2. Agregar tarea
3. Eliminar tarea
4. Salir
Seleccione una opción: 4
<span class="terminal-shot__output">Saliendo del gestor de tareas.</span></code></pre>
</div>

> 📝 **Bug corregido:** `mostrar_tarea` tenía
> `print("Tienes " + len(lista) + "tareas pendientes:")` — `len(lista)` devuelve un
> `int`, y Python **no concatena `str + int` con `+`** (a diferencia de JS, que sí lo
> hace solo). Se cambió a f-string: `f"Tienes {len(lista)} tareas pendientes:"`.

> 💡 **Mejora agregada:** en la opción 3, `int(input(...))` explotaba con
> `ValueError` si el usuario escribía texto en vez de un número, cortando todo el
> programa. Se envolvió en `try`/`except ValueError` (mismo patrón de manejo de errores
> de la Clase 1) para que solo avise y deje reintentar, sin cerrar el gestor.

### 🦸 `superheroes.py` — añadir, eliminar y reemplazar en una lista
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

## 🎯 Reto de POO propuesto en la diapositiva de cierre
La empresa requiere registrar solicitudes y notificar al usuario; el canal de
notificación puede cambiar sin modificar el servicio principal. Se pide construir:

1. **Clase `Ticket`** — atributo de estado encapsulado, métodos `assign()` y `close()`.
2. **Abstracción `NotificationChannel`** — con implementación `EmailNotification` y
   composición dentro de `TicketService`.
3. **Separación en módulos** — responsabilidades claras, nombres descriptivos, tipos
   correctos y excepciones específicas (estructura `helpdesk/` de la sección 10).

> 🔜 *(pendiente)* Todavía no está resuelto en `02-Ejercicios/Clase-02/` — cuando lo
> tengas, se documenta acá con la salida verificada en terminal.

# 🏋️ EJERCICIOS CON SOLUCIÓN
*(pendiente — se documentan 10 ejercicios graduales de POO cuando esté resuelto el reto
de arriba)*

## ❓ Preguntas y respuestas (autoevaluación)
*(pendiente — 10 preguntas graduales sobre clases, encapsulamiento, abstracción,
herencia, composición y SOLID)*

## 📎 Apuntes relacionados
- [Clase 1](Clase-01.md) — tipos de datos, conversión con `int()`/`float()`, base de
  `dataclass` (antesala de los atributos tipados que ahora se ven en `Ticket`).
- [00-Notas/02-Conceptos.md](../00-Notas/02-Conceptos.md) — tabla de conceptos.

## ➡️ Siguiente
[Clase 3](Clase-03.md)
