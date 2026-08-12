# Instrucciones del proyecto — Python para Backend

## 💻 Entorno de Styp: macOS

Styp trabaja en **macOS** (zsh). Cuando el material del curso (slides, capturas) muestra
comandos para Windows, en las notas:

1. Se documenta primero el comando para **macOS/Linux** (el que Styp realmente usa).
2. El comando de Windows de la diapositiva se deja como referencia secundaria, marcado
   claramente como tal (o se omite si no aporta).
3. Si el profe no muestra el comando de macOS/Linux, se agrega igual y se aclara con un
   callout `> 📝` que no estaba en la diapositiva.

**Ejemplo — activación de entorno virtual (`venv`):**
```bash
# Activación en macOS/Linux
source .venv/bin/activate

# Activación en Windows (si el material del curso la muestra, se deja de referencia)
.\.venv\Scripts\activate
```

Aplica a cualquier comando sensible al sistema operativo (activar `venv`, variables de
entorno, rutas, etc.) en `01-Clases/`, `00-Notas/01-Comandos.md` y `05-Snippets/`.

## 📌 Pendientes

- **Bruno (Clase 4, sección 15 — Postman/Bruno):** falta repetir con Bruno el mismo
  recorrido de 13 pasos que ya está documentado con capturas de Postman (Environment →
  variable `base_url` → Collection → los 5 endpoints, incluido el error de FK). Mismos
  pasos, otro cliente — cuando Styp tenga las capturas de Bruno, se agregan al lado de
  las de Postman en `01-Clases/Clase-04.md` (sección "🖱️ Cómo se hizo en Postman
  (capturas propias) — recorrido completo").
