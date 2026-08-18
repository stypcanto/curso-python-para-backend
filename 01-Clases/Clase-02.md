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

### 🔧 Mecánica de Python (funciones)
| Término | Qué es | Se profundiza en |
|---|---|---|
| `def` | Declara una función: un bloque de código con nombre, reutilizable. | sección 2 |
| Parámetro | Valor que la función recibe entre paréntesis y usa dentro de su bloque. | sección 2 |
| `return` | Devuelve un valor a quien llamó a la función, para poder reutilizarlo después. | sección 2 |
| Argumento | El valor concreto que se pasa al **llamar** a la función (`funcion(10, 5)`). | sección 2 |

### 🐍 Mecánica de Python (POO)
| Término | Qué es | Se profundiza en |
|---|---|---|
| `class` | Define el molde: qué datos y qué operaciones tendrá cada objeto creado a partir de ella. | sección 4 |
| `__init__` | El **constructor** — se ejecuta al crear el objeto y arma su estado inicial. | sección 4 |
| `self` | Referencia al propio objeto — así cada método sabe sobre cuál instancia trabaja. | sección 4 |
| Atributo | Dato que vive dentro del objeto (`self.title`). | sección 5 |
| Método | Función que vive en la clase y opera sobre el objeto (`assign()`, `close()`). | sección 5 |
| `@property` | Decorador que expone un método como si fuera un atributo de solo lectura (`ticket.status`, sin paréntesis). | sección 6 |
| `_atributo` (guion bajo) | Convención "protegido": señal de que es uso interno, Python no lo bloquea de verdad. | sección 6 |
| `ABC` / `@abstractmethod` | Clase base abstracta y decorador que obliga a las subclases a implementar un método, o Python no deja instanciarlas. | sección 7 |
| `super()` | Llama al método de la **clase padre** desde una subclase (`super().__init__(...)`). | sección 8 |
| `isinstance(obj, Clase)` | Verifica si un objeto es instancia de una clase (o de una subclase suya). | sección 8 |

### 🧱 Principios y patrones de diseño
| Término | Qué es | Se profundiza en |
|---|---|---|
| SOLID | Acrónimo de 5 principios de diseño orientado a objetos para reducir el costo del cambio. | sección 10 |
| Strategy | Patrón: cambia el algoritmo/regla usada sin modificar quien lo usa. | sección 12 |
| Factory | Patrón: centraliza en un solo lugar la lógica de "qué clase instanciar". | sección 12 |
| Singleton | Patrón: garantiza que exista una única instancia compartida de una clase. | sección 12 |

## 🔧 2. Funciones: repaso y profundización

> 📌 Antes de llegar a los métodos de un objeto (sección 5), repasamos y profundizamos
> la función "suelta" (ya vista en la Clase 1, sección 7) con los casos prácticos de
> esta clase — `funciones.py` y `gestortarea.py`.

Una función se declara con `def`, recibe **parámetros** entre paréntesis, y se ejecuta
recién cuando se **llama** (no al definirla). Puede **mostrar** un resultado con
`print()`, o **devolverlo** con `return` para que quien la llamó lo reutilice:

```python
def mi_primera_funcion(dato1, dato2):
    if dato1 > dato2:
        print(True)
    else:
        print(False)

mi_primera_funcion(10, 5)   # True — pero no se puede guardar en una variable
```

| | `print(...)` | `return ...` |
|---|---|---|
| Qué hace | Muestra el valor en la terminal. | Entrega el valor a quien llamó a la función. |
| Se puede reutilizar el resultado | No — se pierde apenas se imprime. | Sí — `resultado = mi_funcion(...)` guarda el valor. |
| Ejemplo en esta clase | `mi_primera_funcion()` (arriba). | `calculadora(a, b, operation)` — ver Laboratorio de la clase. |

**Varias funciones independientes compartiendo un mismo dato**, en vez de una sola
función gigante: `gestortarea.py` define `mostrar_tarea`, `agregar_tarea` y
`eliminar_tarea`, y a las tres se les **pasa la misma lista** como parámetro para que
operen sobre ella:

```python
def agregar_tarea(lista, tarea):
    lista.append(tarea)

def eliminar_tarea(lista, numero):
    indice = numero - 1
    lista.pop(indice)

tareas = []
agregar_tarea(tareas, "Programar en Python")
eliminar_tarea(tareas, 1)
```

> 💡 **Puente hacia POO:** estas funciones comparten el dato (`lista`) porque se lo
> pasamos **explícitamente** en cada llamada — si me olvido de pasarlo, la función no
> tiene forma de saber sobre qué lista trabajar. Desde la sección 4 en adelante se ve
> la alternativa: guardar ese dato **dentro** del objeto (`self.status`), para que el
> método no necesite recibirlo como parámetro cada vez, solo `self`.

## 🧭 3. De datos aislados a objetos: por qué POO
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

## 🏗️ 4. La clase como plantilla
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
print(ticket_1.ticket_id)
print(ticket_1.title)
print(ticket_1.priority)
print(ticket_1.status)
```
```
1001
Error al iniciar sesión
Alta
Pendiente
```

> 💡 Cada `print(ticket_1.xxx)` accede a un **atributo** por su nombre, sin paréntesis
> — se lee igual que acceder a una clave de un `dict` (`request["title"]`, Clase 1), pero
> con `.` en vez de `[...]` porque ahora el dato vive **dentro de un objeto**, no de un
> diccionario suelto.

> 📌 Mensaje clave de la clase: **la clase describe una estructura; cada objeto contiene
> su propio estado.** Dos `Ticket(...)` creados a partir de la misma clase son objetos
> distintos en memoria, aunque compartan la misma "forma" (mismo principio de identidad
> vs. igualdad que ya apareció con mutabilidad/aliasing en la Clase 1).

**Ejemplo con varios objetos de la misma clase**, para ver ese "propio estado" en
carne propia — tres `Perro` distintos, cada uno con sus propios valores:

```python
class Perro:
    def __init__(self, peso: float, talla: float, familia: str):
        self.peso = peso
        self.talla = talla
        self.familia = familia


perro_golden = Perro(15.5, 2.20, "Golden")
perro_salchicha = Perro(2.2, 1.2, "Salchicha")
perro_san_bernardo = Perro(15.3, 2604, "San Bernardo")

print(perro_golden.peso, perro_golden.familia)
print(perro_salchicha.peso, perro_salchicha.familia)
print(perro_san_bernardo.peso, perro_san_bernardo.familia)
```
```
15.5 Golden
2.2 Salchicha
15.3 San Bernardo
```

> ⚠️ Los tres objetos comparten la misma clase (mismos 3 atributos: `peso`, `talla`,
> `familia`) pero **cada uno guarda sus propios valores** — modificar
> `perro_golden.peso` no afecta a `perro_salchicha.peso` para nada, son objetos
> independientes en memoria. Nota aparte: `perro_san_bernardo` quedó con `talla = 2604`
> (probablemente un error de tipeo al practicar, ¿quiso decir `2.604`? un San Bernardo
> real mide ~0.7m) — se deja tal cual porque no rompe el ejercicio (sigue siendo un
> `float` válido), pero ilustra que Python **no valida rangos "razonables"** de un dato,
> solo su tipo.

## ⚙️ 5. Estado y comportamiento: atributos y métodos
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

### 🎫 Práctica: `objeto.py` — `Ticket` completo, atributos + métodos juntos
Segunda práctica de clases (después de `ticket.py`, que solo tenía atributos):
completar la clase `Ticket` de la teoría con sus tres métodos y probarlos en secuencia
real — crear el ticket, asignarlo y pedir su resumen.

```python
class Ticket:
    def __init__(self, ticket_id: int, title: str, priority: str):
        self.ticket_id = ticket_id
        self.title = title
        self.priority = priority
        self.status = "pendiente"

    def assign(self, technician: str) -> None:
        self.technician = technician
        self.status = "Asignado"

    def close(self) -> None:
        self.status = "Cerrado"

    def get_summary(self) -> str:
        return (
            f"{self.ticket_id} - "
            f"{self.title} - "
            f"{self.status} - "
            f"{self.technician}"
        )

ticket_1 = Ticket(1001, "Error de impresión", "Alta")
ticket_1.assign("Técnico 1")
print(ticket_1.get_summary())
```

<div class="terminal-shot">
  <div class="terminal-shot__titlebar">
    <span class="terminal-shot__dot terminal-shot__dot--red"></span>
    <span class="terminal-shot__dot terminal-shot__dot--yellow"></span>
    <span class="terminal-shot__dot terminal-shot__dot--green"></span>
    <span class="terminal-shot__title">zsh · objeto.py</span>
  </div>
  <pre class="terminal-shot__screen"><code><span class="terminal-shot__prompt">$</span> python3 objeto.py
<span class="terminal-shot__output">1001 - Error de impresión - Asignado - Técnico 1</span></code></pre>
</div>

**Paso a paso, exactamente qué hace cada línea al ejecutarse:**

| Paso | Línea | Qué pasa internamente |
|---|---|---|
| 1 | `ticket_1 = Ticket(1001, "Error de impresión", "Alta")` | Corre `__init__`: crea el objeto y le asigna 4 atributos (`ticket_id`, `title`, `priority`, `status="pendiente"`). **Todavía no existe** `self.technician` — no se le asignó ningún valor. |
| 2 | `ticket_1.assign("Técnico 1")` | Corre `assign()`: **recién acá** se crea el atributo `self.technician = "Técnico 1"` (en Python los atributos se crean al asignarlos, no hace falta declararlos antes) y cambia `self.status` de `"pendiente"` a `"Asignado"`. |
| 3 | `ticket_1.get_summary()` | Arma y devuelve el string final leyendo `self.ticket_id`, `self.title`, `self.status` (ya `"Asignado"`) y `self.technician` (ya existe porque el paso 2 corrió antes). |
| 4 | `print(...)` | Imprime el string devuelto por `get_summary()`. |

> ⚠️ **Orden importa:** si `get_summary()` se llamara **antes** de `assign(...)`, la
> línea `f"{self.technician}"` lanzaría `AttributeError: 'Ticket' object has no
> attribute 'technician'` — porque ese atributo todavía no existiría. Es una limitación
> real de este diseño (se resuelve inicializando `self.technician = None` en
> `__init__`, para que exista desde el arranque aunque esté vacío).

> 📝 **Bug corregido — comas en `get_summary()`:** la primera versión tenía una coma al
> final de cada línea dentro del `return (...)`:
> ```python
> return (
>     f"{self.ticket_id} - ",
>     f"{self.title} - ",
>     f"{self.status}"
> )
> ```
> Eso NO concatena strings — con comas, Python arma una **tupla** de 3 strings
> separados: `('1001 - ', 'Error de impresión - ', 'Asignado')`. La versión corregida
> **saca las comas**: varios strings literales escritos uno junto al otro (sin `+` ni
> `,` entre ellos, solo separados por espacio o salto de línea) se **concatenan
> automáticamente** en uno solo — es una regla propia de Python (*string literal
> concatenation*), no algo exclusivo de f-strings. Por eso ahora `get_summary()`
> devuelve un único `str` en vez de una tupla.

## 🔒 6. Encapsulamiento: proteger el estado interno
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

## 🎭 7. Abstracción: mostrar lo necesario, ocultar la implementación
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

## 🧬 8. Herencia: especializar comportamientos existentes
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

## 🧩 9. Composición: construir objetos a partir de otros objetos
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
> sección 7). Si mañana cambia el canal, `TicketService` no se toca.

> 🧪 Tip de entrevista: ¿cuándo herencia y cuándo composición? Herencia si el objeto **es
> un tipo más específico** del padre (`Technician` sigue siendo, ante todo, un `User`);
> composición si el objeto **usa el servicio de otro** para funcionar (`TicketService`
> usa un `NotificationChannel`, pero no "es" uno).

## 🧱 10. Principios SOLID
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

## 📁 11. Organización del proyecto
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
| `services/` | La lógica que coordina objetos del dominio — `TicketService` (sección 9). |
| `notifications/` | La abstracción `NotificationChannel` y sus implementaciones concretas (sección 7). |
| `policies/` | Reglas de negocio aisladas (p. ej. tiempos de respuesta según prioridad). |

> 💡 Esta separación es la antesala del **Repository Pattern** que se formaliza en la
> Clase 4 (PostgreSQL + SQLAlchemy) — la idea de aislar responsabilidades por carpeta ya
> aparece acá, solo que todavía sin base de datos real.

## 🧰 12. Patrones de diseño (profundización propia)
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
> respuesta a la pregunta de la sección 7 (¿qué tocar para agregar SMS?): un `Factory`
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
> mismo espíritu que `NotificationChannel` (sección 7): el consumidor programa contra un
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
| [`02-Ejercicios/Clase-02/funciones.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-02/funciones.py) | Primera función propia (`def`), con parámetros y un `if`/`else` que devuelve un booleano. |
| [`02-Ejercicios/Clase-02/gestortarea.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-02/gestortarea.py) | Gestor de tareas por consola: 3 funciones independientes (`mostrar_tarea`, `agregar_tarea`, `eliminar_tarea`) + un menú en bucle `while True`. |
| [`02-Ejercicios/Clase-02/ticket.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-02/ticket.py) | Primera práctica de clases: `Ticket` (con `__init__` y `print()` de cada atributo) y `Perro` (tres instancias con estado propio). |
| [`02-Ejercicios/Clase-02/objeto.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-02/objeto.py) | Segunda práctica de clases: `Ticket` completo con `__init__` + métodos (`assign()`, `close()`, `get_summary()`) — atributos **y** comportamiento juntos. |

> 📝 **Reclasificados a la Clase 1:** al revisar la grabación, `main.py` (jubilación),
> `contrasena.py`, `superheroes.py` y `calculadora.py` correspondían en realidad a la
> Clase 1, no a esta — se movieron a `02-Ejercicios/Clase-01/` y su documentación está
> ahora en [Clase 1](Clase-01.md).

### 🔧 `funciones.py` — primera función propia con `def`

> 📚 **¿Qué es una función y para qué sirve?** Una función es un bloque de código con
> **nombre**, que se define una sola vez (`def`) y se puede **reutilizar** llamándolo
> las veces que haga falta (`mi_primera_funcion(10, 5)`), en vez de repetir la misma
> lógica copiada y pegada. Entre paréntesis van los **parámetros** (`dato1`, `dato2`):
> valores que la función recibe de afuera y usa dentro de su propio bloque. La
> definición completa (con type hints y la regla de "una función, un propósito claro")
> ya está en [[Clase-01#🧩-7-organizando-y-reutilizando-la-logica-funciones-y-modulos]]
> de la Clase 1 — acá se aplica ese mismo concepto por primera vez a mano, sin type
> hints todavía.

Enunciado: definir una función propia que reciba dos datos y muestre si el primero es
mayor que el segundo.

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

| Parte | Qué hace | Detalle a notar |
|---|---|---|
| `def mi_primera_funcion(dato1, dato2):` | Declara la función y sus dos parámetros. | El nombre y los parámetros son elegidos por quien escribe la función — no son palabras reservadas. |
| `if dato1 > dato2:` | Compara los dos parámetros recibidos. | Con `10, 5` la condición es verdadera → entra al `if`. |
| `print(True)` / `print(False)` | Muestra el resultado de la comparación por pantalla. | La función **no usa `return`** — solo imprime. No devuelve ningún valor reutilizable a quien la llama (a diferencia de `calculadora()`, que sí hace `return`). |
| `mi_primera_funcion(10, 5)` | Llama a la función con valores concretos (los *argumentos*). | Sin esta línea, la función queda solo definida — nunca se ejecuta. |

> 📝 **Error corregido:** la primera versión escribía `print(true)` / `print(false)` en
> minúscula, lo que da `NameError: name 'true' is not defined` (Python incluso sugiere
> el error: *"Did you mean: 'True'?"*). A diferencia de JavaScript/Java, en Python los
> booleanos son **`True`/`False` con mayúscula inicial** — ver
> [[2026-08-14-nameerror-true-false-minuscula]].
>
> 💡 **`print` vs. `return` — por qué importa la diferencia:** esta función solo
> *muestra* el resultado en la terminal; si otra parte del programa necesitara *usar*
> ese `True`/`False` (guardarlo en una variable, pasarlo a otra función), habría que
> cambiar `print(...)` por `return ...`. Es la misma distinción que aparece en
> `calculadora.py` más abajo, que sí devuelve el resultado con `return` para poder
> imprimirlo después con `print("Resultado:", result)`.

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

> ✅ **Repaso — ¿está bien resuelto o lo compliqué de más?** El enunciado solo pedía
> 3 funciones independientes (mostrar / agregar / eliminar); todo lo demás que se le
> agregó **no es sobre-ingeniería**, tiene un motivo concreto:
> - El menú `while True` no era obligatorio, pero es lo que hace usable el programa
>   reutilizando esas 3 funciones.
> - `enumerate(lista, start=1)` es la forma estándar de numerar desde 1 (no magia).
> - El `try`/`except` de la opción 3 es el mismo patrón de manejo de errores ya visto
>   en la Clase 1, no algo nuevo inventado para complicar.
>
> Dos cosas para tener claras (no son errores, son el "por qué" del código):
> - `numero - 1` en `eliminar_tarea`: el usuario piensa "tarea 1, 2, 3...", pero las
>   listas de Python arrancan en índice `0` → hay que restar 1 para llegar al índice real.
> - `.pop(indice)` borra **y devuelve** el elemento borrado en el mismo paso — por eso
>   se puede armar el mensaje `f'Tarea "{borrada}" eliminada correctamente.'` sin haber
>   guardado el nombre antes.
>
> Detalle cosmético pendiente (no funcional): `print(f'{i}. []{t}')` imprime
> `1. []Programar en Python` sin espacio dentro de los corchetes — si el `[]` busca
> simular un checkbox vacío, se vería mejor como `[ ]` (con espacio) o `☐`.

### 🎫 `ticket.py` — primera práctica de clases y objetos
Enunciado: crear la clase `Ticket` de la teoría (sección 4), instanciar un ticket e
imprimir cada uno de sus atributos por separado. Después, para practicar que "cada
objeto tiene su propio estado", crear una clase `Perro` y tres instancias con datos
distintos.

```python
class Ticket:
    def __init__(self, ticket_id: int, title: str, priority: str):
        self.ticket_id = ticket_id
        self.title = title
        self.priority = priority
        self.status = "pendiente"

ticket_1 = Ticket(1001, "Error al inicial sesión", "Alta")
print(ticket_1.ticket_id)
print(ticket_1.title)
print(ticket_1.priority)
print(ticket_1.status)
```

<div class="terminal-shot">
  <div class="terminal-shot__titlebar">
    <span class="terminal-shot__dot terminal-shot__dot--red"></span>
    <span class="terminal-shot__dot terminal-shot__dot--yellow"></span>
    <span class="terminal-shot__dot terminal-shot__dot--green"></span>
    <span class="terminal-shot__title">zsh · ticket.py</span>
  </div>
  <pre class="terminal-shot__screen"><code><span class="terminal-shot__prompt">$</span> python3 ticket.py
<span class="terminal-shot__output">1001
Error al inicial sesión
Alta
pendiente
15.5 Golden
2.2 Salchicha
15.3 San Bernardo</span></code></pre>
</div>

> 📝 `"Error al inicial sesión"` quedó con una errata de tipeo (sería "inicia**r**
> sesión") — es solo el valor de un `str` que se está practicando, no afecta el
> funcionamiento del ejercicio, así que se documenta tal cual salió.

**Segunda parte — varios objetos, mismo molde:**

```python
class Perro:
    def __init__(self, peso: float, talla: float, familia: str):
        self.peso = peso
        self.talla = talla
        self.familia = familia

perro_golden = Perro(15.5, 2.20, "Golden")
perro_salchicha = Perro(2.2, 1.2, "Salchicha")
perro_san_bernardo = Perro(15.3, 2604, "San Bernardo")

print(perro_golden.peso, perro_golden.familia)
print(perro_salchicha.peso, perro_salchicha.familia)
print(perro_san_bernardo.peso, perro_san_bernardo.familia)
```

| Objeto | `peso` | `familia` |
|---|---|---|
| `perro_golden` | `15.5` | `"Golden"` |
| `perro_salchicha` | `2.2` | `"Salchicha"` |
| `perro_san_bernardo` | `15.3` | `"San Bernardo"` |

> 💡 Los tres objetos vienen de la **misma** clase `Perro` (comparten los 3 mismos
> atributos), pero cada `print()` muestra valores distintos — es la demostración en
> código de "la clase describe la estructura, cada objeto tiene su propio estado"
> (ver teoría, sección 4).

## 🎯 Reto de POO propuesto en la diapositiva de cierre
La empresa requiere registrar solicitudes y notificar al usuario; el canal de
notificación puede cambiar sin modificar el servicio principal. Se pide construir:

1. **Clase `Ticket`** — atributo de estado encapsulado, métodos `assign()` y `close()`.
2. **Abstracción `NotificationChannel`** — con implementación `EmailNotification` y
   composición dentro de `TicketService`.
3. **Separación en módulos** — responsabilidades claras, nombres descriptivos, tipos
   correctos y excepciones específicas (estructura `helpdesk/` de la sección 11).

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
