# Editor Colaborativo en Consola con Python y CRDT (RGA)

Este proyecto implementa un editor de texto colaborativo en consola, desarrollado en Python, que permite a múltiples usuarios editar el mismo documento en tiempo real mediante un CRDT del tipo RGA (Replicated Growable Array). La comunicación se realiza mediante sockets TCP, y la interfaz de usuario se muestra en consola con la biblioteca `curses`.

## Características

- Edición colaborativa en tiempo real
- Sincronización sin conflictos mediante CRDT (RGA)
- Interfaz interactiva en consola
- Soporte para múltiples usuarios conectados simultáneamente
- Manejo de saltos de línea
- Sin servidor central que coordine los cambios: los conflictos se resuelven automáticamente

## Tecnologías usadas

- Python 3
- `socket`, `threading` y `pickle` para red y concurrencia
- `curses` para la interfaz de texto
- CRDT RGA implementado desde cero

## Estructura de archivos

- `servidor.py` – Lógica del servidor que mantiene el estado global del documento y distribuye las operaciones.
- `cliente_editor.py` – Cliente en consola que permite editar el documento de forma colaborativa.
- `rga.py` – Implementación del CRDT RGA (estructura de datos distribuida que permite inserciones y borrados sin conflicto).

## Cómo ejecutar

1. Clona este repositorio o descarga los archivos.
2. En una terminal, inicia el servidor:

   ```bash
   python3 servidor.py
   ```

3. En otra(s) terminal(es), inicia uno o más clientes:

   ```bash
   python3 cliente_editor.py
   ```

4. Introduce un nombre de usuario cuando se te solicite.
5. Empieza a escribir. Todos los clientes verán los cambios en tiempo real.

## Entorno virtual (opcional pero recomendado)

Para evitar conflictos con otras instalaciones de Python y mantener organizadas las dependencias:

1. Crear un entorno virtual (solo la primera vez)

  ```bash
   python3 -m venv venv
   ```
2. Activarlo
### En Windows:

  ```bash
   venv\Scripts\activate
   ```

### En Linux/macOS:

  ```bash
   source venv/bin/activate
   ```

## Controles del cliente

- Flechas ← → ↑ ↓ para moverse por el texto
- Teclas normales para escribir
- Backspace para borrar
- ENTER para insertar salto de línea
- ESC para salir

## Limitaciones actuales

- El cursor puede comportarse de forma descoordinada tras ciertas operaciones de borrado.
- No hay persistencia de datos (todo se pierde al cerrar).
- No hay control de usuarios ni historial de versiones.
- La reconexión automática aún no está implementada.

## Mejoras futuras

- Persistencia con base de datos (e.g., PostgreSQL)
- Gestión de múltiples documentos y sesiones
- Control de versiones y permisos
- Visualización de actividad remota por usuario
- Reconexión tras desconexión inesperada





# Editor de Texto Colaborativo en Web con Yjs y Quill (Node.js + WebSockets)
Este proyecto implementa un editor de texto colaborativo en navegador que permite a múltiples usuarios editar el mismo documento en tiempo real. Utiliza la librería CRDT Yjs para sincronizar el contenido entre los clientes y el editor de texto Quill para la interfaz. La comunicación entre clientes se realiza mediante WebSockets sobre un servidor Node.js.

# Características
1. Edición en tiempo real entre múltiples pestañas o dispositivos
2. Sincronización automática sin conflictos gracias a Yjs (CRDT)
3. Interfaz rica con soporte para formato (negrita, cursiva, enlaces)
4. Comunicación mediante WebSockets (sin necesidad de backend complejo)
5. Arquitectura distribuida basada en documentos compartidos

# Tecnologías usadas
- Node.js
- Yjs (CRDT)
- WebSockets (ws)
- Quill (editor WYSIWYG)
- HTML5 y ECMAScript Modules

# Estructura de archivos
- server.js 
Servidor WebSocket que sincroniza los cambios del documento entre todos los clientes conectados.
- index.html 
Interfaz de usuario con el editor Quill y la integración con Yjs.
- package.json 
Archivo de configuración con las dependencias del servidor.

# Cómo ejecutar
1. Instala las dependencias en la raíz del proyecto:
'npm install'
2. Inicia el servidor WebSocket:
'npm start'
Esto ejecutará server.js en el puerto 1234
3. Abre index.html en dos pestañas del navegador (usando Live Server en VS Code o un servidor local).
4. Escribe en una pestaña y observa cómo los cambios aparecen en tiempo real en la otra.

# Funcionamiento interno
El documento compartido se gestiona con Yjs, que garantiza una sincronización sin conflictos incluso en presencia de ediciones concurrentes.

Cada cliente mantiene su propia instancia del documento y comunica los cambios mediante WebSocket al servidor.

El servidor retransmite los cambios a todos los demás clientes conectados.

Quill actúa como la interfaz visual del documento, y sus cambios se sincronizan bidireccionalmente con Yjs.

# Limitaciones actuales
- El contenido no se guarda en disco (no hay persistencia).
- Todos los usuarios colaboran en una única sala (demo-room).
- No hay control de versiones ni gestión de usuarios.

# Mejoras futuras
- Soporte para múltiples documentos o salas
- Persistencia del contenido mediante base de datos
- Gestión de usuarios y permisos
- Historial de cambios y versiones



## Autor

Este proyecto fue desarrollado como parte de una práctica educativa para explorar el funcionamiento interno de los CRDTs y la colaboración en sistemas distribuidos.