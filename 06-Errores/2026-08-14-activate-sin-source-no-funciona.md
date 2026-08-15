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
