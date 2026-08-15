
#Descripción del programa: El programa es una calculadora simple. El usuario introduce dos números y selecciona una operación aritmética. El programa calcula en consecuencia. Su misión es:

#Defina una función que realice una operación seleccionada por el usuario entre dos dígitos (a, b). ¡La operación de división ya está en el código para servir de referencia!
#Salida esperada del programa🤖

# La salida dependerá de la entrada del usuario
# Si a = 34, b = 12, y operación = * , el programa mostrará lo siguiente:

#Introduzca el primer número: 34
#Introduzca el segundo número: 12
#Introduzca la operación que desea realizar (+, -, *, /):
#Resultado: 408.0
#Aquí tiene algunos consejos 💡

#Utilice la palabra clave def para definir una función y return para devolver los resultados de la función:
#Cuando llame a una función, asegúrese de que el nombre que utiliza coincide con el declarado durante la definición de la función.
#En este caso, la función tendrá tres argumentos, ya que le pasamos dos números, ¡además de la operación!

# Tarea: Define la función que realiza la 'operación' seleccionada por el usuario 
# sobre los dos números (a, b), que también son ingresados por el usuario

def calculadora(a, b, operation):
    if operation == '/':
        if b != 0:
            # a % b es el resto de la división. Si el resto es 0, "a" se
            # divide exacto entre "b" (ej: 8 / 4 = 2.0, resto 0).
            # Si el resto NO es 0, la división no es exacta (ej: 37 / 8 =
            # 4.625, resto 5) -> avisamos en vez de solo mostrar el decimal.
            if a % b == 0:
                return a / b
            else:
                return f"{a} no es divisible entre {b}"
        else:
            return "Error: ¡Intentando dividir por cero!"
    elif operation == '+':
        return a + b
    elif operation == '-':
        return a - b
    elif operation == '*':
        return a * b
    else:
        # Si el usuario escribe algo distinto de +, -, *, /, ninguno de los
        # if/elif de arriba se cumple. Sin este 'else', la función no haría
        # ningún 'return' y devolvería None -> se imprimiría "Resultado: None"
        # sin explicar qué pasó. Mismo patrón que el error de división por
        # cero: devolver un mensaje claro en vez de un None silencioso.
        return "Error: operación no válida. Usa +, -, * o /."

# Solicitar al usuario los números y el tipo de operación
a = float(input("Ingresa el primer número: "))
b = float(input("Ingresa el segundo número: "))
operation = input("Especifica la operación que deseas realizar (+, -, *, /): ")

# Llamando a la función 'calculadora' y mostrando el resultado
result = calculadora(a, b, operation)
print("Resultado:", result)