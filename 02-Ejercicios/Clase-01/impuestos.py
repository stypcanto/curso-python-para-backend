#Pra tributar un determinado impeusto se debe ser mayor de 16 años y tener unos ingresos iguales o superiores
# a 1000 e mensuales. Escribir un programa que pregunte al usuairo su edad y sus ingresos mensuales
# y muesrtre por pantalla si el usuario tiene que tributar o no

salario = float(input("Ingrese su salario: "))
edad = int (input("Ingrese su edad: "))

if edad >= 16:
        print(f"Tiene que tributar, le corresponde {salario * 0.18} soles")
else:  
        print("Aun no tiene que tributar")