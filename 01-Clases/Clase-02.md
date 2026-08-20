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
- Abstracción con `ABC` / `@abstractmethod` (`NotificationChannel`) — resuelta en la
  práctica con `notification_channel.py` → `EmailNotification` + `WhatsAppNotification`
  → `main.py`.
- Herencia ("es un") con `User` → `Technician`.
- Composición ("tiene un") con `TicketService`, que usa un `NotificationChannel`.
- Los 5 principios SOLID aplicados al dominio de tickets.
- Organización de un proyecto Python en módulos (`domain/`, `services/`,
  `notifications/`, `policies/`).
- *(profundización propia)* Los patrones Singleton, Factory y Strategy con ejemplos
  completos — la presentación solo los menciona de pasada.

## 🗂️ Índice de esta clase

**📖 Parte teórica**
1. [Definiciones clave](#📚-1-definiciones-clave)
2. [Funciones: repaso y profundización](#🔧-2-funciones-repaso-y-profundizacion)
3. [De datos aislados a objetos: por qué POO](#🧭-3-de-datos-aislados-a-objetos-por-que-poo)
4. [La clase como plantilla](#🏗️-4-la-clase-como-plantilla)
5. [Estado y comportamiento: atributos y métodos](#⚙️-5-estado-y-comportamiento-atributos-y-metodos)
   - [Práctica: `objeto.py` — `Ticket` completo](#🎫-practica-objeto-py-—-ticket-completo-atributos-metodos-juntos)
6. [Encapsulamiento: proteger el estado interno](#🔒-6-encapsulamiento-proteger-el-estado-interno)
7. [Abstracción: mostrar lo necesario, ocultar la implementación](#🎭-7-abstraccion-mostrar-lo-necesario-ocultar-la-implementacion)
8. [Herencia: especializar comportamientos existentes](#🧬-8-herencia-especializar-comportamientos-existentes)
9. [Composición: construir objetos a partir de otros objetos](#🧩-9-composicion-construir-objetos-a-partir-de-otros-objetos)
10. [Principios SOLID](#🧱-10-principios-solid) — con diagrama
11. [Organización del proyecto](#📁-11-organizacion-del-proyecto)
12. [Patrones de diseño (profundización propia)](#🧰-12-patrones-de-diseno-profundizacion-propia)
    - [Singleton](#singleton-—-una-sola-instancia-compartida) ·
      [Factory](#factory-—-centralizar-la-creacion-de-objetos) ·
      [Strategy](#strategy-—-intercambiar-el-algoritmo-sin-tocar-quien-lo-usa)

**💻 Parte práctica**
- [Laboratorio de la clase](#🧪-laboratorio-de-la-clase)
  - [`funciones.py`](#🔧-funciones-py-—-primera-funcion-propia-con-def) ·
    [`gestortarea.py`](#📋-gestortarea-py-—-funciones-independientes-menu-en-bucle) ·
    [`ticket.py`](#🎫-ticket-py-—-primera-practica-de-clases-y-objetos)
- [Reto de POO propuesto en la diapositiva de cierre](#🎯-reto-de-poo-propuesto-en-la-diapositiva-de-cierre)
  - [La abstracción en 4 archivos (resuelto)](#🔔-notification-channel-py-emailnotification-py-whatsapp-notifiaction-py-main-py-—-la-abstraccion-en-4-archivos)
  - [`encapsulamiento.py`](#🔒-encapsulamiento-py-—-practicando-el-status-de-objeto-py)

**🏋️ Ejercicios y autoevaluación**
- [Ejercicios con solución](#🏋️-ejercicios-con-solucion) — 24 de 24 listos
- [Preguntas y respuestas](#❓-preguntas-y-respuestas-autoevaluacion) *(pendiente)*

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
real — crear el ticket, asignarlo y pedir su resumen. El archivo real ya quedó
comentado línea por línea (útil para releerlo sin volver acá):

```python
# Clase Ticket: define la "forma" de un ticket (qué datos tiene y qué puede hacer),
# no un ticket en sí. Cada Ticket(...) que se cree es un objeto separado, con sus
# propios valores guardados en self.

class Ticket:
    def __init__(self, ticket_id: int, title: str, priority: str):
        # __init__ es el constructor: se ejecuta automáticamente al crear el objeto
        # (Ticket(...)) y arma su estado inicial guardando cada dato en "self".
        self.ticket_id = ticket_id
        self.title = title
        self.priority = priority
        self.status = "pendiente"  # todo ticket nuevo arranca sin atender

    def assign(self, technician: str) -> None:
        # Asigna un técnico al ticket. OJO: acá recién se crea el atributo
        # self.technician -- antes de llamar a este método, el objeto NO lo tiene.
        self.technician = technician
        self.status = "Asignado"

    def close(self) -> None:
        # Cierra el ticket. No toca self.technician (queda con el último asignado).
        self.status = "Cerrado"

    def get_summary(self) -> str:
        # Arma un resumen en un solo string, leyendo los atributos actuales del
        # objeto. Los 4 f-strings van pegados sin comas entre ellos a propósito:
        # así Python los concatena en un solo str (si tuvieran coma, se armaría
        # una tupla de 4 strings en vez de un único resumen).
        return (
            f"{self.ticket_id} - "
            f"{self.title} - "
            f"{self.status} - "
            f"{self.technician}"
        )

# --- Proceso: crear un ticket, asignarlo y pedir su resumen ---

# 1) Se crea el objeto: corre __init__ y guarda ticket_id/title/priority/status.
#    self.technician todavía NO existe en este punto.
ticket_1 = Ticket(1001, "Error de impresión", "Alta")

# 2) Se llama a assign(): recién acá se crea self.technician = "Técnico Gustavo"
#    y self.status pasa de "pendiente" a "Asignado".
ticket_1.assign("Técnico Gustavo")

# 3) Se llama a get_summary(): ya puede leer self.technician porque el paso 2
#    corrió antes -- si se llamara ANTES del assign(), tiraría AttributeError.
#    print() muestra el string que devuelve.
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
<span class="terminal-shot__output">1001 - Error de impresión - Asignado - Técnico Gustavo</span></code></pre>
</div>

**Paso a paso, exactamente qué hace cada línea al ejecutarse** (el resumen de los
comentarios de arriba, en tabla):

| Paso | Línea | Qué pasa internamente |
|---|---|---|
| 1 | `ticket_1 = Ticket(1001, "Error de impresión", "Alta")` | Corre `__init__`: crea el objeto y le asigna 4 atributos (`ticket_id`, `title`, `priority`, `status="pendiente"`). **Todavía no existe** `self.technician` — no se le asignó ningún valor. |
| 2 | `ticket_1.assign("Técnico Gustavo")` | Corre `assign()`: **recién acá** se crea el atributo `self.technician = "Técnico Gustavo"` (en Python los atributos se crean al asignarlos, no hace falta declararlos antes) y cambia `self.status` de `"pendiente"` a `"Asignado"`. |
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

![Diagrama de clases del dominio de tickets con los 5 principios SOLID anclados a su relación real: Ticket sin responsabilidades de notificación (S), SMSNotification agregable sin tocar nada más (O), EmailNotification y SMSNotification intercambiables detrás del mismo contrato (L), NotificacionChannel con un único método (I), y TicketService dependiendo de la abstracción en vez de EmailNotification concreta (D)](/clase-02-principios-solid.svg)

> 📎 Versión interactiva en el
> [Artifact publicado](https://claude.ai/code/artifact/998c914c-00bb-43e4-b563-51eeec5be6ef) —
> fuente editable en `04-Recursos/diagramas/clase-02-principios-solid.html`.
> `SMSNotification` es hipotética (todavía no existe en `02-Ejercicios/Clase-02/`) —
> ilustra el ejemplo de la tabla ("agregar SMSNotification sin tocar las demás clases").

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
| [`02-Ejercicios/Clase-02/encapsulamiento.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-02/encapsulamiento.py) | Práctica de encapsulamiento: importa el `Ticket` de `objeto.py` y lee `ticket_1._status` directo (atributo "protegido"), para comprobar en carne propia que Python no lo bloquea de verdad. |
| [`02-Ejercicios/Clase-02/notification_channel.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-02/notification_channel.py) | Reto de POO resuelto: la abstracción `NotificacionChannel(ABC)` con `@abstractmethod send()`. |
| [`02-Ejercicios/Clase-02/emailnotification.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-02/emailnotification.py) | Implementación concreta 1: `EmailNotification` hereda de `NotificacionChannel` e implementa `send()`. |
| [`02-Ejercicios/Clase-02/whatsapp_notifiaction.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-02/whatsapp_notifiaction.py) | Implementación concreta 2: `WhatsAppNotification` hereda de `NotificacionChannel` e implementa `send()`. |
| [`02-Ejercicios/Clase-02/main.py`](https://github.com/stypcanto/curso-python-para-backend/blob/main/02-Ejercicios/Clase-02/main.py) | Punto de entrada: instancia `EmailNotification` y `WhatsAppNotification` y llama a `.send()` en cada una — la abstracción en acción. |

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

> ✅ **Resuelto — parte 2 (la abstracción de canales).** `02-Ejercicios/Clase-02/` ya
> tiene `notification_channel.py` + `emailnotification.py` + `whatsapp_notifiaction.py`
> + `main.py` funcionando (ver sección siguiente). La parte 1 (`Ticket` encapsulado) ya
> estaba resuelta desde antes en `objeto.py`/`encapsulamiento.py` (secciones 5 y 6). La
> parte 3 (`TicketService` que **compone** un canal, estructura `helpdesk/`) sigue
> pendiente — hoy `main.py` llama a `email.send(...)` directo, sin una clase de
> servicio intermedia.

### 🔔 `notification_channel.py` + `emailnotification.py` + `whatsapp_notifiaction.py` + `main.py` — la abstracción en 4 archivos
Es la resolución práctica de la **sección 7 (Abstracción)**, ahora repartida en
**módulos separados** en vez de un solo archivo — un paso real hacia la organización
por carpetas de la sección 11 (`notifications/base.py`, `notifications/email.py`, …).

![Diagrama de clases: NotificacionChannel (abstracta, con el método abstracto send) es implementada por EmailNotification y WhatsAppNotification, ambas usadas desde main.py mediante .send(); TicketService aparece punteado como composición pendiente](/clase-02-abstraccion-notificaciones.svg)

> 📎 Versión interactiva (zoom/pan) en el
> [Artifact publicado](https://claude.ai/code/artifact/258a2795-aee5-4d79-8202-5755cc9d9d73) —
> fuente editable en `04-Recursos/diagramas/clase-02-abstraccion-notificaciones.html`.

**1) `notification_channel.py` — el contrato (la abstracción):**
```python
from abc import ABC, abstractmethod

class NotificacionChannel(ABC):
    @abstractmethod
    def send(
        self,
        recipient: str,
        mensaje: str) -> None:
        pass
```
Define **qué** debe poder hacer cualquier canal (`send(recipient, mensaje)`) sin decir
**cómo** — igual que `NotificationChannel` en la teoría (sección 7). `ABC` +
`@abstractmethod` impiden instanciar `NotificacionChannel()` directo y obligan a toda
subclase a implementar `send()`, o Python no la deja instanciarse.

**2) `emailnotification.py` y `whatsapp_notifiaction.py` — dos implementaciones concretas:**
```python
from notification_channel import NotificacionChannel

class EmailNotification(NotificacionChannel):
    def send(self, recipient: str, message: str) -> None:
        print(f"Correo enviado a {recipient} con el mensaje: {message}")
```
```python
from notification_channel import NotificacionChannel

class WhatsAppNotification(NotificacionChannel):
    def send(self, recipient: str, message: str) -> None:
        print(f"Mensaje WhatsApp enviado a {recipient} con el mensaje: {message}")
```
Cada clase hereda de `NotificacionChannel` y **cumple el contrato** implementando
`send()` a su manera — un canal imprime "Correo enviado...", el otro "Mensaje WhatsApp
enviado...", pero ambos se usan exactamente igual desde afuera (mismo método, misma
firma). Es la respuesta concreta a la pregunta de la sección 7 (*¿qué hay que tocar
para agregar un canal nuevo?*): un archivo nuevo que herede de `NotificacionChannel` —
nada de lo demás se toca.

**3) `main.py` — el punto de entrada que las ejecuta:**
```python
from emailnotification import EmailNotification
from whatsapp_notifiaction import WhatsAppNotification

email = EmailNotification()
email.send("Juan", "Hola ")

whatsapp = WhatsAppNotification()
whatsapp.send("Pedro", "Hola ")
```

<div class="terminal-shot">
  <div class="terminal-shot__titlebar">
    <span class="terminal-shot__dot terminal-shot__dot--red"></span>
    <span class="terminal-shot__dot terminal-shot__dot--yellow"></span>
    <span class="terminal-shot__dot terminal-shot__dot--green"></span>
    <span class="terminal-shot__title">zsh · main.py</span>
  </div>
  <pre class="terminal-shot__screen"><code><span class="terminal-shot__prompt">$</span> python3 main.py
<span class="terminal-shot__output">Correo enviado a Juan con el mensaje: Hola
Mensaje WhatsApp enviado a Pedro con el mensaje: Hola </span></code></pre>
</div>

| Paso | Qué pasa |
|---|---|
| `email = EmailNotification()` | Crea un objeto concreto. Solo funciona porque `EmailNotification` **sí** implementó `send()` — si le faltara, Python tiraría `TypeError` al instanciar. |
| `email.send("Juan", "Hola ")` | Llama al método concreto de `EmailNotification`, que imprime el mensaje de correo. |
| `whatsapp = WhatsAppNotification()` / `.send(...)` | Mismo patrón, con la implementación de WhatsApp — **el mismo método `.send(...)`**, resultado distinto según la clase. |

> 📝 **Detalles a corregir (no rompen el ejercicio, pero vale la pena anotarlos):**
> - **Nombre en español vs. inglés:** la clase se llamó `NotificacionChannel` (sin la
>   segunda "i", en español) en vez de `NotificationChannel` como en la teoría de la
>   sección 7 — funciona igual, pero mezclar idiomas en nombres de clases no es
>   consistente; lo ideal es elegir uno solo para todo el proyecto.
> - **Nombre de archivo con typo:** `whatsapp_notifiaction.py` (falta la "c" antes de
>   "tion" → sería `whatsapp_notification.py`). No afecta la ejecución (Python importa
>   igual), pero conviene corregirlo antes de que otros archivos lo importen y el typo
>   se propague.
> - **Parámetro `mensaje` vs. `message`:** el método abstracto en
>   `notification_channel.py` declara `def send(self, recipient: str, mensaje: str)`,
>   pero **ambas** implementaciones concretas usan `message` (inglés). No rompe nada
>   porque `main.py` pasa los argumentos **posicionales** (`email.send("Juan", "Hola ")`,
>   sin nombrar el parámetro) — pero si alguna vez se llamara con keyword argument
>   (`email.send(recipient="Juan", mensaje="Hola")`), fallaría con
>   `TypeError: send() got an unexpected keyword argument 'mensaje'` porque la clase
>   concreta espera `message`, no `mensaje`. Python **no exige** que el nombre del
>   parámetro coincida entre la clase abstracta y sus implementaciones (solo el
>   *contrato* de que el método exista), pero mantener el mismo nombre evita esta
>   trampa.
> - **Todavía sin `TicketService` ni excepciones:** este archivo resuelve la
>   *abstracción* (parte 2 del reto) pero no la *composición* — no hay una clase
>   `TicketService(notification: NotificacionChannel)` que reciba el canal como
>   dependencia (sección 9) ni manejo de errores. Es el siguiente paso natural para
>   completar el reto.

### 🔒 `encapsulamiento.py` — practicando el `_status` de `objeto.py`
Archivo aparte, **no relacionado** con la abstracción de arriba — reutiliza el
`Ticket` de `objeto.py` (sección 5) y el `Perro` de `perro.py` (sección 4) para
comprobar en la práctica el punto de la sección 6: `_status` es una convención, no una
protección real.

```python
from objeto import Ticket
from perro import Perro

ticket_1 = Ticket(1001, "Error de impresión", "Alta")
ticket_1.assign("Técnico Gustavo")
print(ticket_1.get_summary())

print(ticket_1._status)  # imprime "Asignado" porque el ticket fue asignado
```

<div class="terminal-shot">
  <div class="terminal-shot__titlebar">
    <span class="terminal-shot__dot terminal-shot__dot--red"></span>
    <span class="terminal-shot__dot terminal-shot__dot--yellow"></span>
    <span class="terminal-shot__dot terminal-shot__dot--green"></span>
    <span class="terminal-shot__title">zsh · encapsulamiento.py</span>
  </div>
  <pre class="terminal-shot__screen"><code><span class="terminal-shot__prompt">$</span> python3 encapsulamiento.py
<span class="terminal-shot__output">1001 - Error de impresión - Asignado - Técnico Gustavo
15.5 2.2 Golden
1001 - Error de impresión - Asignado - Técnico Gustavo
Asignado</span></code></pre>
</div>

> ⚠️ **Por qué salen 4 líneas y no 2:** ni `objeto.py` ni `perro.py` protegen su código
> de ejecución con `if __name__ == "__main__":` — así que al hacer
> `from objeto import Ticket`, Python **también ejecuta** el código suelto que ya
> tiene `objeto.py` al final (su propio `ticket_1` de prueba + `print(...)`), y lo
> mismo con `from perro import Perro`. Por eso las líneas 1 y 2 salen "gratis" solo por
> importar, **antes** de que corra ninguna línea propia de `encapsulamiento.py` — recién
> las líneas 3 y 4 son las que este archivo escribió. Se deja documentado porque es un
> efecto secundario real de reutilizar módulos que no separan "definición" de
> "ejecución", el mismo tipo de problema que resuelve la organización en carpetas de
> la sección 11.
>
> 📝 **`objeto.py` cambió desde la última vez que se documentó:** ahora guarda el
> estado en `self._status` (protegido, sección 6) en vez de `self.status`, que es
> justo lo que permite este ejercicio. Pero además le quedó un bloque muerto al final
> del archivo — un `@property def status(self): return self._status` escrito **fuera**
> de la clase `Ticket` (sin la indentación de método), que Python acepta como una
> función suelta sin dueño, nunca se llama y no cumple su propósito de exponer
> `ticket.status` de solo lectura. No rompe nada porque nadie lo invoca, pero conviene
> volver a indentarlo dentro de la clase para que la `@property` funcione de verdad.

# 🏋️ EJERCICIOS CON SOLUCIÓN

> 📌 24 ejercicios que repasan **toda la teoría de esta clase** (secciones 2 a 12), de lo más
> básico (una clase con un método) a lo más completo (encapsulamiento + abstracción + composición
> en un solo objeto). Cada uno tiene un desplegable **"💡 ¿Sabías que…?"** con el repaso del
> concepto + un ejemplo ya verificado de la teoría de esta misma clase, y un desplegable
> **"Ver solución"** — todo el código fue corrido en terminal antes de documentarlo. Abstracción
> (8-11), herencia (12-15) y polimorfismo (16-19) tienen 4 ejercicios cada uno, de lo más básico a
> lo más específico del concepto. Los ejercicios 1-20 son de un solo concepto; del 21 en adelante
> combinan varios (SOLID, patrones), hasta el integrador final (24).

### Ejercicio 1 — Clase simple con atributos + un método
Crea la clase `Producto` con `nombre` y `precio`, y un método `aplicar_descuento(porcentaje)` que **devuelva** (no modifique) el precio con el descuento aplicado. Crea un producto, guarda el resultado en `precio_final` y muestra `precio_final` y `producto.precio` — comprobá que el original no cambió.

<details><summary>💡 ¿Sabías que…? — la clase como plantilla, sección 4</summary>

Una clase define qué datos y qué operaciones tendrá cada objeto; un método que **devuelve** un valor con `return` no modifica el objeto, solo calcula algo a partir de sus atributos.

```python
class Ticket:
    def __init__(self, ticket_id: int, title: str, priority: str):
        self.ticket_id = ticket_id
        self.title = title
        self.priority = priority
        self.status = "Pendiente"


ticket_1 = Ticket(
    1001, "Error al iniciar sesión", "Alta"
)
print(ticket_1.priority)
```
```
Alta
```
</details>

<details><summary>Ver solución</summary>

```python
class Producto:
    def __init__(self, nombre: str, precio: float):
        self.nombre = nombre
        self.precio = precio

    def aplicar_descuento(self, porcentaje: float) -> float:
        return self.precio * (1 - porcentaje / 100)

producto = Producto("Teclado mecánico", 50000)
precio_final = producto.aplicar_descuento(20)
print(precio_final)
print(producto.precio)
```
```
40000.0
50000
```
</details>

### Ejercicio 2 — Varios objetos, mismo molde, distinto estado
Crea la clase `Empleado` con `nombre` y `salario`. Crea 3 empleados con salarios distintos y mostrá la **suma** de los 3 salarios (accediendo a cada objeto por su nombre de variable, sin lista todavía).

<details><summary>💡 ¿Sabías que…? — la clase como plantilla — varios objetos, sección 4</summary>

Dos objetos creados a partir de la misma clase son objetos **distintos** en memoria, aunque compartan la misma "forma" — cada uno guarda sus propios valores.

```python
class Perro:
    def __init__(self, peso: float, talla: float, familia: str):
        self.peso = peso
        self.talla = talla
        self.familia = familia


perro_golden = Perro(15.5, 2.20, "Golden")
perro_salchicha = Perro(2.2, 1.2, "Salchicha")

print(perro_golden.peso, perro_salchicha.peso)
```
```
15.5 2.2
```
</details>

<details><summary>Ver solución</summary>

```python
class Empleado:
    def __init__(self, nombre: str, salario: float):
        self.nombre = nombre
        self.salario = salario

empleado_ana = Empleado("Ana", 3000)
empleado_luis = Empleado("Luis", 2500)
empleado_sofia = Empleado("Sofía", 3200)

total = empleado_ana.salario + empleado_luis.salario + empleado_sofia.salario
print(total)
```
```
8700
```
</details>

### Ejercicio 3 — Método que modifica el estado (`self.attr = ...`)
Crea la clase `Termostato` con `temperatura` inicial en `20` y un método `subir(grados)` que **modifique** `self.temperatura` sumándole `grados`. Llamalo dos veces y mostrá la temperatura final.

<details><summary>💡 ¿Sabías que…? — estado y comportamiento — métodos que mutan `self`, sección 5</summary>

A diferencia de un método que hace `return`, un método puede **cambiar directamente** el estado del objeto asignando sobre `self.atributo` — el cambio queda guardado en el objeto para las próximas llamadas.

```python
class Ticket:
    def assign(self, technician: str) -> None:
        self.technician = technician
        self.status = "Asignado"

t = Ticket()
t.assign("Técnico Gustavo")
print(t.status)
```
```
Asignado
```
</details>

<details><summary>Ver solución</summary>

```python
class Termostato:
    def __init__(self):
        self.temperatura = 20

    def subir(self, grados: int) -> None:
        self.temperatura += grados

t = Termostato()
t.subir(3)
t.subir(2)
print(t.temperatura)
```
```
25
```
</details>

### Ejercicio 4 — Método que calcula y devuelve (`return`)
Crea la clase `Rectangulo` con `base` y `altura`, y un método `area()` que **devuelva** el área (no la imprima). Guardá el resultado en una variable, mostralo, y mostrá también `r.area() * 2` para comprobar que podés reutilizar el valor devuelto en otra expresión.

<details><summary>💡 ¿Sabías que…? — estado y comportamiento — `return` para reutilizar el resultado, sección 5</summary>

`return` entrega el valor a quien llamó al método, para que se pueda **reutilizar** después (guardarlo, operarlo, pasarlo a otra función) — a diferencia de `print()`, que solo lo muestra y lo pierde.

```python
class Ticket:
    def get_summary(self) -> str:
        return f"{self.ticket_id} - {self.status}"

t = Ticket()
t.ticket_id, t.status = 1001, "Asignado"
resumen = t.get_summary()
print(resumen)
```
```
1001 - Asignado
```
</details>

<details><summary>Ver solución</summary>

```python
class Rectangulo:
    def __init__(self, base: float, altura: float):
        self.base = base
        self.altura = altura

    def area(self) -> float:
        return self.base * self.altura

r = Rectangulo(4, 5)
resultado = r.area()
print(resultado)
print(r.area() * 2)
```
```
20
40
```
</details>

### Ejercicio 5 — Función suelta vs. método: mismo cálculo, dos formas
Escribí el mismo cálculo del IVA (18%) de dos formas: una función suelta `calcular_iva_funcion(precio)` que recibe el precio como parámetro, y un método `Producto.calcular_iva()` que usa `self.precio`. Comprobá que ambas dan el mismo resultado con `==`.

<details><summary>💡 ¿Sabías que…? — el puente entre función y método, sección 2</summary>

Una función suelta necesita que **le pasen el dato explícitamente** en cada llamada; un método ya tiene el dato guardado en `self`, así que no hace falta pasarlo — es la misma idea que abre el salto de funciones a POO en esta clase.

```python
def agregar_tarea(lista, tarea):
    lista.append(tarea)

tareas = []
agregar_tarea(tareas, "Programar en Python")
print(tareas)
```
```
['Programar en Python']
```
</details>

<details><summary>Ver solución</summary>

```python
def calcular_iva_funcion(precio: float) -> float:
    return precio * 0.18

class Producto:
    def __init__(self, precio: float):
        self.precio = precio

    def calcular_iva(self) -> float:
        return self.precio * 0.18

precio = 100
iva_funcion = calcular_iva_funcion(precio)

producto = Producto(100)
iva_metodo = producto.calcular_iva()

print(iva_funcion, iva_metodo)
print(iva_funcion == iva_metodo)
```
```
18.0 18.0
True
```
</details>

### Ejercicio 6 — Encapsulamiento: `_atributo` protegido + `@property`
Crea `CuentaBancaria` con `_saldo` protegido (inicia en `0`), una `@property saldo` de solo lectura, y un método `depositar(monto)` que sume al saldo — pero que lance `ValueError` si `monto <= 0`. Probá un depósito válido y capturá el error de uno inválido con `try`/`except`.

<details><summary>💡 ¿Sabías que…? — encapsulamiento — validar antes de cambiar el estado, sección 6</summary>

El guion bajo (`_saldo`) es la convención "no lo toques directo"; la `@property` expone el valor de **solo lectura**, y el método (`depositar`) es el único lugar autorizado para cambiarlo — centralizando ahí la validación.

```python
class Ticket:
    def close(self) -> None:
        if self._status == "Cerrado":
            raise ValueError("Ya está cerrada")
        self._status = "Cerrado"

t = Ticket()
t._status = "Pendiente"
t.close()
print(t._status)
```
```
Cerrado
```
</details>

<details><summary>Ver solución</summary>

```python
class CuentaBancaria:
    def __init__(self):
        self._saldo = 0

    @property
    def saldo(self) -> float:
        return self._saldo

    def depositar(self, monto: float) -> None:
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        self._saldo += monto

cuenta = CuentaBancaria()
cuenta.depositar(100)
print(cuenta.saldo)

try:
    cuenta.depositar(-50)
except ValueError as e:
    print(f"Error: {e}")
```
```
100
Error: El monto debe ser positivo
```
</details>

### Ejercicio 7 — Encapsulamiento: transición de estado controlada
Crea `Pedido` con `_estado` protegido (inicia en `"creado"`) y un método `confirmar()` que solo permita pasar de `"creado"` a `"confirmado"` — si ya está confirmado, debe lanzar `ValueError`. Confirmalo una vez, mostrá el estado, y probá confirmarlo de nuevo capturando el error.

<details><summary>💡 ¿Sabías que…? — encapsulamiento — transiciones de estado imposibles de romper, sección 6</summary>

Centralizar la regla de negocio ("no se puede confirmar dos veces") en el método evita que cualquier parte del programa deje el objeto en un estado inválido — el mismo principio que `Ticket.close()` en la teoría.

```python
t = None
try:
    if True:
        raise ValueError("Ya está cerrada")
except ValueError as e:
    print(f"Error: {e}")
```
```
Error: Ya está cerrada
```
</details>

<details><summary>Ver solución</summary>

```python
class Pedido:
    def __init__(self):
        self._estado = "creado"

    @property
    def estado(self) -> str:
        return self._estado

    def confirmar(self) -> None:
        if self._estado == "confirmado":
            raise ValueError("El pedido ya está confirmado")
        self._estado = "confirmado"

pedido = Pedido()
pedido.confirmar()
print(pedido.estado)

try:
    pedido.confirmar()
except ValueError as e:
    print(f"Error: {e}")
```
```
confirmado
Error: El pedido ya está confirmado
```
</details>

### Ejercicio 8 — Abstracción: `ABC` + dos implementaciones
Crea la clase abstracta `MetodoPago(ABC)` con `@abstractmethod procesar(monto)`. Implementá `PagoTarjeta` y `PagoEfectivo`. Probá ambas con el mismo monto, y confirmá con `try`/`except TypeError` que `MetodoPago()` no se puede instanciar directo.

<details><summary>💡 ¿Sabías que…? — abstracción — contrato sin implementación, sección 7</summary>

`ABC` + `@abstractmethod` definen **qué** operación debe existir (`procesar`) sin decir cómo — Python bloquea instanciar la clase abstracta directo, y obliga a cada subclase a implementar el método o tampoco se puede instanciar.

```python
from abc import ABC, abstractmethod

class NotificationChannel(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> None:
        pass

try:
    NotificationChannel()
except TypeError as e:
    print(f"Error: {e}")
```
```
Error: Can't instantiate abstract class NotificationChannel without an implementation for abstract method 'send'
```
</details>

<details><summary>Ver solución</summary>

```python
from abc import ABC, abstractmethod

class MetodoPago(ABC):
    @abstractmethod
    def procesar(self, monto: float) -> None:
        pass

class PagoTarjeta(MetodoPago):
    def procesar(self, monto: float) -> None:
        print(f"Cobrando {monto} con tarjeta")

class PagoEfectivo(MetodoPago):
    def procesar(self, monto: float) -> None:
        print(f"Cobrando {monto} en efectivo")

tarjeta = PagoTarjeta()
tarjeta.procesar(150)

efectivo = PagoEfectivo()
efectivo.procesar(150)

try:
    MetodoPago()
except TypeError as e:
    print(f"Error: {e}")
```
```
Cobrando 150 con tarjeta
Cobrando 150 en efectivo
Error: Can't instantiate abstract class MetodoPago without an implementation for abstract method 'procesar'
```
</details>

### Ejercicio 9 — Abstracción: varios métodos abstractos, todos obligatorios
Crea `Figura(ABC)` con **dos** métodos abstractos: `area()` y `perimetro()`. Implementá `Circulo` con ambos. Después, probá crear una clase que implemente **solo uno** de los dos (dejando el otro sin implementar) y capturá con `try`/`except TypeError` que Python igual bloquea la instanciación.

<details><summary>💡 ¿Sabías que…? — abstracción — ABC exige TODOS los métodos abstractos, no alguno, sección 7</summary>

Cuando una clase abstracta declara varios `@abstractmethod`, una subclase que implemente solo algunos **sigue siendo abstracta** — Python no deja instanciarla hasta que estén los que faltan.

```python
from abc import ABC, abstractmethod

class Instrumento(ABC):
    @abstractmethod
    def afinar(self) -> None:
        pass

    @abstractmethod
    def tocar(self) -> None:
        pass

class Guitarra(Instrumento):
    def afinar(self) -> None:
        print("Afinando cuerdas")

    def tocar(self) -> None:
        print("Rasgueando")

Guitarra().tocar()
```
```
Rasgueando
```
</details>

<details><summary>Ver solución</summary>

```python
from abc import ABC, abstractmethod

class Figura(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def perimetro(self) -> float:
        pass

class Circulo(Figura):
    def __init__(self, radio: float):
        self.radio = radio

    def area(self) -> float:
        return 3.1416 * self.radio ** 2

    def perimetro(self) -> float:
        return 2 * 3.1416 * self.radio

circulo = Circulo(3)
print(circulo.area())
print(circulo.perimetro())

class CirculoIncompleto(Figura):
    def __init__(self, radio: float):
        self.radio = radio

    def area(self) -> float:
        return 3.1416 * self.radio ** 2
    # falta implementar perimetro()

try:
    CirculoIncompleto(3)
except TypeError as e:
    print(f"Error: {e}")
```
```
28.2744
18.8496
Error: Can't instantiate abstract class CirculoIncompleto without an implementation for abstract method 'perimetro'
```
</details>

### Ejercicio 10 — Abstracción: método concreto + método abstracto en la misma ABC
Crea `Reporte(ABC)` con un método **ya implementado** `imprimir_encabezado()` (concreto, no abstracto) y un método `generar_cuerpo()` **abstracto**. Implementá `ReporteVentas`, que solo define `generar_cuerpo()` pero hereda `imprimir_encabezado()` sin tocarlo.

<details><summary>💡 ¿Sabías que…? — abstracción — una ABC puede tener comportamiento ya resuelto, sección 7</summary>

`ABC` no obliga a que **todos** los métodos sean abstractos — puede combinar métodos concretos (compartidos tal cual por todas las subclases) con métodos abstractos (que cada subclase debe completar a su manera).

```python
from abc import ABC, abstractmethod

class Documento(ABC):
    def guardar(self) -> None:
        print("Guardado en disco")

    @abstractmethod
    def render(self) -> str:
        pass

class DocumentoPDF(Documento):
    def render(self) -> str:
        return "contenido en PDF"

doc = DocumentoPDF()
doc.guardar()
print(doc.render())
```
```
Guardado en disco
contenido en PDF
```
</details>

<details><summary>Ver solución</summary>

```python
from abc import ABC, abstractmethod

class Reporte(ABC):
    def imprimir_encabezado(self) -> None:
        print("=== Reporte ===")

    @abstractmethod
    def generar_cuerpo(self) -> str:
        pass

class ReporteVentas(Reporte):
    def __init__(self, total: float):
        self.total = total

    def generar_cuerpo(self) -> str:
        return f"Ventas totales: {self.total}"

reporte = ReporteVentas(15000)
reporte.imprimir_encabezado()
print(reporte.generar_cuerpo())
```
```
=== Reporte ===
Ventas totales: 15000
```
</details>

### Ejercicio 11 — Abstracción: ABC con `__init__` real y estado compartido
Crea `Empleado(ABC)` con `__init__(self, nombre)` que guarda `self.nombre`, y un método abstracto `calcular_sueldo()`. Implementá `Vendedor` (sueldo base + comisión) y `Gerente` (sueldo base + bono), ambos reutilizando `__init__` vía `super().__init__(nombre)`. Recorré una lista de ambos con un `for` mostrando nombre y sueldo.

<details><summary>💡 ¿Sabías que…? — abstracción — una ABC también puede tener estado, no solo contratos vacíos, sección 7</summary>

Una clase abstracta puede tener un `__init__` real con atributos — la parte "abstracta" es solo el método sin implementar; el resto (constructor, atributos, métodos concretos) funciona como en cualquier clase normal y se hereda igual.

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    def __init__(self, nombre: str):
        self.nombre = nombre

    @abstractmethod
    def hacer_sonido(self) -> str:
        pass

class Gato(Animal):
    def hacer_sonido(self) -> str:
        return "Miau"

gato = Gato("Michi")
print(gato.nombre, gato.hacer_sonido())
```
```
Michi Miau
```
</details>

<details><summary>Ver solución</summary>

```python
from abc import ABC, abstractmethod

class Empleado(ABC):
    def __init__(self, nombre: str):
        self.nombre = nombre

    @abstractmethod
    def calcular_sueldo(self) -> float:
        pass

class Vendedor(Empleado):
    def __init__(self, nombre: str, comision: float):
        super().__init__(nombre)
        self.comision = comision

    def calcular_sueldo(self) -> float:
        return 1000 + self.comision

class Gerente(Empleado):
    def __init__(self, nombre: str, bono: float):
        super().__init__(nombre)
        self.bono = bono

    def calcular_sueldo(self) -> float:
        return 3000 + self.bono

empleados = [Vendedor("Ana", 500), Gerente("Luis", 800)]
for empleado in empleados:
    print(empleado.nombre, empleado.calcular_sueldo())
```
```
Ana 1500
Luis 3800
```
</details>

### Ejercicio 12 — Herencia: subclase + `super().__init__`
Crea `Vehiculo` (marca, modelo) con un método `descripcion()`. Crea `Auto(Vehiculo)` que agrega `puertas` y reutiliza el constructor del padre con `super().__init__(...)`. Mostrá la descripción heredada, `puertas`, y confirmá con `isinstance(auto, Vehiculo)` que un `Auto` **es un** `Vehiculo`.

<details><summary>💡 ¿Sabías que…? — herencia — reutilizar el constructor del padre, sección 8</summary>

`super().__init__(...)` llama al constructor de la clase padre en vez de repetir sus asignaciones a mano — la subclase hereda automáticamente sus atributos y métodos, y agrega los propios.

```python
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

class Technician(User):
    def __init__(self, name: str, email: str, specialty: str):
        super().__init__(name, email)
        self.specialty = specialty

tech = Technician("Gustavo", "g@mail.com", "Redes")
print(tech.name, tech.specialty)
print(isinstance(tech, User))
```
```
Gustavo Redes
True
```
</details>

<details><summary>Ver solución</summary>

```python
class Vehiculo:
    def __init__(self, marca: str, modelo: str):
        self.marca = marca
        self.modelo = modelo

    def descripcion(self) -> str:
        return f"{self.marca} {self.modelo}"

class Auto(Vehiculo):
    def __init__(self, marca: str, modelo: str, puertas: int):
        super().__init__(marca, modelo)
        self.puertas = puertas

auto = Auto("Toyota", "Corolla", 4)
print(auto.descripcion())
print(auto.puertas)
print(isinstance(auto, Vehiculo))
```
```
Toyota Corolla
4
True
```
</details>

### Ejercicio 13 — Herencia: sobrescribir un método y extenderlo con `super()`
Crea `Empleado` con `calcular_bono()` que devuelve `0`. Crea `Vendedor(Empleado)` que **sobrescribe** `calcular_bono()`, pero en vez de reemplazarlo del todo, llama a `super().calcular_bono()` y le suma un 10% del salario. Comprobá que un `Empleado` normal sigue dando `0` y un `Vendedor` da un valor distinto.

<details><summary>💡 ¿Sabías que…? — herencia — sobrescribir (override) sin perder lo del padre, sección 8</summary>

Sobrescribir un método no significa borrar el del padre — `super().metodo()` dentro del override permite **extender** el comportamiento heredado en vez de reemplazarlo por completo.

```python
class Forma:
    def describir(self) -> str:
        return "Forma genérica"

class Triangulo(Forma):
    def describir(self) -> str:
        base = super().describir()
        return f"{base} — con 3 lados"

print(Triangulo().describir())
```
```
Forma genérica — con 3 lados
```
</details>

<details><summary>Ver solución</summary>

```python
class Empleado:
    def __init__(self, nombre: str, salario: float):
        self.nombre = nombre
        self.salario = salario

    def calcular_bono(self) -> float:
        return 0

class Vendedor(Empleado):
    def calcular_bono(self) -> float:
        bono_base = super().calcular_bono()
        return bono_base + self.salario * 0.10

empleado = Empleado("Ana", 2000)
vendedor = Vendedor("Luis", 2000)
print(empleado.calcular_bono())
print(vendedor.calcular_bono())
```
```
0
200.0
```
</details>

### Ejercicio 14 — Herencia multinivel: abuelo → padre → nieto
Crea `Ser` (nombre) → `Animal(Ser)` (agrega especie) → `Perro(Animal)` (agrega raza, fija `especie="Canino"` automáticamente). Creá un `Perro`, mostrá sus 3 atributos, y confirmá con `isinstance` que **es** tanto `Ser` como `Animal`.

<details><summary>💡 ¿Sabías que…? — herencia — la cadena se hereda completa, no solo un nivel, sección 8</summary>

La herencia no se detiene en el padre directo: un objeto de la clase más específica **es** instancia de **todos** los niveles de la cadena hacia arriba, no solo de su padre inmediato.

```python
class A:
    def saludo(self) -> str:
        return "Hola desde A"

class B(A):
    pass

class C(B):
    pass

c = C()
print(c.saludo())
print(isinstance(c, A))
```
```
Hola desde A
True
```
</details>

<details><summary>Ver solución</summary>

```python
class Ser:
    def __init__(self, nombre: str):
        self.nombre = nombre

class Animal(Ser):
    def __init__(self, nombre: str, especie: str):
        super().__init__(nombre)
        self.especie = especie

class Perro(Animal):
    def __init__(self, nombre: str, raza: str):
        super().__init__(nombre, especie="Canino")
        self.raza = raza

firulais = Perro("Firulais", "Labrador")
print(firulais.nombre, firulais.especie, firulais.raza)
print(isinstance(firulais, Ser), isinstance(firulais, Animal))
```
```
Firulais Canino Labrador
True True
```
</details>

### Ejercicio 15 — Herencia múltiple (mixins): combinar dos clases base
Crea `Loggable` (con `log(mensaje)`) y `Serializable` (con `to_dict()` que devuelve `self.__dict__`) como clases independientes, sin relación entre ellas. Crea `Pedido(Loggable, Serializable)` con sus propios atributos, y comprobá que puede usar los métodos de **ambas**.

<details><summary>💡 ¿Sabías que…? — herencia múltiple — combinar comportamientos con mixins, sección 8</summary>

Python permite heredar de **más de una** clase a la vez (`class Hija(A, B)`) — cada clase base aporta un comportamiento independiente ("mixin"), y la subclase termina con los métodos de todas.

```python
class Volador:
    def volar(self) -> str:
        return "Vuelo"

class Nadador:
    def nadar(self) -> str:
        return "Nado"

class Pato(Volador, Nadador):
    pass

pato = Pato()
print(pato.volar(), pato.nadar())
```
```
Vuelo Nado
```
</details>

<details><summary>Ver solución</summary>

```python
class Loggable:
    def log(self, mensaje: str) -> None:
        print(f"[LOG] {mensaje}")

class Serializable:
    def to_dict(self) -> dict:
        return self.__dict__

class Pedido(Loggable, Serializable):
    def __init__(self, pedido_id: int, total: float):
        self.pedido_id = pedido_id
        self.total = total

pedido = Pedido(1001, 250)
pedido.log("Pedido creado")
print(pedido.to_dict())
```
```
[LOG] Pedido creado
{'pedido_id': 1001, 'total': 250}
```
</details>

### Ejercicio 16 — Polimorfismo: misma llamada, comportamiento distinto
Reusando `MetodoPago`/`PagoTarjeta`/`PagoEfectivo` del ejercicio 8, escribí una función `cobrar(metodo: MetodoPago, monto)` que llame a `metodo.procesar(monto)` sin saber de qué subclase se trata. Probala recorriendo con un `for` una lista `[PagoTarjeta(), PagoEfectivo()]`.

<details><summary>💡 ¿Sabías que…? — polimorfismo — programar contra el contrato, no contra la clase concreta, sección 8</summary>

`cobrar()` no pregunta "¿sos tarjeta o efectivo?" — solo confía en que cualquier `MetodoPago` sabe `procesar()`. Es la misma idea que `TicketService` (sección 9), que usa un `NotificationChannel` sin importarle cuál sea.

```python
def notificar(canal, recipient, message):
    canal.send(recipient, message)

class EmailNotification:
    def send(self, r, m): print(f"Correo enviado a {r}: {m}")

notificar(EmailNotification(), "Juan", "Hola")
```
```
Correo enviado a Juan: Hola
```
</details>

<details><summary>Ver solución</summary>

```python
from abc import ABC, abstractmethod

class MetodoPago(ABC):
    @abstractmethod
    def procesar(self, monto: float) -> None:
        pass

class PagoTarjeta(MetodoPago):
    def procesar(self, monto: float) -> None:
        print(f"Tarjeta: {monto}")

class PagoEfectivo(MetodoPago):
    def procesar(self, monto: float) -> None:
        print(f"Efectivo: {monto}")

def cobrar(metodo: MetodoPago, monto: float) -> None:
    metodo.procesar(monto)

metodos = [PagoTarjeta(), PagoEfectivo()]
for metodo in metodos:
    cobrar(metodo, 200)
```
```
Tarjeta: 200
Efectivo: 200
```
</details>

### Ejercicio 17 — Polimorfismo: duck typing sin una clase base en común
Crea `Perro` y `Pato`, **sin ninguna relación de herencia entre ellas** (ni ABC en común), ambas con un método `hablar()`. Escribí `hacer_hablar(animal)` que llame a `animal.hablar()` y probala con un objeto de cada clase en un `for`.

<details><summary>💡 ¿Sabías que…? — polimorfismo — duck typing: "si camina como pato y grazna como pato...", sección 8</summary>

El polimorfismo de esta clase (secciones 7-8) se apoya en heredar de una base común — pero Python no lo exige: si dos clases **no relacionadas** tienen el mismo método, una función puede tratarlas igual sin que compartan ninguna clase padre. Se llama *duck typing*.

```python
class Perro:
    def hablar(self) -> str:
        return "Guau"

class Pato:
    def hablar(self) -> str:
        return "Cuac"

def hacer_hablar(animal) -> None:
    print(animal.hablar())

for animal in [Perro(), Pato()]:
    hacer_hablar(animal)
```
```
Guau
Cuac
```
</details>

<details><summary>Ver solución</summary>

```python
class NotificadorInterno:
    def enviar(self, mensaje: str) -> None:
        print(f"Interno (Slack): {mensaje}")

class NotificadorExterno:
    def enviar(self, mensaje: str) -> None:
        print(f"Externo (Email): {mensaje}")

def avisar(notificador, mensaje: str) -> None:
    notificador.enviar(mensaje)

for notificador in [NotificadorInterno(), NotificadorExterno()]:
    avisar(notificador, "Turno confirmado")
```
```
Interno (Slack): Turno confirmado
Externo (Email): Turno confirmado
```
</details>

### Ejercicio 18 — Polimorfismo: mismo contrato, comportamiento distinto por figura
Crea `Figura(ABC)` con `descripcion()` abstracto. Implementá `Circulo` y `Cuadrado`, cada una devolviendo un string distinto. Recorré `[Circulo(), Cuadrado()]` con un `for` llamando `figura.descripcion()` en cada una.

<details><summary>💡 ¿Sabías que…? — polimorfismo — mismo método, resultado distinto según la clase real, sección 8</summary>

El `for` no sabe (ni le importa) si cada `figura` es un `Circulo` o un `Cuadrado` — solo llama `descripcion()` y cada objeto responde según **su propia** implementación.

```python
from abc import ABC, abstractmethod

class Idioma(ABC):
    @abstractmethod
    def saludar(self) -> str:
        pass

class Espanol(Idioma):
    def saludar(self) -> str:
        return "Hola"

class Ingles(Idioma):
    def saludar(self) -> str:
        return "Hello"

for idioma in [Espanol(), Ingles()]:
    print(idioma.saludar())
```
```
Hola
Hello
```
</details>

<details><summary>Ver solución</summary>

```python
from abc import ABC, abstractmethod

class Figura(ABC):
    @abstractmethod
    def descripcion(self) -> str:
        pass

class Circulo(Figura):
    def descripcion(self) -> str:
        return "Soy un círculo"

class Cuadrado(Figura):
    def descripcion(self) -> str:
        return "Soy un cuadrado"

figuras = [Circulo(), Cuadrado()]
for figura in figuras:
    print(figura.descripcion())
```
```
Soy un círculo
Soy un cuadrado
```
</details>

### Ejercicio 19 — Polimorfismo: `isinstance` dentro de una función polimórfica
Escribí `cobrar_con_descuento(metodo: MetodoPago, monto)` que llame a `metodo.procesar(monto)` polimórficamente, pero aplique un 5% de descuento **solo si** `metodo` es `PagoEfectivo` (usando `isinstance` para ese caso puntual). Probala con `PagoTarjeta` y con `PagoEfectivo`.

<details><summary>💡 ¿Sabías que…? — polimorfismo — cuándo SÍ conviene usar `isinstance` dentro de código polimórfico, sección 8</summary>

El ideal es no preguntar nunca "¿de qué clase sos?" — pero en casos reales, una regla de negocio puntual ("descuento solo en efectivo") a veces sí necesita un `isinstance` acotado, sin que eso rompa el resto del diseño polimórfico.

```python
class Paquete:
    def calcular_envio(self) -> float:
        return 10

class PaqueteFragil(Paquete):
    def calcular_envio(self) -> float:
        return 10

def cotizar(paquete: Paquete) -> float:
    costo = paquete.calcular_envio()
    if isinstance(paquete, PaqueteFragil):
        costo += 5  # seguro extra solo para frágiles
    return costo

print(cotizar(Paquete()))
print(cotizar(PaqueteFragil()))
```
```
10
15
```
</details>

<details><summary>Ver solución</summary>

```python
from abc import ABC, abstractmethod

class MetodoPago(ABC):
    @abstractmethod
    def procesar(self, monto: float) -> float:
        pass

class PagoTarjeta(MetodoPago):
    def procesar(self, monto: float) -> float:
        return monto

class PagoEfectivo(MetodoPago):
    def procesar(self, monto: float) -> float:
        return monto

def cobrar_con_descuento(metodo: MetodoPago, monto: float) -> float:
    total = metodo.procesar(monto)
    if isinstance(metodo, PagoEfectivo):
        total *= 0.95  # 5% de descuento solo en efectivo
    return total

print(cobrar_con_descuento(PagoTarjeta(), 100))
print(cobrar_con_descuento(PagoEfectivo(), 100))
```
```
100
95.0
```
</details>

### Ejercicio 20 — Composición: "tiene un" con inyección por constructor
Crea `Motor` con un método `arrancar()`. Crea `Auto` que **recibe** un `Motor` por constructor (composición, no herencia) y un método `encender()` que delega en `self.motor.arrancar()`.

<details><summary>💡 ¿Sabías que…? — composición — un objeto usa a otro para funcionar, sección 9</summary>

La composición modela "tiene un": `Auto` no *es* un `Motor`, lo *usa*. El objeto se recibe ya armado por constructor — el mismo patrón que `TicketService(notification)` de la teoría.

```python
class TicketService:
    def __init__(self, notification):
        self.notification = notification

    def register(self, ticket_id, email):
        self.notification.send(email, f"Solicitud {ticket_id} registrada")

class EmailNotification:
    def send(self, r, m): print(f"Correo enviado a {r}: {m}")

service = TicketService(EmailNotification())
service.register(1001, "juan@mail.com")
```
```
Correo enviado a juan@mail.com: Solicitud 1001 registrada
```
</details>

<details><summary>Ver solución</summary>

```python
class Motor:
    def arrancar(self) -> None:
        print("Motor arrancando...")

class Auto:
    def __init__(self, motor: Motor):
        self.motor = motor

    def encender(self) -> None:
        print("Encendiendo el auto")
        self.motor.arrancar()

auto = Auto(Motor())
auto.encender()
```
```
Encendiendo el auto
Motor arrancando...
```
</details>

### Ejercicio 21 — SOLID (S): separar una clase con dos responsabilidades
Refactorizá: en vez de que `Factura` tenga `calcular_total()` **y** `guardar_en_archivo()` (dos motivos de cambio en una sola clase), separá en `Factura` (solo calcula) y `FacturaRepositorio` (solo guarda, recibe la factura como parámetro).

<details><summary>💡 ¿Sabías que…? — Single Responsibility — un solo motivo para cambiar, sección 10</summary>

Si `Factura` cambia porque cambia el cálculo del total **y también** porque cambia el formato del archivo, tiene dos responsabilidades mezcladas — dos motivos de cambio distintos en una sola clase, justo lo que viola SRP.

```python
class Ticket:
    def save_database(self): pass
    def send_email(self): pass
    def generate_pdf(self): pass

# 3 motivos de cambio en una sola clase: viola SRP
```
```
(no se ejecuta — es el antipatrón de la teoría, sección 10)
```
</details>

<details><summary>Ver solución</summary>

```python
class Factura:
    def __init__(self, items: list[float]):
        self.items = items

    def calcular_total(self) -> float:
        return sum(self.items)

class FacturaRepositorio:
    def guardar(self, factura: Factura) -> None:
        print(f"Guardando factura por {factura.calcular_total()}")

factura = Factura([100, 250, 50])
repositorio = FacturaRepositorio()
repositorio.guardar(factura)
print(factura.calcular_total())
```
```
Guardando factura por 400
400
```
</details>

### Ejercicio 22 — SOLID (O + D): agregar un canal sin tocar nada existente
Reusando el patrón `Notificador(ABC)` con `EmailNotificador`/`SMSNotificador`, agregá un tercer canal `ConsolaNotificador` **sin modificar** ninguna de las clases anteriores ni la función `notificar_todos(canales, mensaje)`. Agregalo a la lista de canales y confirmá que funciona igual.

<details><summary>💡 ¿Sabías que…? — Open/Closed + Dependency Inversion, sección 10</summary>

`notificar_todos` depende de la **abstracción** `Notificador`, no de una clase concreta (D) — por eso puede recibir un canal que ni existía cuando se escribió la función, sin que nadie la toque (O). Es exactamente el reto resuelto de esta clase (`notification_channel.py`).

```python
channels = {"email": "EmailChannel", "sms": "SMSChannel"}

def channel_factory(kind: str):
    if kind not in channels:
        raise ValueError(f"Canal no soportado: {kind}")
    return channels[kind]

print(channel_factory("sms"))
```
```
SMSChannel
```
</details>

<details><summary>Ver solución</summary>

```python
from abc import ABC, abstractmethod

class Notificador(ABC):
    @abstractmethod
    def enviar(self, mensaje: str) -> None:
        pass

class EmailNotificador(Notificador):
    def enviar(self, mensaje: str) -> None:
        print(f"Email: {mensaje}")

class SMSNotificador(Notificador):
    def enviar(self, mensaje: str) -> None:
        print(f"SMS: {mensaje}")

# Canal nuevo — se agrega SIN tocar Notificador, EmailNotificador, SMSNotificador
# ni la función notificar_todos() de más abajo.
class ConsolaNotificador(Notificador):
    def enviar(self, mensaje: str) -> None:
        print(f"Consola: {mensaje}")

def notificar_todos(canales: list[Notificador], mensaje: str) -> None:
    for canal in canales:
        canal.enviar(mensaje)

canales = [EmailNotificador(), SMSNotificador(), ConsolaNotificador()]
notificar_todos(canales, "Tu pedido fue enviado")
```
```
Email: Tu pedido fue enviado
SMS: Tu pedido fue enviado
Consola: Tu pedido fue enviado
```
</details>

### Ejercicio 23 — Patrón Factory: centralizar qué clase instanciar
Escribí `crear_notificador(tipo: str) -> Notificador` que devuelva `EmailNotificador()` o `SMSNotificador()` según un string, y lance `ValueError` si el tipo no existe. Probalo con `"sms"` y con un tipo inválido (`"whatsapp"`) capturando el error.

<details><summary>💡 ¿Sabías que…? — Factory — centralizar la decisión de qué instanciar, sección 12</summary>

Cuando el código empieza a llenarse de `if`/`elif` para decidir qué clase crear, una función Factory concentra esa decisión en un solo lugar — quien la llama no necesita conocer las clases concretas, solo el string.

```python
def channel_factory(kind: str):
    channels = {"email": "EmailChannel", "sms": "SMSChannel"}
    if kind not in channels:
        raise ValueError(f"Canal no soportado: {kind}")
    return channels[kind]

try:
    channel_factory("fax")
except ValueError as e:
    print(f"Error: {e}")
```
```
Error: Canal no soportado: fax
```
</details>

<details><summary>Ver solución</summary>

```python
from abc import ABC, abstractmethod

class Notificador(ABC):
    @abstractmethod
    def enviar(self, mensaje: str) -> None:
        pass

class EmailNotificador(Notificador):
    def enviar(self, mensaje: str) -> None:
        print(f"Email: {mensaje}")

class SMSNotificador(Notificador):
    def enviar(self, mensaje: str) -> None:
        print(f"SMS: {mensaje}")

def crear_notificador(tipo: str) -> Notificador:
    tipos = {"email": EmailNotificador, "sms": SMSNotificador}
    if tipo not in tipos:
        raise ValueError(f"Tipo de notificador no soportado: {tipo}")
    return tipos[tipo]()

notificador = crear_notificador("sms")
notificador.enviar("Tu código es 4821")

try:
    crear_notificador("whatsapp")
except ValueError as e:
    print(f"Error: {e}")
```
```
SMS: Tu código es 4821
Error: Tipo de notificador no soportado: whatsapp
```
</details>

### Ejercicio 24 — Integrador: encapsulamiento + abstracción + composición
Crea `Pedido` con `_estado` protegido (`property estado`) y un método `confirmar(notificador: Notificador)` que: (a) valide que no esté ya confirmado — **encapsulamiento**; (b) reciba el canal por constructor del método, sin conocer la clase concreta — **abstracción + composición**. Probalo con 2 pedidos distintos, cada uno confirmado con un notificador distinto.

<details><summary>💡 ¿Sabías que…? — los 4 conceptos de esta clase, juntos, secciones 6, 7 y 9</summary>

Es el reto completo de la diapositiva de cierre (ver sección "Reto de POO" más arriba), resuelto en un solo objeto: `_estado` protegido con transición validada (6), `Notificador` inyectado sin importar cuál sea (7 + 9).

</details>

<details><summary>Ver solución</summary>

```python
from abc import ABC, abstractmethod

class Notificador(ABC):
    @abstractmethod
    def enviar(self, mensaje: str) -> None:
        pass

class EmailNotificador(Notificador):
    def enviar(self, mensaje: str) -> None:
        print(f"Email: {mensaje}")

class SMSNotificador(Notificador):
    def enviar(self, mensaje: str) -> None:
        print(f"SMS: {mensaje}")

class Pedido:
    def __init__(self, pedido_id: int):
        self.pedido_id = pedido_id
        self._estado = "creado"

    @property
    def estado(self) -> str:
        return self._estado

    def confirmar(self, notificador: Notificador) -> None:
        if self._estado == "confirmado":
            raise ValueError("El pedido ya está confirmado")
        self._estado = "confirmado"
        notificador.enviar(f"Pedido {self.pedido_id} confirmado")

pedido_1 = Pedido(101)
pedido_1.confirmar(EmailNotificador())
print(pedido_1.estado)

pedido_2 = Pedido(102)
pedido_2.confirmar(SMSNotificador())
print(pedido_2.estado)
```
```
Email: Pedido 101 confirmado
confirmado
SMS: Pedido 102 confirmado
confirmado
```
</details>

## ❓ Preguntas y respuestas (autoevaluación)
*(pendiente — 10 preguntas graduales sobre clases, encapsulamiento, abstracción,
herencia, composición y SOLID)*

## 📎 Apuntes relacionados
- [Clase 1](Clase-01.md) — tipos de datos, conversión con `int()`/`float()`, base de
  `dataclass` (antesala de los atributos tipados que ahora se ven en `Ticket`).
- [00-Notas/02-Conceptos.md](../00-Notas/02-Conceptos.md) — tabla de conceptos.

## ➡️ Siguiente
[Clase 3](Clase-03.md)
