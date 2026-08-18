lista_solicitudes = [
     { "id": 1001,
        "title":"Error de acceso 1"},
     { "id": 1002,
        "title":"Error de acceso 2"},
     { "id": 1003,
        "title":"Error de acceso 3"},
]

contador = 0
while contador < 3:
    print(lista_solicitudes[contador].get("id"))
    contador = contador + 1