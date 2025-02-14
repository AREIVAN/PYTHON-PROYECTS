import socket

ip = input("introduce la direccion IP a escanear:")

for puerto in range(1, 35):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)

    resultado = sock.connect_ex((ip, puerto))

    if resultado == 0:
        print("puerto abierto: ", puerto)
        sock.close()
    else:
        print("puerto cerrado: ", puerto)
