import random

movimientos = ["piedra", "papel", "tijera"]

movimiento_ia = random.choice(movimientos)
movimiento_usuario = input("Introduce tu movimiento: (piedra,papel,tijera) ")
if movimiento_usuario not in movimientos:
    print("Movimiento no válido")
    quit()

print(F"has elegido {movimiento_usuario}")
print(F"ha elegido {movimiento_ia}")


if movimiento_usuario == "piedra":
    if movimiento_ia == "papel":
        print("Perdiste")
elif movimiento_ia == "tijera":
    print("Ganaste")

if movimiento_usuario == "papel":
    if movimiento_ia == "tijera":
        print("Perdiste")
    elif movimiento_ia == "piedra":
        print("Ganaste")

if movimiento_usuario == "tijera":
    if movimiento_ia == "piedra":
        print("Perdiste")
    elif movimiento_ia == "papel":
        print("Ganaste")
if movimiento_usuario == movimiento_ia:
    print("Empate")
