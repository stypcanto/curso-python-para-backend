---
categoria: "🖥️ Comandos y rutas"
sidebar: "zsh: command not found: python"
---

# ❌ zsh: command not found: python

> [Clase 4](../01-Clases/Clase-04.md) · al crear el entorno virtual con `python -m venv .venv`

## 🧨 Qué pasó

```bash
❯ python -m venv .ven
zsh: command not found: python
```

## 🔍 Causa

En **macOS** (con Python instalado vía Homebrew, como en tu caso — `3.14.6`), el binario
se llama **`python3`**, no `python`. El comando `python` a secas no existe por defecto.
Además había un segundo error suelto: `.ven` en vez de `.venv` (faltaba la "v" final).

> 📝 El material del curso mostró el comando genérico `python -m venv .venv`, que sí
> funciona en Windows (ahí `python` sí existe). En macOS/Linux hay que usar `python3`.

## ✅ Solución

```bash
# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

Una vez que el `.venv` está **activado**, ahí sí `python` (a secas) funciona dentro de esa
terminal — el venv crea un symlink `python` que apunta a su propio `python3`.

## 📎 Relacionado
- [[pip-command-not-found-venv-inactivo]]
- [00-Notas/01-Comandos.md](../00-Notas/01-Comandos.md)
