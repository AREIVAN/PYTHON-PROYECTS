import requests

URL = "https://pokeapi.co/api/v2/pokemon/"
pokemon = input("Escribe el nombre el pokemon: ")
respuesta = requests.get(URL + pokemon)
datos = respuesta.json()

print(f"-----Movimientos de{pokemon}:-----")
for move in datos["moves"]:
    print(move["move"]["name"])

print(f"-----tipos de{pokemon}:-----")
for type in datos["types"]:
    print(type["type"]["name"])
