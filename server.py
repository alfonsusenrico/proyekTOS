import eventlet
import socketio

socket = socketio.Server()
app = socketio.WSGIApp(socket)

#list object
users = []
allDevice = []

class Device:
    user_id = ''
    token = ''
    def __init__(self, id, token):
        self.user_id = id
        self.token = token

class User:
    user_id = ''
    deviceCount = 0
    devices = []
    activeDevice = ''
    def __init__(self, id):
        self.user_id = id
        self.deviceCount = 0
    def addDevice(self, device):
        self.devices.append(device)
        self.deviceCount += 1
        self.activeDevice = device.token

#BOT
@socket.event
def connect(sid, data):
    print('Socket connected')

@socket.on('addUser')
def addUser(sid, data):
    users.append(User(data))
    socket.emit('afterData', data)

@socket.on('tokenGenerated')
def setToken(sid, data):
    for user in users:
        if user.user_id == data['id']:
            user.addDevice(Device(data['id'], data['token']))
            allDevice.append(Device(data['id'], data['token']))
            socket.enter_room(sid, str(data['token']))
            #socket.emit('afterToken', data.token)
            break

#CLIENT
#inputData
@socket.on('afterInput')
def afterInput(sid, data):
    rm = str(data)
    socket.enter_room(sid, rm)
    socket.emit('inputted', data, room=rm)

#CheckSystem
@socket.on('checkSystem')
def checkSystem(sid, data):
    for user in users:
        if user.user_id == data:
            rm = str(user.activeDevice)
            socket.emit('client_checkSystem', {'id': data, 'room': rm}, room=rm)
        break
@socket.on('client_systemChecked')
def system(sid, data):
    socket.emit('systemChecked', data, room=data['room'])

#RunApps(Firefox)
@socket.on('launchFirefox')
def launchFirefox(sid, data):
    for user in users:
        if user.user_id == data:
            rm = str(user.activeDevice)
            socket.emit('client_launchFirefox', {'id': data, 'room': rm}, room=rm)
        break
@socket.on('client_firefoxLaunched')
def firefoxLaunched(sid, data):
    socket.emit('firefoxLaunched', data, room=data['room'])

#RunApps(Chrome)
@socket.on('launchChrome')
def launchChrome(sid, data):
    for user in users:
        if user.user_id == data:
            rm = str(user.activeDevice)
            socket.emit('client_launchChrome', {'id': data, 'room': rm}, room=rm)
        break
@socket.on('client_chromeLaunched')
def chromeLaunched(sid, data):
    socket.emit('chromeLaunched', data, room=data['room'])

#shutdown
@socket.on('turnOFf')
def turnOff(sid, data):
    for user in users:
        if user.user_id == data:
            rm = str(user.activeDevice)
            socket.emit('client_turnOff', {'id': data, 'room': rm}, room=rm)
        break
@socket.on('client_turnedOff')
def turnedOff(sid, data):
    socket.emit('turnedOff', data, room=data['room'])

#restart
@socket.on('restart')
def restart(sid, data):
    for user in users:
        if user.user_id == data:
            rm = str(user.activeDevice)
            socket.emit('client_restart', {'id': data, 'room': rm}, room=rm)
        break
@socket.on('client_restarted')
def restarted(sid, data):
    socket.emit('restarted', data, room=data['room'])

#DEBUG / CHECKING
@socket.on('test')
def tes(sid):
    print(users)
    print(allDevice)
    for item in users:
        print(item.user_id)
        print(item.deviceCount)
        print(item.activeDevice)
eventlet.wsgi.server(eventlet.listen(('',5000)), app)