
numero1 = int(input("Introduce el primer numero: "))
numero2 = int(input("introduce el segundo numero: "))

operaciones_posibles = ["suma", "resta", "multiplicacion", "division"]
operacion = input("Introduce la operacion que quieres realizar: ")

try:
    if operacion == "suma":
        print(numero1 + numero2)
    elif operacion == "resta":
        print(numero1 - numero2)
    elif operacion == "multiplicacion":
        print(numero1 * numero2)
    elif operacion == "division":
        print(numero1 / numero2)
except ZeroDivisionError:
    print("No se puede dividir por 0")
while operacion not in operaciones_posibles:
    exit("Operacion no valida")
