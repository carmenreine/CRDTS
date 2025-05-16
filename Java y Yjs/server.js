import http from 'http' // Importa el módulo HTTP nativo de Node.js
import * as Y from 'yjs' // Importa todas las funciones del paquete Yjs (CRDT para colaboración en tiempo real)
import { WebSocketServer } from 'ws' // Importa la clase WebSocketServer del paquete 'ws'

const docs = new Map() // Crea un mapa para almacenar los documentos Yjs por sala

function getYDoc(room) { // Función para obtener el documento de una sala específica
  if (!docs.has(room)) { // Si no existe el documento para esa sala...
    docs.set(room, new Y.Doc()) // ...se crea un nuevo documento Yjs y se guarda en el mapa
  }
  return docs.get(room) // Devuelve el documento correspondiente a la sala
}

const server = http.createServer() // Crea un servidor HTTP básico (no maneja rutas, solo sirve como base para WebSocket)
const wss = new WebSocketServer({ server }) // Crea un servidor WebSocket montado sobre el servidor HTTP

wss.on('connection', (ws) => { // Se ejecuta cuando un cliente se conecta al WebSocket
  const room = 'demo-room' // Nombre de la sala (en este caso es fijo)
  const doc = getYDoc(room) // Obtiene o crea el documento Yjs para esa sala

  const initialUpdate = Y.encodeStateAsUpdate(doc) // Codifica el estado actual del documento como un binario
  ws.send(initialUpdate) // Envía ese estado inicial al cliente que se acaba de conectar

  ws.on('message', (message) => { // Se ejecuta cuando el cliente envía un mensaje
    const update = new Uint8Array(message) // Convierte el mensaje a un array de bytes
    Y.applyUpdate(doc, update) // Aplica la actualización al documento Yjs

    // Reenvía la actualización a los demás clientes conectados (excepto al que la envió)
    wss.clients.forEach(client => {
      if (client !== ws && client.readyState === ws.OPEN) { // Si el cliente está conectado y no es el emisor...
        client.send(update) // ...se le envía la actualización
      }
    })
  })

  ws.on('close', () => { // Se ejecuta cuando el cliente se desconecta
    console.log('Cliente desconectado') // Muestra un mensaje por consola
  })
})

server.listen(1234, () => { // Inicia el servidor en el puerto 1234
  console.log('Servidor WebSocket en puerto 1234') // Muestra mensaje en consola al iniciar
})

