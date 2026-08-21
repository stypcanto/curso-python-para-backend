---
categoria: "🖥️ Comandos y rutas"
sidebar: "command not found: uvicorn[standard]"
---

# ❌ zsh: command not found: uvicorn[standard]

> [Clase 6](../01-Clases/Clase-06.md) · instalando dependencias en `users_service`

## 🧨 Qué pasó

```bash
❯ "uvicorn[standard]"
zsh: command not found: uvicorn[standard]
```

(pasó dos veces seguidas — mismo motivo las dos).

## 🔍 Causa

Al comando **le faltaba `pip install` adelante**. `"uvicorn[standard]"` a secas no es un
comando de terminal — es un **argumento** que hay que pasarle a `pip install`. Al
ejecutarlo solo, zsh intenta buscar un programa que se llame literalmente
`uvicorn[standard]` en el `PATH`, no lo encuentra, y avisa "command not found".

Las comillas alrededor (`"uvicorn[standard]"`) sí eran necesarias — sin ellas zsh
interpretaría `[standard]` como un patrón glob y fallaría con `no matches found` en vez
de `command not found` — pero comillas correctas con un comando incompleto sigue sin
funcionar: falta la primera palabra, `pip install`.

## ✅ Solución

```bash
pip install fastapi "uvicorn[standard]"
```

El extra `[standard]` de uvicorn instala dependencias opcionales de rendimiento
(`uvloop`, `httptools`, `websockets`, `watchfiles`, entre otras) — por eso el instalador
baja varios paquetes de golpe en vez de uno solo.

## 📎 Relacionado
- [00-Notas/01-Comandos.md](../00-Notas/01-Comandos.md)
- [[activate-sin-source-no-funciona]] (otro caso de mezclar/perder una palabra del
  comando en la misma sesión de instalación)
