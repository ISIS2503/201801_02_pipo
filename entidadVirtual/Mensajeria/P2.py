import json
import requests
from kafka import KafkaConsumer
from flask import app,Flask, render_template, request, session, redirect, url_for
from bson.json_util import dumps, loads, ObjectId, CANONICAL_JSON_OPTIONS
 
topicos2=("alta.piso1","Centro.Toscana.emergencia.aperturaSospechosa.2-503","Centro.Toscana.emergencia.puertaAbierta.2-503",
         "Centro.Toscana.emergencia.aperturaNoPermitida.3-503","Centro.Toscana.emergencia.bateriaCritica.2-503")

consumer = KafkaConsumer(bootstrap_servers=['172.24.42.70:8090'])
consumer.subscribe(topicos2)
app = Flask(__name__)
app.secret_key = "super secret key"

isAuthenticated=False
print(topicos2)
print(consumer)
for message in consumer:
	print(message)
	location = message.topic.split('.')
	sensor_code = location[1] + '.' + location[2]
	
	json_data = json.loads(message.value.decode('utf-8'))
	sensetime = json_data['sensetime']
	emergency = json_data['emergency']
	
	unidad = emergency['conjunto']
	inmuebleId = emergency['apartamento']
	idEmergencia = emergency['emergencia']
	
	tipoEmergencia = ''
	if idEmergencia == str(1):
		tipoEmergencia = 'Puerta abierta'
	elif idEmergencia == str(2):
		tipoEmergencia = 'Apertura sospechosa'
	elif idEmergencia == str(3):
		tipoEmergencia = 'Apertura no permitida'
	elif idEmergencia == str(4):
		tipoEmergencia = 'Bateria baja'
	if isAuthenticated==False:
		with app.test_request_context():
			url='https://isis2503-jamanrique.auth0.com/oauth/token'
			payload={
					"grant_type":"http://auth0.com/oauth/grant-type/password-realm",
					"username": "yale1234",
					"password": "Yale1234",
					"scope": "openid",
					"client_id": "VFOHkNbDGQJlrFJ8QzfmLkM3EVhDIDFn", 
					"client_secret": "QeQufdmrmAlBLFOkhYhNbR85g6riIH1maey--dJha5YAZCEnnpkrJ3rSq1PO4pRY", 
					"realm": "Username-Password-Authentication"
					}
			response = requests.post(url, data=json.dumps(payload),headers={'Content-type': 'application/json'})
			print("Response Status Code: " + str(response.status_code))
			resp = loads(response.content)
			url = 'https://' + 'isis2503-jamanrique.auth0.com' + '/userinfo'
			headers = {'authorization': 'Bearer ' + resp['access_token']}
			resp = requests.get(url, headers=headers)
			user_info = resp.json()
			session['JWT_PAYLOAD'] = user_info
			session['PROFILE_KEY'] = {
			  'user_id': user_info['sub'],
			  'name': session['JWT_PAYLOAD']['nickname'],
			  'email': user_info['name'],
			  'picture': user_info['picture']
			}
			print("SESION",type(session))
			isAuthenticated=True	
	url = 'http://172.24.42.64/unidadesResidenciales/' + unidad + '/inmuebles/' + inmuebleId + '/hub/cerradura/emergencias'
	payload = {
		'fecha': sensetime,
		'tipo': tipoEmergencia,
		'idEmergencia' : idEmergencia
    }
	print(tipoEmergencia)
	with app.test_request_context():
		response = requests.post(url, data=json.dumps(payload),headers={'Content-type': 'application/json','session':json.loads(str(session))})
		print("Response Status Code: " + str(response.status_code))
		print(response.content)
		if(response.status_code==403):
			isAuthenticated=False
	
	
	

		
	
