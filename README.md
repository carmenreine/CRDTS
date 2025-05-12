# 📝 EDITORES COLABORATIVOS CON CRDTS

Este repositorio contiene **dos editores de texto colaborativos** que permiten la edición en tiempo real por múltiples usuarios sin conflictos, utilizando **CRDTs (Conflict-free Replicated Data Types)**:

- Un **editor en consola** implementado en Python desde cero con el algoritmo **RGA (Replicated Growable Array)**.
- Un **editor web** basado en la librería **Yjs** con una interfaz creada usando  **Quill** y sincronización por WebSockets.

Estas implementaciones forman parte de un trabajo académico sobre **sistemas distribuidos y CRDTs**.

---

## 🖥️ EDITOR COLABORATIVO EN CONSOLA (Python + RGA)

### Características

- Edición colaborativa en tiempo real desde la terminal
- CRDT RGA (implementado desde cero)
- Sincronización automática mediante sockets TCP
- Interfaz basada en `curses` (navegable con teclado)
- Soporte para múltiples usuarios conectados simultáneamente
- Manejo de saltos de línea

### Tecnologías usadas

- Python 3
- `socket`, `threading` y `pickle` para concurrencia y red
- `curses` para la interfaz en consola
- CRDT RGA propio (estructura distribuida sin conflictos)

### Estructura de archivos

- `servidor_sync.py` – Servidor que mantiene el estado global y distribuye cambios
- `cliente_editor_saltos.py` – Cliente que muestra el editor en consola
- `rga.py` – Implementación del algoritmo RGA (CRDT)

### Entorno virtual (opcional pero recomendado)

Para evitar conflictos con otras instalaciones de Python y mantener organizadas las dependencias:

1. Crear un entorno virtual (solo la primera vez)

  ```bash
   python3 -m venv venv
   ```
2. Activarlo

**En Windows:**

  ```bash
   venv\Scripts\activate
   ```

**En Linux/macOS:**

  ```bash
   source venv/bin/activate
   ```

### Cómo ejecutar

1. Clona el repositorio.
2. Inicia el servidor:

   ```bash
   python3 servidor_sync.py
   ```
3. En otra(s) terminal(es), inicia uno o más clientes:
   ```bash
   python3 cliente_editor_saltos.py
   ```
4. Introduce un nombre de usuario.
5. Comienza a escribir.

### Controles del cliente

- Flechas ← → ↑ ↓ para moverse por el texto
- Letras y símbolos para escribir
- ENTER para salto de línea
- Backspace para borrar
- ESC para salir

### Limitaciones actuales

- El cursor puede desincronizarse tras ciertos borrados
- No hay persistencia (se pierde al cerrar)
- No hay control de usuarios ni reconexión automática

### Mejoras futuras

- Persistencia del documento (ej. con PostgreSQL)
- Soporte para múltiples sesiones
- Control de versiones y permisos
- Reentrada tras desconexión inesperada

---

## 🌐 EDITOR COLABORATIVO EN WEB (Yjs + Quill + WebSockets)

### Características

- Edición en tiempo real en el navegador
- Interfaz rica con formato (negrita, cursiva, enlaces)
- CRDT Yjs para sincronización automática sin conflictos
- Comunicación mediante WebSockets
- Multiplataforma (varias pestañas o dispositivos)

### Tecnologías usadas

- Node.js
- WebSockets (`ws`)
- Yjs (CRDT)
- Quill (editor WYSIWYG)
- HTML5 y JavaScript (ECMAScript Modules)

### Estructura de archivos

- `server.js` – Servidor WebSocket para sincronización
- `index.html` – Interfaz del editor + integración con Yjs
- `package.json` – Dependencias del proyecto

### Cómo ejecutar

1. Instala las dependencias:
   ```bash
   npm install
   ```
2. Inicia el servidor:
   ```bash
   npm start
   ```
3. Abre `index.html` en dos pestañas usando Live Server o un servidor local.
4. Escribe en una pestaña y observa los cambios en la otra.

### Funcionamiento

Cada cliente mantiene su propia instancia del documento Yjs. Los cambios se sincronizan con el servidor WebSocket, que los reenvía a los demás clientes. Quill proporciona la interfaz visual bidireccional.

### Limitaciones actuales

- No hay persistencia del contenido
- Todos los usuarios están en la misma sala de edición
- No hay gestión de usuarios ni control de versiones

### Mejoras futuras

- Soporte para múltiples documentos o salas
- Guardado del contenido en base de datos
- Autenticación y control de permisos
- Historial de versiones y actividad por usuario

---

## ✍️ Autoras

Este proyecto fue desarrollado por **Paula Segura Manzanares** y **Carmen Reine Rueda** como parte de una práctica educativa para explorar los fundamentos y aplicaciones de los CRDTs en entornos distribuidos.
