---
categoria: "🖥️ Comandos y rutas"
sidebar: "zsh: command not found: .venvScriptsactivate"
---

# ❌ zsh: command not found: .venvScriptsactivate

> [Clase 1](../01-Clases/Clase-01.md) · al activar el `venv` de `02-Ejercicios/Clase-01`

## 🧨 Qué pasó

```bash
❯ python3 -m venv .venv
❯ .\venv\Scripts\activate
zsh: command not found: .venvScriptsactivate
```

## 🔍 Causa

Dos problemas mezclados:

1. **Comando de Windows en una terminal macOS/Linux.** `.\venv\Scripts\activate` es la
   sintaxis de PowerShell/cmd. zsh no reconoce las barras invertidas (`\`) como
   separador de rutas — las interpreta como caracter de escape y las descarta, por eso
   el error final muestra todo pegado: `.venvScriptsactivate`.
2. **Faltaba `pwd` en la carpeta correcta.** Además, si te movés (`cd`) **dentro** de la
   carpeta `.venv` en vez de quedarte en la carpeta del ejercicio (`Clase-01/`), ni
   siquiera el comando correcto de macOS encuentra la ruta — `.venv` no está dentro de
   sí misma.

## ✅ Solución

```bash
cd 02-Ejercicios/Clase-01     # la carpeta del ejercicio, NO adentro de .venv
source .venv/bin/activate     # el prompt debe mostrar (.venv) al inicio
```

> 💡 `source` es necesario porque `activate` modifica variables de entorno (`PATH`,
> `VIRTUAL_ENV`). Ejecutado normal, zsh lo corre en un subshell que se cierra apenas
> termina, sin que la terminal actual se entere del cambio. `source` lo corre **en la
> sesión actual** — ver la tabla comparativa en [00-Notas/01-Comandos.md](../00-Notas/01-Comandos.md).

## 📎 Relacionado
- [[python-command-not-found]]
- [[pip-command-not-found-venv-inactivo]]
- [00-Notas/01-Comandos.md](../00-Notas/01-Comandos.md)

## 🔁 Recurrió en Clase 3 (2026-08-20)
Mismo error, mismo motivo — esta vez con el venv llamado `venv` (sin punto, no `.venv`)
en `02-Ejercicios/Clase-03/`:

```bash
❯ python3 -m venv venv
❯ venv\Scripts\activate
zsh: command not found: venvScriptsactivate
```

La solución fue la misma, ajustada al nombre de esta carpeta (`venv`, no `.venv`):

```bash
source venv/bin/activate
```

Con el venv ya activado, instaló FastAPI y Uvicorn — ver
[Clase 3 — Primer proyecto](../01-Clases/Clase-03.md#🧪-primer-proyecto-—-02-ejercicios-clase-03):
```bash
pip install fastapi "uvicorn[standard]"
```

## 🔁 Recurrió en Clase 6 (2026-08-20)

Mismo error base (sintaxis de Windows en zsh), esta vez en
[Clase 6](../01-Clases/Clase-06.md), dentro de `users_service/`, con **tres intentos
seguidos** que muestran cada paso intermedio del "¿por qué no prende?":

```bash
❯ python3 -m venv venv
❯ venv\Scripts\activate
zsh: command not found: venvScriptsactivate

❯ source venv\Scripts\activate
source: no such file or directory: venvScriptsactivate

❯ .source venv\Scripts\activate
zsh: command not found: .source
```

| Intento | Qué le faltaba |
|---|---|
| `venv\Scripts\activate` | Dos cosas: sintaxis de Windows (`\` en vez de `/`, y `Scripts` en vez de `bin` — así arma la ruta un venv creado en macOS/Linux) **y** falta `source` adelante. |
| `source venv\Scripts\activate` | Ya agregó `source` ✅, pero la ruta sigue en sintaxis Windows — zsh se come las `\` y busca un archivo llamado `venvScriptsactivate` que no existe. |
| `.source venv\Scripts\activate` | Intento de "arreglar" pegándole un `.` a `source` (`.source` no es nada — ni el operador `.` de POSIX, que va **separado** con espacio, ni el comando `source`). Sigue sin resolver el problema real: la ruta. |

**La única corrección que hace falta es la ruta**, no agregarle símbolos a `source`:

```bash
# macOS/Linux — activar el venv que ya creaste con python3 -m venv venv
source venv/bin/activate      # bin, no Scripts · / no \ · el prompt debe mostrar (venv)
```

> 📝 `Scripts\activate` (con `\`) es la ruta que genera un venv creado en **Windows**; en
> macOS/Linux el mismo `python3 -m venv venv` genera la carpeta `bin/`, no `Scripts/` — no
> es solo cambiar la barra, la carpeta interna también se llama distinto.
