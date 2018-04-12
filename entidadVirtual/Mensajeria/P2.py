import json
import requests
from kafka import KafkaConsumer
 
topicos2=("Centro.Toscana.emergencia.aperturaSospechosa.2-503","Centro.Toscana.emergencia.puertaAbierta.2-503",
         "Centro.Toscana.emergencia.aperturaNoPermitida.3-503","Centro.Toscana.emergencia.bateriaCritica.2-503")

consumer = KafkaConsumer(bootstrap_servers=['172.24.42.64:8090'])
consumer.subscribe(topicos2)
 
for message in consumer:
	json_data = json.loads(message.value.decode('utf-8'))
	sensetime = json_data['sensetime']
	emergency = json_data['emergency']
	
	unidad = emergency['conjunto']
	inmuebleId = emergency['apartamento']
	idEmergencia = emergency['emergencia']
	zone=emergency['zona']
	
	tipoEmergencia = ''
	if idEmergencia == str(1):
		tipoEmergencia = 'Puerta abierta'
	elif idEmergencia == str(2):
		tipoEmergencia = 'Apertura sospechosa'
	elif idEmergencia == str(3):
		tipoEmergencia = 'Apertura no permitida'
	elif idEmergencia == str(4):
		tipoEmergencia = 'Bateria baja'
	
	
	location = message.topic.split('.')
	sensor_code = location[1] + '.' + location[2]
 
	url = 'http://172.24.42.64:8080/unidadesResidenciales/' + unidad + '/inmuebles/' + inmuebleId + '/hub/cerradura/emergencias'
	payload = {
		'fecha': sensetime,
		'tipo': tipoEmergencia,
		'idEmergencia' : idEmergencia
		'zona':zone
    }
	print(tipoEmergencia)
	response = requests.post(url, data=json.dumps(payload),headers={'Content-type': 'application/json'})
	print("Response Status Code: " + str(response.status_code))
