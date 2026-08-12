---
sidebar: "Clase 2 · POO y arquitectura"
---

# 📙 Clase 2 — Programación orientada a objetos y arquitectura

> Python para Backend · 2026-08-04 · Carpeta: `02-Ejercicios/Clase-02`
> ⬅️ Volver al [índice de clases](00-Indice.md)

## 🎯 Qué aprendí (según temario — por confirmar/completar al documentar la clase)
- Clases y objetos
- Herencia y composición
- Encapsulamiento y abstracción
- Principios SOLID
- Organización de proyectos Python
- Patrones básicos de diseño

# 📖 PARTE TEÓRICA

> 📌 **Esta teoría no viene de la clase real dictada por el profe** (todavía no pasé
> capturas ni grabación de la Clase 2) — es **teoría estándar de referencia**, armada solo
> a partir de los 6 puntos del temario (ver "Qué aprendí" arriba) y verificada con fuentes
> externas y en terminal. Cuando tenga el material real de la clase, esta sección se
> revisa y se completa con los ejemplos/orden que haya dado el profe — no se descarta,
> se enriquece.

## 🏗️ 1. Clases y objetos
Una **clase** es el molde: define qué datos (atributos) y qué comportamientos (métodos)
va a tener cada cosa que se cree a partir de ella. Un **objeto** es una instancia
concreta de esa clase — cada `SupportTicket(...)` que se crea es un objeto distinto, con
sus propios valores, aunque comparta la misma "forma".

```python
class SupportTicket:
    """Representa una solicitud de soporte."""

    def __init__(self, id: int, title: str, priority: str):
        self.id = id            # atributo de instancia
        self.title = title
        self.priority = priority

    def describe(self) -> str:
        return f"Ticket {self.id}: {self.title} ({self.priority})"


t1 = SupportTicket(1001, "Error de acceso", "Alta")
t2 = SupportTicket(1002, "Lentitud del sistema", "Media")

print(t1.describe())
print(t2.describe())
print(t1 is t2)
```
```
Ticket 1001: Error de acceso (Alta)
Ticket 1002: Lentitud del sistema (Media)
False
```

| Concepto | Qué es |
|---|---|
| `class` | Define el molde (atributos + métodos). |
| `__init__` | El **constructor**: se ejecuta al crear el objeto (`SupportTicket(...)`) y arma su estado inicial. |
| `self` | Referencia al propio objeto — así cada método sabe sobre cuál instancia está trabajando. |
| Atributo | Dato que vive en el objeto (`self.title`). |
| Método | Función que vive en la clase y opera sobre el objeto (`describe()`). |

> 💡 `t1 is t2` da `False` porque son dos objetos **distintos** en memoria, aunque tengan
> la misma clase — es el mismo principio de identidad vs. igualdad que ya apareció con
> mutabilidad/aliasing en la Clase 1 (sección "para ir más allá").

> 🧪 Tip de entrevista: ¿diferencia entre clase y objeto? La clase es la **definición**
> (existe una sola vez en el código); el objeto es una **instancia en memoria** creada a
> partir de esa definición (pueden existir muchos, cada uno con su propio estado).

## 🧬 2. Herencia y composición
Son las dos formas de **reutilizar código entre clases**, pero responden preguntas
distintas: herencia responde "¿qué **ES**?", composición responde "¿qué **TIENE**?".

```python
class Ticket:
    def __init__(self, id: int, title: str):
        self.id = id
        self.title = title

    def describe(self) -> str:
        return f"Ticket {self.id}: {self.title}"


# Herencia: UrgentTicket "ES" un Ticket (extiende su comportamiento)
class UrgentTicket(Ticket):
    def __init__(self, id: int, title: str, escalated_to: str):
        super().__init__(id, title)          # reutiliza el __init__ del padre
        self.escalated_to = escalated_to

    def describe(self) -> str:
        base = super().describe()            # reutiliza el describe() del padre
        return f"{base} — ESCALADO a {self.escalated_to}"


u = UrgentTicket(2001, "Caída del servidor", "Infraestructura")
print(u.describe())
print(isinstance(u, Ticket))


# Composición: SupportAgent "TIENE" un Logger (usa sus servicios, no hereda de él)
class Logger:
    def log(self, message: str) -> None:
        print(f"[LOG] {message}")


class SupportAgent:
    def __init__(self, name: str):
        self.name = name
        self.logger = Logger()               # composición: el agente contiene un logger

    def resolve(self, ticket: Ticket) -> None:
        self.logger.log(f"{self.name} resolvió: {ticket.describe()}")


agent = SupportAgent("Styp")
agent.resolve(u)
```
```
Ticket 2001: Caída del servidor — ESCALADO a Infraestructura
True
[LOG] Styp resolvió: Ticket 2001: Caída del servidor — ESCALADO a Infraestructura
```

| | Herencia (`class B(A)`) | Composición (`self.x = X()`) |
|---|---|---|
| Relación | "ES UN/A" (`UrgentTicket` ES UN `Ticket`) | "TIENE UN/A" (`SupportAgent` TIENE UN `Logger`) |
| Acoplamiento | Más fuerte — la subclase queda atada a la implementación del padre | Más flexible — se puede cambiar el objeto interno sin tocar la clase que lo usa |
| Cuándo usarla | Cuando de verdad hay una jerarquía "tipo de" | Para la mayoría de los demás casos (reutilizar comportamiento sin heredar) |

> 📌 Regla de oro muy citada en diseño OO: **"favorece la composición sobre la
> herencia"** — no porque la herencia esté mal, sino porque abusar de ella genera
> jerarquías rígidas y difíciles de cambiar. La herencia se reserva para cuando la
> relación "ES UN/A" es real y estable.

> 🧪 Tip de entrevista: ¿cuándo usar herencia y cuándo composición? Herencia si el objeto
> **es un tipo más específico** del padre (un `UrgentTicket` sigue siendo, ante todo, un
> `Ticket`); composición si el objeto **usa un servicio de otro** para funcionar (un
> `SupportAgent` usa un `Logger`, pero no "es" un logger).

## 🔒 3. Encapsulamiento y abstracción
**Encapsulamiento**: agrupar datos y los métodos que los manejan dentro de la misma
clase, y controlar qué se puede tocar desde afuera. **Abstracción**: exponer *qué* hace
algo, escondiendo *cómo* lo hace por dentro — quien usa la clase no necesita saber los
detalles internos.

```python
class BankAccount:
    def __init__(self, owner: str, balance: float):
        self.owner = owner
        self._balance = balance          # "protegido" (convención: no tocar desde afuera)
        self.__pin = "1234"              # "privado" (name mangling: _BankAccount__pin)

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("El depósito debe ser positivo")
        self._balance += amount

    def get_balance(self) -> float:
        return self._balance


acc = BankAccount("Styp", 100.0)
acc.deposit(50.0)
print(acc.get_balance())
print(acc._BankAccount__pin)   # accesible igual, pero deja claro que "no debería" tocarse
```
```
150.0
1234
```

| Prefijo | Convención | Qué significa |
|---|---|---|
| `nombre` | público | Se puede usar libremente desde afuera de la clase. |
| `_nombre` | protegido | *Convención* ("uso interno") — Python no lo bloquea, solo lo sugiere. |
| `__nombre` | privado | Python le cambia el nombre por dentro (*name mangling* → `_Clase__nombre`) para dificultar el acceso accidental, pero **sigue siendo accesible**. |

> ⚠️ Python **no tiene encapsulamiento estricto** como Java (`private` de verdad). Todo es
> convención: el `_`/`__` es una señal para quien lee el código ("no lo toques desde
> afuera"), no una barrera real que el lenguaje imponga.

La abstracción se implementa formalmente con **clases abstractas** (`ABC`): definen *qué*
métodos debe tener una familia de clases, sin decir *cómo* los implementa cada una.

```python
from abc import ABC, abstractmethod

class NotificationChannel(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        ...

class EmailChannel(NotificationChannel):
    def send(self, message: str) -> None:
        print(f"Email enviado: {message}")

class SMSChannel(NotificationChannel):
    def send(self, message: str) -> None:
        print(f"SMS enviado: {message}")

def notify_all(channels: list[NotificationChannel], message: str) -> None:
    for channel in channels:
        channel.send(message)      # no le importa CÓMO envía cada canal, solo QUE puede enviar

notify_all([EmailChannel(), SMSChannel()], "Ticket 2001 resuelto")

try:
    NotificationChannel()   # no se puede instanciar directamente: es abstracta
except TypeError as e:
    print("Error esperado:", e)
```
```
Email enviado: Ticket 2001 resuelto
SMS enviado: Ticket 2001 resuelto
Error esperado: Can't instantiate abstract class NotificationChannel without an implementation for abstract method 'send'
```

> 💡 `notify_all` no sabe (ni le importa) si el canal es email o SMS — solo confía en que
> **cualquier** `NotificationChannel` tiene un método `send`. Esa es la abstracción en la
> práctica: programar contra la interfaz, no contra el detalle.

## 🧱 4. Principios SOLID
SOLID es un acrónimo de 5 principios de diseño orientado a objetos que buscan código
**fácil de mantener, extender y probar**. No son reglas exclusivas de Python (nacieron en
el mundo de lenguajes más estrictos como Java/C#), pero aplican igual.

| Letra | Principio | Idea central |
|---|---|---|
| **S** | Single Responsibility (responsabilidad única) | Una clase debe tener **una sola razón para cambiar**. |
| **O** | Open/Closed (abierto/cerrado) | Abierta a **extenderse** (agregar casos nuevos), cerrada a **modificarse** (no tocar lo que ya funciona). |
| **L** | Liskov Substitution (sustitución de Liskov) | Una subclase debe poder **reemplazar** a su clase base sin romper el comportamiento esperado. |
| **I** | Interface Segregation (segregación de interfaces) | Mejor varias interfaces **chicas y específicas** que una gigante y genérica. |
| **D** | Dependency Inversion (inversión de dependencias) | Depender de **abstracciones**, no de clases concretas. |

```python
from abc import ABC, abstractmethod

# S — cada clase tiene UNA sola razón para cambiar
class Ticket:
    def __init__(self, id: int, priority: str):
        self.id = id
        self.priority = priority

class TicketRepository:
    """Solo se ocupa de guardar/leer tickets (no de calcular ni notificar)."""
    def __init__(self):
        self._tickets: list[Ticket] = []

    def save(self, ticket: Ticket) -> None:
        self._tickets.append(ticket)


# O — se agregan casos nuevos SIN modificar el código existente
class PriorityCalculator(ABC):
    @abstractmethod
    def response_hours(self) -> int: ...

class HighPriority(PriorityCalculator):
    def response_hours(self) -> int:
        return 2

class MediumPriority(PriorityCalculator):
    def response_hours(self) -> int:
        return 8
    # mañana se agrega LowPriority sin tocar ninguna clase existente

def print_response_time(calculator: PriorityCalculator) -> None:
    print(f"Responder en {calculator.response_hours()}h")

print_response_time(HighPriority())
print_response_time(MediumPriority())


# L — una subclase debe poder sustituir a su clase base sin sorpresas
class Bird:
    def move(self) -> str:
        return "se mueve"

class FlyingBird(Bird):
    def move(self) -> str:
        return "vuela"

def describe_movement(bird: Bird) -> None:
    print(bird.move())

describe_movement(Bird())
describe_movement(FlyingBird())   # sustituye a Bird sin romper describe_movement()


# I — interfaces chicas y específicas, no una gigante
class Readable(ABC):
    @abstractmethod
    def read(self) -> str: ...

class Writable(ABC):
    @abstractmethod
    def write(self, data: str) -> None: ...

class ReadOnlyFile(Readable):
    def read(self) -> str:
        return "contenido"

rof = ReadOnlyFile()
print(rof.read())    # no está obligado a implementar write()


# D — depender de una abstracción, no de una clase concreta
class NotificationSender(ABC):
    @abstractmethod
    def send(self, message: str) -> None: ...

class EmailSender(NotificationSender):
    def send(self, message: str) -> None:
        print(f"Email: {message}")

class TicketService:
    def __init__(self, sender: NotificationSender):   # depende de la abstracción
        self._sender = sender

    def close_ticket(self, ticket_id: int) -> None:
        self._sender.send(f"Ticket {ticket_id} cerrado")

service = TicketService(EmailSender())   # se puede cambiar por SMSSender sin tocar TicketService
service.close_ticket(1001)
```
```
Responder en 2h
Responder en 8h
se mueve
vuela
contenido
Email: Ticket 1001 cerrado
```

> ⚠️ Error común: confundir "clase pequeña" (S) con "clase con un solo método". SRP habla
> de **una sola razón para cambiar** (un solo motivo de negocio), no de un límite de
> líneas — una clase puede tener varios métodos y seguir cumpliendo SRP si todos giran
> alrededor de la misma responsabilidad.

> 🧪 Tip de entrevista: ¿por qué "Dependency Inversion" y no simplemente "usar
> interfaces"? Porque invierte quién depende de quién: normalmente el código de alto
> nivel (`TicketService`) dependería directo del de bajo nivel (`EmailSender`); con DIP,
> **ambos** dependen de una abstracción (`NotificationSender`) — de ahí "inversión".

## 📁 5. Organización de proyectos Python
A medida que un proyecto crece, mezclar toda la lógica en un solo archivo (o en
funciones sueltas sin agrupar) se vuelve difícil de mantener. La convención más usada en
backend es separar por **responsabilidad** (parecido al principio S de SOLID, pero a
nivel de carpetas en vez de clases):

```
mi_backend/
├── .venv/                  # entorno virtual (no se sube a git)
├── requirements.txt        # dependencias del proyecto
├── main.py                 # punto de entrada (arranca la app)
└── mi_backend/              # el paquete real del proyecto (mismo nombre, buena práctica)
    ├── __init__.py
    ├── models/              # entidades del dominio (qué ES un Ticket, un Usuario…)
    │   └── ticket.py
    ├── repositories/        # acceso a datos: guardar/leer (hoy en memoria, después en BD)
    │   └── ticket_repository.py
    ├── services/            # lógica de negocio (reglas, cálculos, validaciones)
    │   └── ticket_service.py
    └── routes/              # (más adelante, con FastAPI) los endpoints HTTP
        └── ticket_routes.py
└── tests/                   # pruebas, separadas del código de la app
    └── test_ticket_service.py
```

| Carpeta | Responsabilidad | Analogía con SOLID |
|---|---|---|
| `models/` | Define la forma de los datos del dominio (parecido a la `dataclass` de la Clase 1). | — |
| `repositories/` | Aísla **cómo** se guardan/leen los datos (lista en memoria, base de datos…). | Si mañana cambia de memoria a PostgreSQL, solo cambia esta carpeta — el resto ni se entera (D). |
| `services/` | Reglas de negocio: qué hacer con los datos, no cómo guardarlos. | Cada servicio con una responsabilidad clara (S). |
| `routes/` | La "puerta de entrada" HTTP — traduce peticiones en llamadas a los servicios. | — |
| `tests/` | Pruebas separadas del código de producción. | — |

> 💡 Esta separación (`models` / `repositories` / `services` / `routes`) es exactamente la
> antesala del **Repository Pattern** que se va a formalizar en la Clase 4 (PostgreSQL +
> SQLAlchemy) — la idea ya aparece acá, solo que sin base de datos real todavía.

> 📌 El nombre de la carpeta del paquete interno (`mi_backend/mi_backend/`) suele repetir
> el nombre del proyecto — es la convención más común en la comunidad Python para que
> `import mi_backend` funcione igual una vez instalado el paquete.

## 🧩 6. Patrones básicos de diseño
Un **patrón de diseño** es una solución ya probada a un problema recurrente de diseño de
software — no es código para copiar y pegar tal cual, sino una plantilla que se adapta al
contexto.

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
> 💡 Uso típico: un logger o una configuración global que debe ser **una sola** en toda la
> aplicación (evita, por ejemplo, tener dos conexiones de configuración desincronizadas).

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
> instanciar — la Factory concentra esa decisión en un solo lugar.

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
> mismo patrón que ya usamos sin nombrarlo en la Clase 1 al pasar una función distinta a
> `key=` de `sorted()`... salvo que ahí no la usamos; acá es la primera vez, pero la idea
> de "pasar comportamiento como parámetro" ya apareció con las funciones de la Clase 1.

| Patrón | Problema que resuelve | Dónde se vuelve a ver más adelante en el curso |
|---|---|---|
| Singleton | Necesito una única instancia compartida | Conexión a base de datos, configuración de la app (Clase 4+) |
| Factory | Necesito crear objetos sin acoplarme a la clase exacta | Crear instancias de modelos/servicios según el tipo de petición |
| Strategy | Necesito intercambiar un algoritmo sin tocar el código que lo usa | Repository Pattern (Clase 4): cambiar de dónde vienen los datos sin tocar el servicio |

> 🧪 Tip de entrevista: ¿diferencia entre Factory y Strategy? Factory decide **qué objeto
> crear**; Strategy decide **qué algoritmo ejecutar** sobre un objeto que ya existe. Se
> pueden combinar (una Factory que devuelve la Strategy correcta según el caso).

> 🔗 Fuentes usadas para verificar esta teoría (búsqueda web, agosto 2026):
> [Los pilares de la POO en Python](https://picodotdev.github.io/blog-bitix/2021/03/los-conceptos-de-encapsulacion-herencia-polimorfismo-y-composicion-de-la-programacion-orientada-a-objetos/) ·
> [Principios SOLID en Python](https://softwarecrafters.io/python/principios-solid-python) ·
> [Estructurando tu proyecto — The Hitchhiker's Guide to Python](https://python-guide-es.readthedocs.io/es/latest/writing/structure.html) ·
> [Patrones de diseño en Python — Refactoring Guru](https://refactoring.guru/es/design-patterns/python)

# 💻 PARTE PRÁCTICA
*(pendiente)*

# 🏋️ EJERCICIOS CON SOLUCIÓN
*(pendiente — se documentan 10 ejercicios graduales cuando haya contenido de la clase)*

## ❓ Preguntas y respuestas (autoevaluación)
*(pendiente — 10 preguntas graduales)*

## 📎 Apuntes relacionados
*(pendiente)*

## ➡️ Siguiente
[Clase 3](Clase-03.md)
