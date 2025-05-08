import uuid

class Nodo:
    def __init__(self, valor, prev_id=None, visible=True):
        self.id = str(uuid.uuid4())
        self.valor = valor
        self.prev_id = prev_id  # ID del nodo anterior
        self.visible = visible

class RGA:
    def __init__(self):
        self.nodos = {}  # id -> Nodo
        self.orden = []  # ids en orden reconstruido

    def insert_after(self, prev_id, valor):
        nuevo = Nodo(valor, prev_id)
        self.nodos[nuevo.id] = nuevo
        self._reconstruir_orden()
        return nuevo.id

    def delete(self, nodo_id):
        if nodo_id in self.nodos:
            self.nodos[nodo_id].visible = False

    def value(self):
        return [self.nodos[nid].valor for nid in self.orden if self.nodos[nid].visible]

    def _reconstruir_orden(self):
        grafo = {}
        for nodo in self.nodos.values():
            grafo.setdefault(nodo.prev_id, []).append(nodo.id)

        # ORDENAMOS los hijos de cada nodo por ID para consistencia entre nodos
        for hijos in grafo.values():
            hijos.sort()

        self.orden = []
        self._dfs(None, grafo)

    def _dfs(self, curr, grafo):
        for siguiente in grafo.get(curr, []):
            self.orden.append(siguiente)
            self._dfs(siguiente, grafo)

    def get_ops(self):
        return [(n.id, n.valor, n.prev_id, n.visible) for n in self.nodos.values()]

    def aplicar_operacion(self, nodo_id, valor, prev_id, visible):
        if nodo_id not in self.nodos:
            nodo = Nodo(valor, prev_id, visible)
            nodo.id = nodo_id
            self.nodos[nodo_id] = nodo
        else:
            self.nodos[nodo_id].visible = visible  # actualización si ya existe
        self._reconstruir_orden()
