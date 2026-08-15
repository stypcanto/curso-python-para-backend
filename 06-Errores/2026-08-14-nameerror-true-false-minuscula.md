---
categoria: "🧠 Lógica y tipos"
sidebar: "NameError: name 'true' is not defined"
---

# ❌ NameError: name 'true' is not defined

> [Clase 2](../01-Clases/Clase-02.md) · en `funciones.py`, primera función propia

## 🧨 Qué pasó

```python
def mi_primera_funcion(dato1, dato2):
    if dato1 > dato2:
        print(true)
    else:
        print(false)

mi_primera_funcion(10, 5)
```
```
NameError: name 'true' is not defined. Did you mean: 'True'?
```

## 🔍 Causa

En Python los booleanos son `True` y `False`, **con mayúscula inicial**. Es un error muy
común si venís de JavaScript, Java o C#, donde los booleanos se escriben en minúscula
(`true`/`false`). Python no reconoce `true` como nada — lo interpreta como el nombre de
una variable que nunca se definió, por eso el error es `NameError` (no un error de tipo).

## ✅ Solución

```python
def mi_primera_funcion(dato1, dato2):
    if dato1 > dato2:
        print(True)
    else:
        print(False)

mi_primera_funcion(10, 5)   # True
```

> 💡 El propio intérprete de Python ayuda acá: el mensaje incluye *"Did you mean:
> 'True'?"* — vale la pena leer el mensaje completo del error, no solo la primera línea.

## 📎 Relacionado
- [Clase 1](../01-Clases/Clase-01.md) — tipos de datos básicos (`bool` ya aparece ahí).
- [00-Notas/01-Comandos.md](../00-Notas/01-Comandos.md)
