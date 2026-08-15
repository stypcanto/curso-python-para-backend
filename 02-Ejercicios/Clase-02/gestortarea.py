#Construir estas tareas para organizar profesionalmente mediante funciones independientes:
# Mostrar tarea
# Agregar tarea
# Eliminar la tarea


def mostrar_tarea(lista):
    """Imprime todas las tareas de la lista, numeradas desde 1."""
    if len(lista) == 0:
        print("No hay tareas pendientes.")
    else:
        # f-string en vez de "texto" + len(lista): len() devuelve un int,
        # y "str" + int no se puede concatenar directo con + en Python.
        print(f"Tienes {len(lista)} tareas pendientes:")
        # enumerate(lista, start=1): recorre la lista dando también el índice
        # (i), empezando en 1 en vez de 0 -> así el usuario ve "1. tarea",
        # no "0. tarea".
        for i, t in enumerate(lista, start=1):
            print(f'{i}. []{t}')


def agregar_tarea(lista, nueva_tarea):
    """Agrega una tarea nueva al final de la lista (modifica la lista original)."""
    lista.append(nueva_tarea)
    print(f'Tarea "{nueva_tarea}" agregada correctamente.')


def eliminar_tarea(lista, numero):
    """Elimina la tarea en la posición `numero` (numeración 1..N, no 0..N-1)."""
    if 1 <= numero <= len(lista):
        # El usuario piensa en "tarea 1, 2, 3...", pero las listas de Python
        # empiezan en 0 -> por eso numero - 1 para llegar al índice real.
        # .pop(indice) borra ese elemento Y lo devuelve (para poder avisar cuál se borró).
        borrada = lista.pop(numero - 1)
        print(f'Tarea "{borrada}" eliminada correctamente.')
    else:
        print("Número de tarea inválido. No se pudo eliminar la tarea.")


# BUCLE — el programa se repite hasta que el usuario elige "4. Salir"
mis_tareas = ['Programar en Python', 'Hacer ejercicio', 'Leer un libro']

while True:
    print("\nGestor de Tareas")
    print("1. Mostrar tareas")
    print("2. Agregar tarea")
    print("3. Eliminar tarea")
    print("4. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        mostrar_tarea(mis_tareas)
    elif opcion == "2":
        nueva_tarea = input("Ingrese la nueva tarea: ")
        agregar_tarea(mis_tareas, nueva_tarea)
    elif opcion == "3":
        # try/except: si el usuario escribe algo que no es número (ej. "abc"),
        # int(...) lanza ValueError. Sin este bloque, el programa se cerraría
        # de golpe con un error feo (mismo patrón visto en la Clase 1).
        try:
            numero = int(input("Ingrese el número de la tarea a eliminar: "))
            eliminar_tarea(mis_tareas, numero)
        except ValueError:
            print("Eso no es un número válido. Intenta de nuevo.")
    elif opcion == "4":
        print("Saliendo del gestor de tareas.")
        break
    else:
        print("Opción inválida. Por favor, seleccione una opción válida.")
