---
categoria: "🖥️ Comandos y rutas"
sidebar: "parse error: source python3 -m venv"
---

# ❌ parse error near `)' al crear el venv con `source`

> [Clase 6](../01-Clases/Clase-06.md) · dentro de `02-Ejercicios/Clase-06/project/users_service`

## 🧨 Qué pasó

```bash
cd users_service
❯ source python3 -m venv venv
/opt/homebrew/bin/python3:1: parse error near `)'
```

## 🔍 Causa

`source` **no es parte del comando para crear el entorno virtual** — es un comando aparte
que sirve para *ejecutar un script en la sesión actual* (lo vimos al **activar** el venv,
no al crearlo: ver [[activate-sin-source-no-funciona]] y
[[zsh-command-not-found-venvscriptsactivate]]).

Al escribir `source python3 -m venv venv`, la shell no entiende "ejecutá `python3 -m venv
venv`" — entiende **"tomá el archivo `python3` y leelo línea por línea como si fuera un
script de shell"**. Pero `python3` es un binario (compilado), no un script de texto; la
shell intenta interpretar sus bytes como comandos y truena en el primer carácter que no
reconoce (`)`).

Son **dos comandos distintos con propósitos distintos** que se pisaron en uno solo:

| Paso | Comando | Para qué sirve |
|---|---|---|
| 1. Crear el venv | `python3 -m venv venv` | Crea la carpeta `venv/` con un Python aislado para este servicio. **Sin `source`.** |
| 2. Activar el venv | `source venv/bin/activate` | Activa ese entorno en la terminal actual. **Con `source`**, porque `activate` modifica variables (`PATH`, `VIRTUAL_ENV`) que solo persisten si corre en la sesión actual, no en un subshell. |

## ✅ Solución

```bash
# macOS/Linux — dos comandos separados, en este orden
cd users_service
python3 -m venv venv          # 1) crear el entorno (sin source)
source venv/bin/activate      # 2) activarlo (con source) — el prompt debe mostrar (venv)
```

> 📝 El material de la Clase 6 corre en Windows (VS Code con `PS D:\TECYLAB\...`), donde el
> equivalente de activar sería `venv\Scripts\activate` (sin `source`, PowerShell no lo
> necesita). En macOS/Linux siempre son los dos comandos de la tabla de arriba.

## 📎 Relacionado
- [[activate-sin-source-no-funciona]]
- [[zsh-command-not-found-venvscriptsactivate]] (mismo tipo de mezcla creación/activación,
  ahí con sintaxis de Windows en vez de `source` de más)
- [00-Notas/01-Comandos.md](../00-Notas/01-Comandos.md)
