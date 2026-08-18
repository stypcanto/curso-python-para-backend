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
| [`02-Ejercicios/Clase-02/calculadora.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-02/calculadora.py) | Función con 3 parámetros (`a`, `b`, `operation`) y una rama `if/elif` por operador; manejo de división por cero, división no exacta y operación inválida. |

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

### 🦸 `superheroes.py` — añadir, eliminar y reemplazar en una lista

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
> [[Clase-01#🖊️-práctica-libre-variables-sueltas-listas-y-diccionarios]] de la Clase 1.
>
> Métodos usados en este ejercicio:
>
> | Método | Qué hace |
> |---|---|
> | `.append(x)` | Agrega `x` al **final** de la lista. |
> | `.remove(x)` | Elimina la **primera aparición** del valor `x` (no por posición). |
> | `.index(x)` | Devuelve la **posición** (índice) donde está `x`, para poder reemplazarlo: `lista[lista.index(x)] = nuevo_valor`. |
> | `.pop(i)` | Elimina el elemento en la posición `i` **y lo devuelve** (usado en `gestortarea.py`). |

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

### 🧮 `calculadora.py` — función con `if/elif` por operador
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

> 📌 Repaso de **todo lo visto en esta clase**, de básico a completo: primero lo que ya
> se practicó en `02-Ejercicios/Clase-02/` (función propia, listas, `if`/`elif`,
> funciones independientes + manejo de errores), y después cada concepto de POO de la
> parte teórica (clase, encapsulamiento, abstracción, herencia, composición, patrón +
> SOLID) — en otro dominio y con otros datos, para practicar sin copiar.

### Ejercicio 1 — Función propia con `def`
Definí una función `es_par(numero)` que reciba un número entero y muestre por pantalla
si es par o impar (usando el operador `%`, resto de la división). Probala con el
número `7`. Salida esperada: `Es impar`.

<details><summary>💡 ¿Sabías que…? — repaso de `def` y parámetros</summary>

Repaso: una función se declara con `def nombre(parámetros):` y se ejecuta recién
cuando se **llama** (`nombre(valor)`), no al definirla — ver
[[Clase-02#🔧-funciones-py-—-primera-funcion-propia-con-def]]. Ejemplo de referencia
(otro caso, mismo patrón):

```python
def es_mayor_de_edad(edad):
    if edad >= 18:
        print("Es mayor de edad")
    else:
        print("Es menor de edad")

es_mayor_de_edad(16)
```
```
Es menor de edad
```
</details>

<details><summary>Ver solución</summary>

```python
def es_par(numero):
    if numero % 2 == 0:
        print("Es par")
    else:
        print("Es impar")

es_par(7)
```
```
Es impar
```
</details>

### Ejercicio 2 — Agregar, eliminar y reemplazar en una lista
Dada `frutas = ["Manzana", "Pera", "Uva", "Kiwi", "Mango"]`: (1) agregá `"Fresa"` al
final, (2) eliminá `"Uva"`, (3) reemplazá `"Kiwi"` por `"Piña"`. Imprimí la lista final.

<details><summary>💡 ¿Sabías que…? — repaso de `.append()`/`.remove()`/`.index()`</summary>

Repaso: `.append(x)` agrega al final, `.remove(x)` borra la primera aparición del
**valor**, y `lista[lista.index(x)] = nuevo` busca la posición de `x` para reemplazarlo
sin hardcodear el índice — ver [[Clase-02#🦸-superheroes-py-—-anadir-eliminar-y-reemplazar-en-una-lista]].
Ejemplo de referencia:

```python
colores = ["Rojo", "Verde", "Azul", "Amarillo"]
colores.append("Violeta")
colores.remove("Verde")
colores[colores.index("Amarillo")] = "Naranja"
print("Lista final de colores:", colores)
```
```
Lista final de colores: ['Rojo', 'Azul', 'Naranja', 'Violeta']
```
</details>

<details><summary>Ver solución</summary>

```python
frutas = ["Manzana", "Pera", "Uva", "Kiwi", "Mango"]

frutas.append("Fresa")
frutas.remove("Uva")
frutas[frutas.index("Kiwi")] = "Piña"

print("Lista final de frutas:", frutas)
```
```
Lista final de frutas: ['Manzana', 'Pera', 'Piña', 'Mango', 'Fresa']
```
</details>

### Ejercicio 3 — Función con `if`/`elif` por caso, y un caso inválido
Definí `convertir_temperatura(valor, escala)`: si `escala` es `'C'`, devuelve el valor
convertido de Celsius a Fahrenheit (`valor * 9/5 + 32`); si es `'F'`, de Fahrenheit a
Celsius (`(valor - 32) * 5/9`); si no es ninguna de las dos, devuelve un mensaje de
error. Probala con `25, 'C'`. Salida esperada: `Resultado: 77.0`.

<details><summary>💡 ¿Sabías que…? — repaso del patrón `if`/`elif`/`else` con `return`</summary>

Repaso: el último `else` evita que la función devuelva `None` en silencio cuando
ningún caso coincide — mismo patrón que la rama de operación inválida de
`calculadora()`, ver [[Clase-02#🧮-calculadora-py-—-funcion-con-if-elif-por-operador]].
Ejemplo de referencia:

```python
def convertir_distancia(valor, unidad):
    if unidad == 'km':
        return valor * 0.621371
    elif unidad == 'mi':
        return valor / 0.621371
    else:
        return "Error: unidad no válida. Usa 'km' o 'mi'."

print("Resultado:", convertir_distancia(10, 'km'))
```
```
Resultado: 6.21371
```
</details>

<details><summary>Ver solución</summary>

```python
def convertir_temperatura(valor, escala):
    if escala == 'C':
        return valor * 9/5 + 32
    elif escala == 'F':
        return (valor - 32) * 5/9
    else:
        return "Error: escala no válida. Usa 'C' o 'F'."

resultado = convertir_temperatura(25, 'C')
print("Resultado:", resultado)
```
```
Resultado: 77.0
```
</details>

### Ejercicio 4 — Funciones independientes + manejo de errores sobre una lista compartida
Escribí tres funciones independientes que operen sobre una misma lista de contactos:
`mostrar_contactos(lista)`, `agregar_contacto(lista, nombre)` y
`eliminar_contacto(lista, numero)` (recibe el número **tal como lo ve el usuario**,
empezando en 1; si el número no existe, avisa sin romper el programa). Agregá
`"Ana"` y `"Luis"`, mostrá la lista, eliminá el contacto 1 y mostrá de nuevo.

<details><summary>💡 ¿Sabías que…? — repaso de índice `numero - 1`, `.pop()` y `try`/`except`</summary>

Repaso: el usuario cuenta desde 1, pero las listas de Python arrancan en índice `0`
(de ahí `numero - 1`); `.pop(indice)` borra **y devuelve** el elemento en el mismo
paso; y envolver la conversión/acceso en `try`/`except` evita que un número inválido
corte el programa — ver [[Clase-02#📋-gestortarea-py-—-funciones-independientes-menu-en-bucle]].
Ejemplo de referencia (mismo patrón, con el caso de número inválido):

```python
def mostrar_pendientes(lista):
    if not lista:
        print("No hay pendientes.")
    else:
        print(f"Tienes {len(lista)} pendiente(s):")
        for i, item in enumerate(lista, start=1):
            print(f"{i}. {item}")

def agregar_pendiente(lista, texto):
    lista.append(texto)
    print(f'Pendiente "{texto}" agregado correctamente.')

def eliminar_pendiente(lista, numero):
    try:
        indice = numero - 1
        eliminado = lista.pop(indice)
        print(f'Pendiente "{eliminado}" eliminado correctamente.')
    except (IndexError, ValueError):
        print("Número de pendiente no válido.")

pendientes = []
agregar_pendiente(pendientes, "Pagar la luz")
agregar_pendiente(pendientes, "Llamar al dentista")
mostrar_pendientes(pendientes)
eliminar_pendiente(pendientes, 5)
```
```
Pendiente "Pagar la luz" agregado correctamente.
Pendiente "Llamar al dentista" agregado correctamente.
Tienes 2 pendiente(s):
1. Pagar la luz
2. Llamar al dentista
Número de pendiente no válido.
```
</details>

<details><summary>Ver solución</summary>

```python
def mostrar_contactos(lista):
    if not lista:
        print("No hay contactos.")
    else:
        print(f"Tienes {len(lista)} contacto(s):")
        for i, contacto in enumerate(lista, start=1):
            print(f"{i}. {contacto}")

def agregar_contacto(lista, nombre):
    lista.append(nombre)
    print(f'Contacto "{nombre}" agregado correctamente.')

def eliminar_contacto(lista, numero):
    try:
        indice = numero - 1
        eliminado = lista.pop(indice)
        print(f'Contacto "{eliminado}" eliminado correctamente.')
    except (IndexError, ValueError):
        print("Número de contacto no válido.")

contactos = []
agregar_contacto(contactos, "Ana")
agregar_contacto(contactos, "Luis")
mostrar_contactos(contactos)
eliminar_contacto(contactos, 1)
mostrar_contactos(contactos)
```
```
Contacto "Ana" agregado correctamente.
Contacto "Luis" agregado correctamente.
Tienes 2 contacto(s):
1. Ana
2. Luis
Contacto "Ana" eliminado correctamente.
Tienes 1 contacto(s):
1. Luis
```
</details>

### Ejercicio 5 — Una clase con atributos y métodos
Definí una clase `Producto` con atributos `nombre`, `precio` y `stock`, y métodos
`vender(cantidad)` (resta del stock), `reponer(cantidad)` (suma al stock) y
`resumen()` (devuelve un string legible). Creá un `Producto("Teclado", 25000, 10)`,
vendé 3, reponé 5 e imprimí el resumen.

<details><summary>💡 ¿Sabías que…? — repaso de clase, `__init__` y métodos</summary>

Repaso: la clase define la estructura (atributos + métodos), `__init__` arma el
estado inicial de cada objeto, y los métodos operan sobre `self` — ver
[[Clase-02#🏗️-3-la-clase-como-plantilla]] y [[Clase-02#⚙️-4-estado-y-comportamiento-atributos-y-metodos]].
Ejemplo de referencia:

```python
class Empleado:
    def __init__(self, nombre, salario_base, horas_extra):
        self.nombre = nombre
        self.salario_base = salario_base
        self.horas_extra = horas_extra

    def agregar_horas(self, cantidad):
        self.horas_extra += cantidad

    def calcular_pago(self):
        return self.salario_base + (self.horas_extra * 5000)

    def resumen(self):
        return f"{self.nombre}: ${self.calcular_pago()} ({self.horas_extra}h extra)"

ana = Empleado("Ana", 800000, 2)
ana.agregar_horas(3)
print(ana.resumen())
```
```
Ana: $825000 (5h extra)
```
</details>

<details><summary>Ver solución</summary>

```python
class Producto:
    def __init__(self, nombre, precio, stock):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def vender(self, cantidad):
        self.stock -= cantidad

    def reponer(self, cantidad):
        self.stock += cantidad

    def resumen(self):
        return f"{self.nombre}: {self.stock} unidades a ${self.precio}"

teclado = Producto("Teclado", 25000, 10)
teclado.vender(3)
teclado.reponer(5)
print(teclado.resumen())
```
```
Teclado: 12 unidades a $25000
```
</details>

### Ejercicio 6 — Encapsulamiento con `_atributo` + `@property`
Definí `CuentaBancaria` con `titular` y saldo **protegido** (`_saldo`), expuesto de
solo lectura con `@property saldo`. El método `retirar(monto)` debe lanzar
`ValueError("Fondos insuficientes")` si `monto` supera el saldo. Creá una cuenta con
$1000, retirá $300 (imprimí el saldo), y después intentá retirar $2000.

<details><summary>💡 ¿Sabías que…? — repaso de `_atributo`, `@property` y estados inválidos</summary>

Repaso: el guion bajo es una **convención** (Python no bloquea el acceso de verdad),
`@property` expone el valor de solo lectura, y las transiciones inválidas se
bloquean con una excepción dentro del método — mismo patrón que `Ticket.close()` en
[[Clase-02#🔒-5-encapsulamiento-proteger-el-estado-interno]]. Ejemplo de referencia:

```python
class Almacen:
    def __init__(self, producto, stock_inicial):
        self.producto = producto
        self._stock = stock_inicial

    @property
    def stock(self):
        return self._stock

    def despachar(self, cantidad):
        if cantidad > self._stock:
            raise ValueError("Stock insuficiente")
        self._stock -= cantidad

almacen = Almacen("Cajas", 50)
almacen.despachar(20)
print(almacen.stock)
almacen.despachar(100)
```
```
30
ValueError: Stock insuficiente
```
</details>

<details><summary>Ver solución</summary>

```python
class CuentaBancaria:
    def __init__(self, titular, saldo_inicial):
        self.titular = titular
        self._saldo = saldo_inicial

    @property
    def saldo(self):
        return self._saldo

    def retirar(self, monto):
        if monto > self._saldo:
            raise ValueError("Fondos insuficientes")
        self._saldo -= monto

cuenta = CuentaBancaria("Ana", 1000)
cuenta.retirar(300)
print(cuenta.saldo)
cuenta.retirar(2000)
```
```
700
ValueError: Fondos insuficientes
```
</details>

### Ejercicio 7 — Abstracción con `ABC` / `@abstractmethod`
Definí una clase abstracta `PaymentMethod` con el método abstracto `pay(amount)`, y
una implementación concreta `CreditCardPayment` que imprima el pago realizado. Creá un
`CreditCardPayment()`, pagá `500`, y después intentá instanciar `PaymentMethod()`
directamente.

<details><summary>💡 ¿Sabías que…? — repaso de `ABC` y por qué no se puede instanciar</summary>

Repaso: `ABC` + `@abstractmethod` define **qué** operación debe existir sin
implementarla; instanciar la clase abstracta directamente lanza `TypeError` — ver
[[Clase-02#🎭-6-abstraccion-mostrar-lo-necesario-ocultar-la-implementacion]]. Ejemplo
de referencia:

```python
from abc import ABC, abstractmethod

class ExportFormat(ABC):
    @abstractmethod
    def export(self, data):
        pass

class CSVExport(ExportFormat):
    def export(self, data):
        print(f"Exportando a CSV: {data}")

exporter = CSVExport()
exporter.export("reporte de ventas")
ExportFormat()
```
```
Exportando a CSV: reporte de ventas
TypeError: Can't instantiate abstract class ExportFormat without an implementation for abstract method 'export'
```
</details>

<details><summary>Ver solución</summary>

```python
from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class CreditCardPayment(PaymentMethod):
    def pay(self, amount):
        print(f"Pago de ${amount} realizado con tarjeta de crédito")

payment = CreditCardPayment()
payment.pay(500)
PaymentMethod()
```
```
Pago de $500 realizado con tarjeta de crédito
TypeError: Can't instantiate abstract class PaymentMethod without an implementation for abstract method 'pay'
```
</details>

### Ejercicio 8 — Herencia con `super()`
Definí `Vehicle` con `brand` y `model`, y `Car(Vehicle)` que agrega `doors` y un
método `info()`. El `__init__` de `Car` debe reutilizar el de `Vehicle` con
`super()`. Creá `Car("Toyota", "Corolla", 4)`, imprimí `info()` y comprobá que
`isinstance(car, Vehicle)` es `True`.

<details><summary>💡 ¿Sabías que…? — repaso de "es un" y `super().__init__()`</summary>

Repaso: la herencia modela "es un" — `Car` **es un** `Vehicle` con comportamiento
adicional — y `super().__init__(...)` reutiliza el constructor del padre en vez de
repetir sus atributos a mano, ver [[Clase-02#🧬-7-herencia-especializar-comportamientos-existentes]].
Ejemplo de referencia:

```python
class Publication:
    def __init__(self, title, author):
        self.title = title
        self.author = author

class Book(Publication):
    def __init__(self, title, author, pages):
        super().__init__(title, author)
        self.pages = pages

    def info(self):
        return f"{self.title} de {self.author} ({self.pages} páginas)"

book = Book("Clean Code", "Robert C. Martin", 464)
print(book.info())
print(isinstance(book, Publication))
```
```
Clean Code de Robert C. Martin (464 páginas)
True
```
</details>

<details><summary>Ver solución</summary>

```python
class Vehicle:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

class Car(Vehicle):
    def __init__(self, brand, model, doors):
        super().__init__(brand, model)
        self.doors = doors

    def info(self):
        return f"{self.brand} {self.model} ({self.doors} puertas)"

car = Car("Toyota", "Corolla", 4)
print(car.info())
print(isinstance(car, Vehicle))
```
```
Toyota Corolla (4 puertas)
True
```
</details>

### Ejercicio 9 — Composición: un servicio que usa una abstracción
Definí `OrderService`, que recibe un `PaymentMethod` (Ejercicio 7) en su constructor
y en `checkout(amount)` imprime `"Procesando compra..."` y delega el pago al método
recibido. Creá el servicio con un `CreditCardPayment()` y hacé `checkout(750)`.

<details><summary>💡 ¿Sabías que…? — repaso de "tiene un" vs. "es un"</summary>

Repaso: `OrderService` no **es** un método de pago, **usa** uno — la misma relación
que `TicketService` con `NotificationChannel`, ver
[[Clase-02#🧩-8-composicion-construir-objetos-a-partir-de-otros-objetos]]. Gracias a
que ambos programan contra la abstracción (Ejercicio 7), el método de pago puede
cambiarse sin tocar `OrderService`. Ejemplo de referencia:

```python
class ReportService:
    def __init__(self, export_format):
        self.export_format = export_format

    def generate(self, data):
        print("Generando reporte...")
        self.export_format.export(data)

service = ReportService(CSVExport())
service.generate("ventas de agosto")
```
```
Generando reporte...
Exportando a CSV: ventas de agosto
```
</details>

<details><summary>Ver solución</summary>

```python
class OrderService:
    def __init__(self, payment_method):
        self.payment_method = payment_method

    def checkout(self, amount):
        print("Procesando compra...")
        self.payment_method.pay(amount)

service = OrderService(CreditCardPayment())
service.checkout(750)
```
```
Procesando compra...
Pago de $750 realizado con tarjeta de crédito
```
</details>

### Ejercicio 10 — Integración: patrón Strategy + principio Open/Closed
Escribí dos funciones de descuento, `descuento_regular(precio)` (no descuenta nada) y
`descuento_black_friday(precio)` (30% off), y una función `aplicar_descuento(precio,
estrategia)` que reciba **cuál** función de descuento usar como parámetro. Probala con
`1000` y cada estrategia.

<details><summary>💡 ¿Sabías que…? — repaso de Strategy y por qué es Open/Closed</summary>

Repaso: `aplicar_descuento` no cambia — solo cambia qué función de estrategia recibe
— mismo espíritu que `sort_tickets(tickets, strategy)` de
[[Clase-02#🧰-11-patrones-de-diseno-profundizacion-propia]]. Es también un ejemplo de
**Open/Closed (O)**: agregar una promoción nueva (`descuento_navidad`) no requiere
tocar `aplicar_descuento`. Ejemplo de referencia:

```python
def envio_estandar(peso_kg):
    return peso_kg * 2000

def envio_express(peso_kg):
    return peso_kg * 2000 + 5000

def calcular_envio(peso_kg, estrategia):
    return estrategia(peso_kg)

print(calcular_envio(3, envio_estandar))
print(calcular_envio(3, envio_express))
```
```
6000
11000
```
</details>

<details><summary>Ver solución</summary>

```python
def descuento_regular(precio):
    return precio

def descuento_black_friday(precio):
    return precio * 0.7

def aplicar_descuento(precio, estrategia):
    return estrategia(precio)

print(aplicar_descuento(1000, descuento_regular))
print(aplicar_descuento(1000, descuento_black_friday))
```
```
1000
700.0
```
</details>

## ❓ Preguntas y respuestas (autoevaluación)

**1. ¿Cuál es la diferencia entre una clase y un objeto?**
> La clase es el **molde**: define qué datos y qué operaciones tendrá cada elemento
> creado a partir de ella (sección 3). El objeto es una **instancia concreta**, con su
> propio estado en memoria — `Ticket` es la clase, `ticket_1 = Ticket(1001, ...)` es un
> objeto. Dos objetos de la misma clase son distintos entre sí aunque compartan la misma
> "forma".

**2. ¿Para qué sirven `__init__` y `self` dentro de una clase?**
> `__init__` es el **constructor**: se ejecuta automáticamente al crear el objeto y arma
> su estado inicial (`self.ticket_id = ticket_id`, etc.). `self` es la referencia al
> **propio objeto** — gracias a `self`, cada método sabe sobre cuál instancia está
> trabajando, y sin él Python no tendría forma de distinguir `ticket_1.close()` de
> `ticket_2.close()` (sección 3).

**3. En la clase `Ticket`, ¿qué es un atributo y qué es un método? Da un ejemplo de cada uno.**
> El **atributo** es el estado que vive dentro del objeto — un dato, como
> `self.ticket_id` o `self.status`. El **método** es una función que vive en la clase y
> opera sobre ese estado — por ejemplo `assign(technician)` (cambia `status` a
> `"Asignado"`) o `close()` (cambia `status` a `"Cerrado"`) (sección 4).

**4. `Ticket` guarda el estado en `_status` (con guion bajo) y lo expone con
`@property status`, en vez de un simple `self.status` público. ¿Qué gana el código con
eso?**
> Encapsulamiento: todas las reglas de cambio de estado quedan centralizadas en los
> métodos de la clase (`close()`), en vez de que cualquier parte del programa pueda
> hacer `ticket.status = "lo que sea"` sin validar nada. Así, transiciones inválidas
> (cerrar un ticket ya cerrado) se pueden bloquear con una excepción en un único lugar
> (sección 5). `_status` es solo una **convención** — Python no impide de verdad escribir
> `t._status = "x"` desde afuera, pero comunica "no lo toques directo".

**5. ¿Qué hace que `NotificationChannel` sea una clase abstracta, y qué pasa si se
intenta hacer `NotificationChannel()` directamente?**
> Hereda de `ABC` y su método `send()` está decorado con `@abstractmethod` (sección 6).
> Eso significa que define **qué** operación debe existir (`send(recipient, message)`)
> sin implementarla, y obliga a cada subclase concreta (`EmailNotification`) a
> implementarla. Instanciar `NotificationChannel()` directamente lanza `TypeError`:
> Python no deja crear objetos de una clase con métodos abstractos sin implementar.

**6. `Technician` hereda de `User` y su `__init__` empieza con
`super().__init__(name, email)`. ¿Qué relación modela la herencia y para qué sirve ese
`super()`?**
> La herencia modela una relación **"es un"** — `Technician` **es un** `User` con
> comportamiento adicional (`attend_ticket`) (sección 7). `super().__init__(...)` llama
> al constructor de la clase padre para reutilizar su lógica (`self.name = name`,
> `self.email = email`) en vez de repetirla a mano en la subclase.

**7. `TicketService` recibe un `NotificationChannel` en su constructor en vez de heredar
de él. ¿Por qué se eligió composición ("tiene un") y no herencia ("es un") en este caso?**
> Porque `TicketService` no **es** un canal de notificación, **usa** uno para funcionar
> — la relación correcta es "tiene un" (sección 8). Con composición, `TicketService` no
> sabe (ni le importa) si `self.notification` es un email o un SMS, solo que cumple el
> contrato `NotificationChannel`; si mañana cambia el canal, `TicketService` no se toca.
> Regla del profe: preferir composición cuando el comportamiento deba poder cambiarse.

**8. De los 5 principios SOLID, ¿cuáles dos se ven más claramente reflejados en el diseño
`TicketService` + `NotificationChannel` (abstracción) del reto de POO, y por qué?**
> **Dependency Inversion (D):** `TicketService` depende de la abstracción
> `NotificationChannel`, no de una clase concreta como `EmailNotification` — puede
> recibir cualquier canal que cumpla el contrato. **Open/Closed (O):** para agregar un
> canal nuevo (SMS, webhook) alcanza con crear `SMSNotification(NotificationChannel)`
> sin modificar `TicketService` ni las clases existentes (sección 9).

**9. ¿Cuál es la diferencia entre el patrón Factory y el patrón Strategy? Menciona un
ejemplo de cada uno.**
> Factory decide **qué objeto crear** — `channel_factory("sms")` centraliza en un solo
> lugar la lógica de instanciar `EmailChannel` o `SMSChannel` según un parámetro, en vez
> de esparcir `if`/`elif` por el código. Strategy decide **qué algoritmo ejecutar** sobre
> algo que ya existe — `sort_tickets(tickets, by_priority)` recibe la función de orden
> como parámetro sin cambiar `sort_tickets` (sección 11). Se pueden combinar: una Factory
> que devuelve la Strategy correcta según el caso.

**10. En el reto de POO de cierre (`Ticket`, `NotificationChannel` + `EmailNotification`,
`TicketService`), ¿qué patrón de diseño de la sección 11 describe mejor la relación
`TicketService` → `NotificationChannel`, y qué principio SOLID garantiza que sea seguro
agregar un canal nuevo sin romper nada?**
> Es el mismo espíritu que **Strategy**: `TicketService` programa contra el contrato
> `NotificationChannel.send()`, no contra una implementación concreta, así que el canal
> puede intercambiarse sin tocar `TicketService` (secciones 8 y 11). El principio que lo
> garantiza es **Open/Closed (O)**: el sistema queda abierto a extensión (agregar
> `SMSNotification`) pero cerrado a modificación (no hay que tocar `TicketService` ni las
> clases existentes) — la misma pregunta que cerró la sección 6 de la teoría.

## 📎 Apuntes relacionados
- [Clase 1](Clase-01.md) — tipos de datos, conversión con `int()`/`float()`, base de
  `dataclass` (antesala de los atributos tipados que ahora se ven en `Ticket`).
- [00-Notas/02-Conceptos.md](../00-Notas/02-Conceptos.md) — tabla de conceptos.

## ➡️ Siguiente
[Clase 3](Clase-03.md)
