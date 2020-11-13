import socketio
import datetime
from telegram.ext import Updater
from telegram.ext import CommandHandler

#bot vars
TOKEN = '1452749128:AAFyUCu3p6aUmMuLhWq1-n9v0XsP12u62kU'
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

#socket vars
socket = socketio.Client()
socket.connect('http://1ce0ea9ea35c.ngrok.io')

#start
def start(update, context):
    socket.emit('addUser', str(update.effective_chat.id))
    @socket.on('afterData')
    def afterData(data):
        context.bot.send_message(chat_id=data, text="Silahkan gunakan command /token untuk mendapatkan token device anda")
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


#check system
def checkSystem(update, context):
    socket.emit('checkSystem', str(update.effective_chat.id))
    @socket.on('systemChecked')
    def systemChecked(data):
        context.bot.send_message(chat_id=data['id'], text=data['message'])
start_handler = CommandHandler('system', checkSystem)
dispatcher.add_handler(start_handler)

#launch Firefox
def launchFirefox(update, context):
    socket.emit('launchFirefox', str(update.effective_chat.id))
    @socket.on('firefoxLaunched')
    def firefoxLaunched(data):
        context.bot.send_message(chat_id=data['id'], text=data['message'])
start_handler = CommandHandler('firefox', launchFirefox)
dispatcher.add_handler(start_handler)

#launch Chrome
def launchChrome(update, context):
    socket.emit('launchChrome', str(update.effective_chat.id))
    @socket.on('chromeLaunched')
    def chromeLaunched(data):
        context.bot.send_message(chat_id=data['id'], text=data['message'])
start_handler = CommandHandler('chrome', launchChrome)
dispatcher.add_handler(start_handler)

#shutdown
def turnOff(update, context):
    socket.emit('turnOff', str(update.effective_chat.id))
    @socket.on('turnedOff')
    def turnedOff(data):
        context.bot.send_message(chat_id=data['id'], text=data['message'])
start_handler = CommandHandler('shutdown', turnOff)
dispatcher.add_handler(start_handler)

#restart
def restart(update, context):
    socket.emit('restart', str(update.effective_chat.id))
    @socket.on('restarted')
    def restarted(data):
        context.bot.send_message(chat_id=data['id'], text=data['message'])
start_handler = CommandHandler('restart', restart)
dispatcher.add_handler(start_handler)

#DEBUG
def tes(update, context):
    socket.emit('test')
start_handler = CommandHandler('test', tes)
dispatcher.add_handler(start_handler)

#creator
#def creator(update, context):
#    context.bot.send_message(chat_id=update.effective_chat.id, text="1. Alfonsus Enrico / C14180067 \n2. Vito Varian L. / C14180095")
#dispatcher.add_handler(CommandHandler('creator', creator))

#generate token
def generateToken(update, context):
    date = datetime.datetime.now()
    token = str(update.effective_chat.id)+str(date.day)+str(date.month)+str(date.year)+str(date.hour)+str(date.minute)+str(date.second)
    data = {
        'token' : token,
        'id' : str(update.effective_chat.id)
    }
    socket.emit('tokenGenerated', data)
    msg = 'Token anda adalah ' + token
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
dispatcher.add_handler(CommandHandler('token', generateToken))

@socket.event
def connect():
    socket.emit('source', 'bot')

#start bot
updater.start_polling()