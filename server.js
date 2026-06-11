const express = require('express')
const { createServer } = require('http')
const { Server } = require('socket.io')
const app = express()
const server = createServer(app)
const io = new Server(server, {
  cors: { origin: '*' },
  maxHttpBufferSize: 50 * 1024 * 1024 // 50MB for large model files
})
const { v4: uuidV4 } = require('uuid')

/** roomId -> Map<userId, socketId> */
const rooms = new Map()

function getRoom(roomId) {
  if (!rooms.has(roomId)) {
    rooms.set(roomId, new Map())
  }
  return rooms.get(roomId)
}

function emitToUser(roomId, targetUserId, event, payload) {
  const room = rooms.get(roomId)
  if (!room) return
  const socketId = room.get(targetUserId)
  if (socketId) {
    io.to(socketId).emit(event, payload)
  }
}

function removeUser(roomId, userId) {
  const room = rooms.get(roomId)
  if (!room) return
  room.delete(userId)
  if (room.size === 0) {
    rooms.delete(roomId)
  }
}

app.set('view engine', 'ejs')
app.use(express.static('public'))

app.get('/', (req, res) => {
  res.redirect(`/${uuidV4()}`)
})

app.get('/:room', (req, res) => {
  res.render('room', { roomId: req.params.room })
})

io.on('connection', socket => {
  let joinedRoomId = null
  let joinedUserId = null

  socket.on('join-room', (roomId, userId) => {
    joinedRoomId = roomId
    joinedUserId = userId

    socket.join(roomId)
    const room = getRoom(roomId)

    room.forEach((existingSocketId, existingUserId) => {
      if (existingUserId !== userId) {
        socket.emit('user-connected', existingUserId)
      }
    })

    room.set(userId, socket.id)
    socket.to(roomId).emit('user-connected', userId)
  })

  socket.on('webrtc-offer', payload => {
    if (!joinedRoomId || !joinedUserId) return
    emitToUser(joinedRoomId, payload.targetId, 'webrtc-offer', {
      sdp: payload.sdp,
      fromId: joinedUserId
    })
  })

  socket.on('webrtc-answer', payload => {
    if (!joinedRoomId || !joinedUserId) return
    emitToUser(joinedRoomId, payload.targetId, 'webrtc-answer', {
      sdp: payload.sdp,
      fromId: joinedUserId
    })
  })

  socket.on('webrtc-ice-candidate', payload => {
    if (!joinedRoomId || !joinedUserId) return
    emitToUser(joinedRoomId, payload.targetId, 'webrtc-ice-candidate', {
      candidate: payload.candidate,
      fromId: joinedUserId
    })
  })

  socket.on('drawing-data', data => {
    if (!joinedRoomId) return
    socket.to(joinedRoomId).emit('drawing-data', data)
  })

  socket.on('model-data-chunk', payload => {
    if (!joinedRoomId || !joinedUserId) return
    console.log(`[model-data-chunk] from ${joinedUserId}, chunk ${payload.chunkIndex}/${payload.totalChunks}, transferId: ${payload.transferId}`)
    socket.to(joinedRoomId).emit('model-data-chunk', payload)
  })

  socket.on('model-data-complete', payload => {
    if (!joinedRoomId || !joinedUserId) return
    console.log(`[model-data-complete] from ${joinedUserId}, transferId: ${payload.transferId}, type: ${payload.type}`)
    socket.to(joinedRoomId).emit('model-data-complete', payload)
  })

  socket.on('disconnect', () => {
    if (joinedRoomId && joinedUserId) {
      removeUser(joinedRoomId, joinedUserId)
      socket.to(joinedRoomId).emit('user-disconnected', joinedUserId)
    }
  })
})

const PORT = process.env.PORT || 3000
server.listen(PORT, () => {
  console.log(`Signaling server listening on port ${PORT}`)
})
