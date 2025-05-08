import socket
import threading
import pickle
from rga import RGA

usuarios_conectados = []
rga_global = RGA()

def manejar_usuario(conn, addr):
    print(f"[SERVIDOR] Nueva conexión desde {addr}")
    usuarios_conectados.append(conn)
    try:
        # Enviar estado inicial del RGA con longitud explícita
        estado_inicial = rga_global.get_ops()
        estado_serializado = pickle.dumps({
            "tipo": "estado_inicial",
            "ops": estado_inicial
        })
        conn.sendall(len(estado_serializado).to_bytes(4, 'big') + estado_serializado)

        while True:
            data = conn.recv(4096)
            if not data:
                break

            op = pickle.loads(data)

            if op["tipo"] == "insertar":
                rga_global.aplicar_operacion(op["id"], op["valor"], op["prev_id"], True)
            elif op["tipo"] == "borrar":
                rga_global.aplicar_operacion(op["id"], None, None, False)


            for usuario in usuarios_conectados:
                if usuario != conn:
                    try:
                        usuario.send(data)
                    except:
                        pass
    except:
        pass
    finally:
        print(f"[SERVIDOR] Usuario {addr} desconectado.")
        usuarios_conectados.remove(conn)
        conn.close()

def iniciar_servidor():
    host = '0.0.0.0'
    puerto = 5555

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, puerto))
    server.listen()

    print(f"[SERVIDOR] Escuchando en {host}:{puerto}...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=manejar_usuario, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    iniciar_servidor()
