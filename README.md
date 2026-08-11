# 🐍 Python para Backend

> Apuntes del curso, organizados para llevar el control de clases, ejercicios y dudas.
> Formato de notas: ver [00-Notas](00-Notas/) y el índice de clases en
> [01-Clases/00-Indice.md](01-Clases/00-Indice.md).

## 🗂️ Estructura

| Carpeta | Contenido |
|---|---|
| [`00-Notas/`](00-Notas/) | Comandos, conceptos, preguntas abiertas, preguntas de entrevista |
| [`01-Clases/`](01-Clases/) | Resumen de cada clase (teoría + práctica + ejercicios + preguntas) |
| [`02-Ejercicios/`](02-Ejercicios/) | Código de los ejercicios prácticos, por clase |
| [`03-Proyectos/`](03-Proyectos/) | Proyectos del curso |
| [`04-Recursos/`](04-Recursos/) | Enlaces, PDFs, imágenes, herramientas |
| [`05-Snippets/`](05-Snippets/) | Fragmentos de código reutilizables |
| [`06-Errores/`](06-Errores/) | Errores reales y cómo se resolvieron |
| [`90-Resumen/`](90-Resumen/) | Resumen final para repasar todo el curso |

## 🚦 Cómo se documenta

Cada clase se agrega a [`01-Clases/00-Indice.md`](01-Clases/00-Indice.md) apenas empieza,
y se completa con `Teoría → Práctica → 10 Ejercicios con solución → 10 Preguntas y
respuestas` a medida que avanza. Ver la skill `apuntes-curso` para el detalle del formato.

## 🌐 Sitio web de apuntes (VitePress)

Los `.md` de este repo se sirven además como un sitio navegable (sidebar automático,
buscador local, modo oscuro, callouts de colores). El sidebar se arma solo leyendo
`01-Clases/`, `00-Notas/`, `05-Snippets/`, `03-Proyectos/`, `06-Errores/` y
`90-Resumen/` — un apunte nuevo aparece sin tocar la configuración.

```bash
npm install          # una sola vez
npm run docs:dev      # → http://localhost:5173
npm run docs:build    # verifica que compile sin errores
```

- Config: [`.vitepress/config.ts`](.vitepress/config.ts) (nombre del curso: `Python para
  Backend`) y el color de marca en
  [`.vitepress/theme/custom.css`](.vitepress/theme/custom.css) (`#3776ab`, el azul de
  Python).
- Deploy (subdominio en Hostinger): completar `NOMBRE_SUBDOMINIO` en el script `deploy`
  de `package.json` cuando se cree el subdominio, y correr `npm run deploy`.
- Detalle completo del montaje: skill `apuntes-curso`, sección 7.
