import socket
import threading
import pickle
import curses
from rga import RGA, Nodo

class ClienteEditor:
    def __init__(self, nombre):
        self.nombre = nombre
        self.rga = RGA()
        self.cursor_index = 0
        self.cursor_target_x = 0  # Moverse ↑ ↓
        self.cursor_nodo_id = None  
        self.stdscr = None

        ip_servidor = "172.19.80.1"
        print(f"[INFO] Conectando al servidor en {ip_servidor}:5555")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.sock.connect((ip_servidor, 5555))
            longitud = int.from_bytes(self.sock.recv(4), 'big')
            estado = b""
            while len(estado) < longitud:
                estado += self.sock.recv(longitud - len(estado))
            mensaje = pickle.loads(estado)
            if mensaje["tipo"] == "estado_inicial":
                for id, valor, prev_id, visible in mensaje["ops"]:
                    self.rga.aplicar_operacion(id, valor, prev_id, visible)
            print("[INFO] Conexión establecida con el servidor.")
        except Exception as e:
            print(f"[ERROR] No se pudo conectar al servidor: {e}")
            exit(1)

        threading.Thread(target=self.escuchar, daemon=True).start()
        curses.wrapper(self.bucle_editor)

    def enviar_operacion(self, tipo, id, valor=None, prev_id=None):
        op = {
            "autor": self.nombre,
            "tipo": tipo,
            "id": id,
            "valor": valor,
            "prev_id": prev_id
        }
        try:
            self.sock.send(pickle.dumps(op))
        except BrokenPipeError:
            print("[ERROR] Conexión perdida con el servidor.")
            exit(1)

    def escuchar(self):
        while True:
            try:
                data = self.sock.recv(4096)
                if not data:
                    break
                op = pickle.loads(data)
                if op["autor"] != self.nombre:
                    if op["tipo"] == "insertar":
                        self.rga.aplicar_operacion(op["id"], op["valor"], op["prev_id"], True)
                    elif op["tipo"] == "borrar":
                        self.rga.aplicar_operacion(op["id"], None, None, False)
                    self.ajustar_cursor()
                    self.refrescar_pantalla()
            except:
                break

    def bucle_editor(self, stdscr):
        curses.curs_set(1)
        self.stdscr = stdscr
        stdscr.nodelay(False)
        stdscr.clear()

        while True:
            self.refrescar_pantalla()
            ch = stdscr.getch()

            self.nodos_visibles = [nid for nid in self.rga.orden if self.rga.nodos[nid].visible]
            
            # Actualizar el cursor
            if ch == curses.KEY_LEFT and self.cursor_index > 0: 
                self.cursor_index -= 1
                self.cursor_target_x = self._get_cursor_x()
            elif ch == curses.KEY_RIGHT and self.cursor_index < len(self.nodos_visibles):   
                self.cursor_index += 1
                self.cursor_target_x = self._get_cursor_x()
            elif ch == curses.KEY_UP:   
                self._mover_cursor_vertical(-1)
            elif ch == curses.KEY_DOWN:
                self._mover_cursor_vertical(1)
            elif ch in (curses.KEY_BACKSPACE, 127): 
                if self.cursor_index > 0 and self.nodos_visibles:
                    borrar_id = self.nodos_visibles[self.cursor_index - 1]
                    self.rga.aplicar_operacion(borrar_id, None, None, False)
                    self.enviar_operacion("borrar", borrar_id)
                    self.cursor_index -= 1

            elif ch == 27:  # Escape
                break
            elif ch == 10:  # Enter
                # Insertar un salto de línea
                char = '\n'
                prev_id = self.nodos_visibles[self.cursor_index - 1] if self.cursor_index > 0 else None
                nuevo_id = self.rga.insert_after(prev_id, char)
                self.enviar_operacion("insertar", nuevo_id, char, prev_id)
                self.cursor_index += 1
            elif 32 <= ch <= 126: # Caracteres imprimibles
                char = chr(ch)
                prev_id = self.nodos_visibles[self.cursor_index - 1] if self.cursor_index > 0 else None
                nuevo_id = self.rga.insert_after(prev_id, char)
                self.enviar_operacion("insertar", nuevo_id, char, prev_id)
                self.cursor_index += 1

            self.nodos_visibles = [nid for nid in self.rga.orden if self.rga.nodos[nid].visible]
            self.cursor_nodo_id = self.nodos_visibles[self.cursor_index - 1] if self.cursor_index > 0 else None

    def ajustar_cursor(self):
        self.nodos_visibles = [nid for nid in self.rga.orden if self.rga.nodos[nid].visible]
        self.cursor_index = min(self.cursor_index, len(self.nodos_visibles))
        if self.cursor_index < 0:
            self.cursor_index = 0
        self.cursor_nodo_id = self.nodos_visibles[self.cursor_index - 1] if self.cursor_index > 0 else None

    def _get_cursor_x(self):
        texto = ''.join(self.rga.value())
        x = 0
        index = 0
        for c in texto:
            if index == self.cursor_index:
                return x
            if c == '\n':
                x = 0
            else:
                x += 1
            index += 1
        return x

    def refrescar_pantalla(self):
        self.nodos_visibles = [nid for nid in self.rga.orden if self.rga.nodos[nid].visible]

        if self.stdscr:
            self.stdscr.clear()
            texto = ''.join(self.rga.value())

            # Dibujar el texto línea por línea
            y, x = 0, 0
            cursor_y, cursor_x = 0, 0
            index = 0
            for c in texto:
                if index == self.cursor_index:
                    cursor_y, cursor_x = y, x
                if c == '\n':
                    y += 1
                    x = 0
                else:
                    try:
                        self.stdscr.addch(y, x, c)
                    except curses.error:
                        pass  # Ignora si está fuera de la pantalla
                    x += 1
                index += 1

            # Si estamos al final del texto, actualiza cursor
            if self.cursor_index == len(texto):
                cursor_y, cursor_x = y, x

            self.stdscr.move(cursor_y, cursor_x)
            self.stdscr.refresh()


    def _mover_cursor_vertical(self, direccion):
        texto = ''.join(self.rga.value())
        lineas = texto.split('\n')

        index = 0
        y_actual = 0
        for i, linea in enumerate(lineas):
            if index + len(linea) >= self.cursor_index:
                y_actual = i
                break
            index += len(linea) + 1

        y_destino = y_actual + direccion
        if 0 <= y_destino < len(lineas):
            nueva_linea = lineas[y_destino]
            x = min(len(nueva_linea), self.cursor_target_x)
            nuevo_index = sum(len(lineas[i]) + 1 for i in range(y_destino)) + x
            self.nodos_visibles = [nid for nid in self.rga.orden if self.rga.nodos[nid].visible]
            self.cursor_index = min(nuevo_index, len(self.nodos_visibles))

if __name__ == "__main__":
    nombre = input("Nombre de usuario: ")
    ClienteEditor(nombre)
