import random

MINIMO = 1

dificultad = input("Selecciona la dificultad (F,M,D): ")
if dificultad == "F":
    maximo = 10
elif dificultad == "M":
    maximo = 50
elif dificultad == "D":
    maximo = 100
elif dificultad not in "FMD":
    print("dificultad no valida")
    maximo = 10


intentos = 0
numero_azar = random.randint(MINIMO, maximo)

while True:
    intento_usuario = int(
        input(f"Introdue un numero entre el 1 y el {maximo} : "))
    intentos += 1
    if intento_usuario > numero_azar:
        print("Te pasaste, el numero es mas pequeño que " + str(intento_usuario))
    elif intento_usuario < numero_azar:
        print("Te quedaste corto, el numero es mas grande que " +
              str(intento_usuario))
    else:
        break
print("Felicidades, adivinaste el numero")
print(f"Numero de intentos: {intentos}")
