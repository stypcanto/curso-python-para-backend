# Escribir un programa que almacene la cadena de caracteres holamundo en una variable,
# pregunte al usuario por la contraseña e imprima por pantalla si la contraseña introducida
# por el usuario coincide con la guardada en la variable sin tener en cuenta mayúsculas y minúsculas.

contrasena_bd = "holamundo"
contrasena_usuario = input("Ingrese la contraseña del usuario: ")


if contrasena_usuario.lower() == contrasena_bd.lower():
    print("La contraseña es correcta")
else:
    print("La contraseña es incorrecta")