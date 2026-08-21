# Diagrama de arquitectura — Clase 6

Arquitectura de `users_service` y `products_service` (Python para Backend, Clase 6):
cada microservicio con su `config.py` → `main.py` → `routers/*.py` → lista en memoria,
más la llamada HTTP entre servicios del Ejercicio 10 (`products_service` consulta a
`users_service` por su API pública, vía `httpx`).

## Regenerar

```bash
cd 04-Recursos/diagramas-tecnicos/clase-06-arquitectura-microservicios
dot -Tsvg src/arquitectura-clase-06.dot -o svg/arquitectura-clase-06.svg
dot -Tpng -Gdpi=180 src/arquitectura-clase-06.dot -o png/arquitectura-clase-06.png
cp png/arquitectura-clase-06.png ../../../public/clase-06-arquitectura-microservicios.png
```

Si se edita el `.dot`, hay que repetir el `cp` final — `public/` no se actualiza solo.
