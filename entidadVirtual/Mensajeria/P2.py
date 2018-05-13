import json
import requests
from kafka import KafkaConsumer
from bson.json_util import dumps, loads, ObjectId, CANONICAL_JSON_OPTIONS
 
topicos2=("Centro.Toscana.emergencia.aperturaSospechosa.2-5-3","Centro.Toscana.emergencia.puertaAbierta.2-5-3",
         "Centro.Toscana.emergencia.aperturaNoPermitida.2-5-3","Centro.Toscana.emergencia.bateriaCritica.2-5-3")
topicosFallos=("Centro.Toscana.fallo.cerraduraFueraDeLinea.2-5-3","Centro.Toscana.fallo.hubFueraDeLinea.2-5-3")
consumer = KafkaConsumer(bootstrap_servers=['172.24.42.70:8090'])
consumer.subscribe(topicos2)
consumer.subscribe(topicosFallos)

isAuthenticated=False
print(topicos2)
print(topicosFallos)
print(consumer)
for message in consumer:
	if isAuthenticated==False:
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
		sessionParam={"JWT_PAYLOAD": user_info,"PROFILE_KEY":{"user_id": user_info['sub'],
															  "name": user_info['nickname'],
															  "email": user_info['name'],
															  "picture": user_info['picture']
															}
					}
		print("SESION",type(sessionParam))
		isAuthenticated=True	

	print(message)
	if message.topic in topicos2:
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
		
		url = 'http://172.24.42.64/p2/unidadesResidenciales/' + unidad + '/inmuebles/' + inmuebleId + '/hub/cerradura/emergencias'
		payload = {
			'fecha': sensetime,
			'tipo': tipoEmergencia,
			'idEmergencia' : idEmergencia
	    }
	elif message.topic in topicosFallos:
		location = message.topic.split('.')
		sensor_code = location[1] + '.' + location[2]
		
		json_data = json.loads(message.value.decode('utf-8'))
		sensetime = json_data['sensetime']
		failure = json_data['failure']
		
		unidad = failure['conjunto']
		inmuebleId = failure['apartamento']
		idFallo = failure['fallo']
		
		tipoFallo = ''
		if idFallo == str(1):
			tipoFallo = 'Cerradura fuera de linea'
		elif idFallo == str(2):
			tipoFallo = 'Hub fuera de linea'
		
		url = 'http://172.24.42.64/p2/unidadesResidenciales/' + unidad + '/inmuebles/' + inmuebleId + '/hub/fallos'
		payload = {
			'fecha': sensetime,
			'tipo': tipoFallo,
			'idFallo' : idFallo
	    }
	response = requests.post(url, data=json.dumps(payload),headers={'Content-type': 'application/json','sessionParam':json.dumps(sessionParam)})
	print("Response Status Code: " + str(response.status_code))
	print(response.content)
	if(response.status_code!=200):
		isAuthenticated=False
	
	
	

		
	
