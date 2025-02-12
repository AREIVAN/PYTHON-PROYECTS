# Lista de números a ordenar
arr = [5, 3, 4, 8, 7, 5, 1, 2, 3, 10, 92, 2]
print("Arreglo original:", arr)

# Algoritmo de ordenamiento por inserción
for j in range(1, len(arr)):
    # Elemento actual a insertar en la parte ordenada del arreglo
    actual = arr[j]

    i = j - 1
    # Desplazar elementos de la parte ordenada del arreglo hacia la derecha
    # para hacer espacio para el elemento actual
    while i >= 0 and arr[i] > actual:
        arr[i + 1] = arr[i]
        i = i - 1
    # Insertar el elemento actual en su posición correcta
    arr[i + 1] = actual

# Imprimir el arreglo ordenado
print("Arreglo ordenado:", arr)

"""
El algoritmo de ordenamiento por inserción no es muy eficiente para arreglos grandes
debido a su complejidad temporal de O(n^2) en el peor de los casos.
"""
