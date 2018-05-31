from bson.json_util import dumps, loads, ObjectId, CANONICAL_JSON_OPTIONS
from gevent import monkey
import json
import threading
from threading import Lock
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import paho.mqtt.client as mqtt
from threading import Thread
 
# Set this variable to "threading", "eventlet" or "gevent" to test the 
app = Flask(__name__)
app.debug = True
mqtt_thread = None
socketio = SocketIO(app)


class MQTT_Thread(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.stop = False

	def run(self):
		while not self.stop and client.loop_forever() == 0:
			pass
print ("MQTT Thread terminado")

#----------------MQTT---------------#

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("Centro/Toscana/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    jsonRequest=loads(msg.payload.decode('utf-8'))
    event = None
    if 'emergency' in jsonRequest:
        jsonRequest=jsonRequest['emergency']
        event=jsonRequest['conjunto']
    elif  'failure' in jsonRequest:
        jsonRequest=jsonRequest['failure']
        event=jsonRequest['conjunto']
    print("JSON",jsonRequest)
    print("EVENT",event)
    socketio.emit(event,msg.payload.decode('utf-8'))

def on_disconnect(client, userdata, rc):
	if rc != 0:
		print ("Desconexion inesperada al servidor MQTT COD:[{0}]".format(str(rc)))
	

#-------------FIN MQTT---------------#


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set('yale', password='Yale2018.')
client.connect("34.202.239.178", 8083, 60)

# Rutina que se ejecuta cada vez que se conecta un cliente de websocket e inicia el conmunidor de Kafka
@socketio.on('connect')
def test_connect():
    print("Conecta")

def main():
		mqtt_thread = MQTT_Thread()
		mqtt_thread.start()
		socketio.run(app, host='0.0.0.0',port=8079,debug=True)
    

# Iniciar el servicio en el puerto 8079
if __name__ == '__main__':
    main()