"Fonte de referencia: https://blog.miguelgrinberg.com/post/easy-websockets-with-flask-and-gevent"
"https://learn.pimoroni.com"
"http://community.thingspeak.com/tutorials/update-a-thingspeak-channel-using-mqtt-on-a-raspberry-pi"
"https://www.mathworks.com/help/thingspeak/mqtt-basics.html#zmw57dd0e21035"

from RB3Publish import RB3Publish
from RB3Subscribe import RB3Subscribe
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room,close_room, rooms, disconnect
from frdm import kl25z

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

publish = RB3Publish()
subscribe = RB3Subscribe()
tracker = kl25z()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
threadRabbitMQ = None

def task_RabbitMQ():    
    """Thread para inicilizacao do subscribe e publish e envio periodico dos dados de telemetria"""

    tracker.init()

    while True:
        tracker.publishTLM()
        socketio.sleep(1) 

def background_thread():    
    """Thread para inicilizacao do subscribe e publish e envio periodico dos dados de telemetria"""

    count = 0

    #Inicia o publicador
    publish.start()

    #inicia o consumidor
    #subscribe.init()

    while True:
        count += 1
        #print("Iniciando a leitura do canal no ThingSpeak")
        #subscribe.readValues()
        sendAllDataRB3(count)
        #print("Leitura do ThingSpeak finalizada e envianda para frontend")

        socketio.sleep(1)

def sendAllDataRB3(count):

    socketio.emit('onUpdateTLM',
                 {'temperatura':  str(subscribe.getCPUtemperature()) ,
                  'humidade':  str(subscribe.getHumidity()) ,
                  'memoria': str(subscribe.getMemory()),
                  'disco': str(subscribe.getDisk()),
                  'cpu': str(subscribe.getCPU()),
                  'pressao': str(subscribe.getPressure()),
                  'count':count},
                   namespace='/test')    
    
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('close_room', namespace='/test')
def close(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',        
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])


@socketio.on('my_room_event', namespace='/test')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()

@socketio.on('my_ping', namespace='/test')
def ping_pong():
    emit('my_pong')

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my_response', {'data': 'Connected', 'count': 0})

    global threadRabbitMQ 
    if threadRabbitMQ  is None:
        threadRabbitMQ  = socketio.start_background_task(target=task_RabbitMQ)
    print("Thread RabbitMQ iniciada !")

    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)
    print("Thread ThingSpeak iniciada !")

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)

@app.route('/pressao')
def pressao():    
    return str(subscribe.getPressure()) + ' %'

@app.route('/humidade')
def humidade():
    return str(subscribe.getHumidity()) + ' %'

@app.route('/temperatura')
def tempearature():
    return str(subscribe.getCPUtemperature()) + ' Celsus'
    
@app.route('/cpu')
def cpu():
    return str(subscribe.getCPU()) + ' %'

@app.route('/memory')
def memory():
    return str(subscribe.getMemory()) +' MB'

@app.route('/disk')
def disk():
    return str(subscribe.getDisk()) +' GB'

if __name__ == '__main__':
    app.run(
        debug=True,
        host= '192.168.42.1',
        port=5000
    )
    socketio.run(app, debug=True)

