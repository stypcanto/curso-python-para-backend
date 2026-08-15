#empleado de 50 anos
input_edad = input("Ingrese la edad del empleado: ")
edad = int(input_edad)


#65 años de te jubilarse
#empleado tiene mas de 65 anos para jubilarse
if edad >= 65:
    print("El empleado puede jubilarse")
    print("El empleado tiene " + str(edad) + " años")
else:
    print("El empleado no puede jubilarse")
    print("El empleado tiene " + str(edad) + " años")