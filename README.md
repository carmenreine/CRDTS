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

## Autor

Este proyecto fue desarrollado como parte de una práctica educativa para explorar el funcionamiento interno de los CRDTs y la colaboración en sistemas distribuidos.
