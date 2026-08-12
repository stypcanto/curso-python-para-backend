---
categoria: "⚙️ Configuración"
sidebar: "Pylance: reportMissingImports"
---

# ❌ "No se ha podido resolver la importación 'pydantic'" (Pylance)

> [Clase 4](../01-Clases/Clase-04.md) · en `02-Ejercicios/Clase-04/app/schemas/ticket.py`

## 🧨 Qué pasó

VS Code subrayó en amarillo la primera línea de `ticket.py`:

```python
from pydantic import BaseModel, ConfigDict, Field
```

con el aviso:

```
No se ha podido resolver la importación "pydantic". Pylance(reportMissingImports)
```

## 🔍 Causa

**No es un error real de Python** — `pydantic` sí estaba instalado en el `.venv` del
proyecto (se verificó ejecutando el import por terminal y funcionó). El problema es que
**VS Code/Pylance está usando otro intérprete de Python** (no el `.venv` del proyecto),
así que no encuentra los paquetes instalados ahí.

> 📝 Pasa siempre que abrís una carpeta de proyecto nueva con su propio `.venv`: VS Code
> no lo selecciona automáticamente, hay que indicárselo una vez.

### 🤔 Por qué pasa esto (el porqué, no solo el cómo)

VS Code (Pylance) y la terminal son **dos programas separados que no se enteran uno del
otro**. `source .venv/bin/activate` solo cambia el `PATH` de *esa terminal*; VS Code
tiene su propio ajuste aparte ("Python: Select Interpreter") que hay que configurar por
su cuenta.

Cuando corrés `pip install pydantic` con el venv activado, el paquete **no se instala
"para toda la Mac"** — se copia adentro de una carpeta específica de ese venv:

```
.venv/lib/python3.14/site-packages/pydantic/   ← ahí vive de verdad
```

Por eso, si VS Code está mirando el Python **global** (`/opt/homebrew/bin/python3`, que
nunca corrió ese `pip install`), Pylance busca `pydantic` ahí, no lo encuentra, y marca
error — aunque el código esté perfecto y funcione en la terminal. Al apuntar VS Code al
`.venv/bin/python` del proyecto, Pylance empieza a mirar la carpeta correcta y el aviso
desaparece.

## ✅ Solución

1. `Cmd+Shift+P` → **"Python: Select Interpreter"**
2. Elegir el intérprete del proyecto: `./app/.venv/bin/python`
3. El subrayado desaparece (Pylance re-indexa en unos segundos)

> 💡 Cómo confirmar que el código en sí está bien, sin depender de VS Code: correr el
> import directo con el python del venv —
> `.venv/bin/python -c "from schemas.ticket import TicketBase"`. Si no tira error, el
> código está OK y el problema es 100% de configuración del editor.

## 📎 Relacionado
- [[python-command-not-found]]
- [00-Notas/05-Estructura-Proyecto-FastAPI.md](../00-Notas/05-Estructura-Proyecto-FastAPI.md)
