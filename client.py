import socketio
import platform
import subprocess

socket = socketio.Client()

socket.connect('http://84db0bdc1324.ngrok.io')
print('Halo, silahkan menggunakan bot @proyekTOS_bot dengan command /start')
print('Silahkan masukkan token yang didapat dari bot dengan command /token: '),
token = input()
socket.emit('afterInput', token)
system = platform.system()
@socket.on('inputted')
def inputted(data):
    print('Device terdaftar dengan token', data, 'silahkan gunakan command yang tersedia di bot')

@socket.event
def connect():
    socket.emit('source', 'client')

#check system platform
@socket.on('client_checkSystem')
def sysCheck(data):
    msg = 'Sistem PC / Laptop anda adalah: '+str(system)+' '+str(platform.machine())
    socket.emit('client_systemChecked', {'id' : data['id'], 'room': data['room'], 'message' : msg})

#launch Firefox
@socket.on('client_launchFirefox')
def client_launchFirefox(data):
    if system.lower() == 'windows':
        subprocess.call(['C:\\Program Files\\Mozilla Firefox\\firefox.exe'])
    elif system.lower() == 'linux':
        subprocess.call(['firefox'])
    msg = 'Firefox telah dijalankan'
    socket.emit('client_firefoxLaunched', {'id' : data['id'], 'room': data['room'], 'message' : msg})

#launch Chrome
@socket.on('client_launchChrome')
def client_launchChrome(data):
    if system.lower() == 'windows':
        subprocess.call(['C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'])
    elif system.lower() == 'linux':
        subprocess.call(['chrome'])
    msg = 'Chrome telah dijalankan'
    socket.emit('client_chromeLaunched', {'id' : data['id'], 'room': data['room'], 'message' : msg})

#shutdown
@socket.on('client_turnOff')
def client_turnOff(data):
    if system.lower() == 'windows':
        subprocess.call(['shutdown -s'])
    elif system.lower() == 'linux':
        subprocess.call(['shutdown now'])
    msg = 'PC / Laptop anda telah menerima command shutdown'
    socket.emit('client_turnedOff', {'id' : data['id'], 'room': data['room'], 'message' : msg})

#restart
@socket.on('client_restart')
def client_restart(data):
    if system.lower() == 'windows':
        subprocess.call(['shutdown -r'])
    elif system.lower() == 'linux':
        subprocess.call(['reboot'])
    msg = 'PC / Laptop anda telah menerima command restart'
    socket.emit('client_restarted', {'id' : data['id'], 'room': data['room'], 'message' : msg})