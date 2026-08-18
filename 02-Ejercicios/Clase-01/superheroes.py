#Descripción del programa: Este programa añade, elimina y modifica elementos de la lista. Tus misiones son:

#Añadir Spider-Man
#Eliminar Thor
#Sustituir Capitán América por Pantera Negra
#Salida esperada del programa 🤖

#La lista final de héroes: ['Iron Man', 'Pantera Negra', 'Hulk', 'Viuda Negra', 'Spider-Man']
#Aquí tiene algunos consejos

#Declarar una lista: my_list = [1, 2, 3]

#Agregar un elemento a la lista: my_list.append(4). Esta línea añadirá el número 4 al final de la lista.

#Agregar un elemento en una posición específica: my_list.insert(1, 5). Esta línea añadirá el número 5 en la segunda posición de la lista.

#Eliminar un elemento: my_list.remove(2). Esta línea eliminará la primera aparición del número 2 en la lista.

#Cambiar un elemento en la lista: my_list[0] = 9. Esta línea reemplazará el primer elemento de la lista con el número 9.

#Acceder a un elemento en la lista: my_list[0]. Esta línea devolverá el primer elemento de la lista (9).

#Corte de lista (slicing): my_list[1:3]. Esta línea devolverá una nueva lista: [2, 3].

#Contar la cantidad de elementos en la lista: len(my_list). Esta línea devolverá 3.

# --- Solución ---

# Lista original de héroes de los Vengadores
avengers = ["Iron Man", "Capitán América", "Thor", "Hulk", "Viuda Negra"]

# Agregar a Spider-Man
avengers.append("Spider-Man")

# Eliminar a Thor
avengers.remove("Thor")

# Reemplazar a Capitán América con Pantera Negra
avengers[avengers.index("Capitán América")] = "Pantera Negra"

# La lista final de héroes de los Vengadores
print("La lista final de héroes:", avengers)
