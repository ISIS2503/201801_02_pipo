from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory
from flask_cors import CORS
from authlib.flask.client import OAuth
from pymongo import MongoClient, ReturnDocument
from bson.json_util import dumps, loads, ObjectId, CANONICAL_JSON_OPTIONS
from functools import wraps
from six.moves.urllib.parse import urlencode
from flask_mqtt import Mqtt
import re
import http.client
import os
import json
import requests

#Constantes para conexión mqtt
broker_address = "172.24.41.182"
port = 8083
user = "Yale"
password = "piporules"

#Constantes métodos REST
GET = 'GET'
POST = 'POST'
PUT = 'PUT'
DELETE = 'DELETE'

#Expresión regular para verificar horas [00:00] - [23:59]
TIME_REGEX = r"[0-2][0-9]:[0-5][0-9]"

#Tipos de autorización
USER = 'USER'
YALE = 'YALE'
SECURITY = 'SECURITY'
UR_ADMIN = 'UR_ADMIN'
PROPERTY_OWNER = 'PROPERTY_OWNER'
DISABLED = 'DISABLED'

#Tipo de operación
DEVELOPMENT_MODE = False

#Instalación en AWS ---------------------
#pip install -r requirements.txt (faltan algunos)
#Por SSH, parado en la carpeta de este archivo, poner las siguientes líneas de código:
#export FLASK_APP = "server.py"
#export AUTH0_YALE_CLIENT_SECRET = "<CLIENT_SECRET_AUTH0>"
#export DB_PIPO_IP = <Mongo_IP>
#export DB_PIPO_PORT = <Mongo_Port>
#Correr ejecutando el comando "flask run --port=8080   --host="0.0.0.0" estando parado en el directorio de este archivo

#Setup de mongoDB - MV windows uniandes -- OUTDATED
#Puerto: 27017
#DB: Pipo-yale-persistencia
#COL: unidadesResidenciales / users / groups

#Setup de mongoDB - AWS
DB_IP = os.environ.get('DB_PIPO_IP')
DB_PORT = os.environ.get('DB_PIPO_PORT')
#DB: Pipo-yale-persistencia
#COL: unidadesResidenciales / users / groups

elScope = ''
username = ''

client = MongoClient(DB_IP, int(DB_PORT))
db = client['Pipo-yale-persistencia']
app = Flask(__name__)
CORS(app)
app.secret_key = os.environ.get('AUTH0_CLIENT_SECRET')
app.config['MQTT_BROKER_URL'] = os.environ.get(DB_IP)
app.config['MQTT_BROKER_PORT'] = 8083
app.config['MQTT_USERNAME'] = 'yale'
app.config['MQTT_PASSWORD'] = 'Yale2018.'
app.config['MQTT_KEEPALIVE'] = 5

# Parameters for SSL enabled
#app.config['MQTT_TLS_ENABLED'] = True
#app.config['MQTT_TLS_CA_CERTS'] = 'ca.crt'
#app.config['MQTT_TLS_CERTFILE'] = 'server.crt'
#app.config['MQTT_TLS_KEYFILE'] = 'server.key'
#app.config['MQTT_TLS_VERSION'] = ssl.PROTOCOL_TLSv1_1

#producer = KafkaProducer(bootstrap_servers='172.24.42.70:8090')
mqtt = Mqtt(app);

oauth = OAuth(app)
auth0 = oauth.register(
  'auth0',
  client_id='VFOHkNbDGQJlrFJ8QzfmLkM3EVhDIDFn',
  client_secret=os.environ.get('AUTH0_CLIENT_SECRET'),
  api_base_url='https://%s' % 'isis2503-jamanrique.auth0.com',
  access_token_url='https://isis2503-jamanrique.auth0.com/oauth/token',
  authorize_url='https://isis2503-jamanrique.auth0.com/authorize',
  client_kwargs={
    'scope': 'openid profile'
  }
)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
  print("hola mundo")

def checkRole(user_id, auth_type):
  user = db.users.find_one({'auth0_id' : user_id})
  print("userRole",user['group'])
  if user:
    group = db.groups.find_one({'nombre' : user['group']})
    #Si el usuario existe, se concede la autorización de usuario por defecto
    if auth_type == USER:
      return True
    if group:
      return auth_type in group['roles']
  return False

def checkScope(user_id, auth_type, scope):
  user = db.users.find_one({'auth0_id' : user_id})
  global username
  username = user['username']
  print("username afuera: "+username)
  print("userScope",user['scope'])
  if not scope:
    return True
  if user:
    return scope.startswith(user['scope']) or scope == user['username']
  return "El usuario no existe", 404

def checkSession(user_id, auth_type, scope):
  print('uid: ', user_id, 'auth: ', auth_type, 'scope: ', scope)
  userId = user_id
  return checkRole(user_id, auth_type) and checkScope(user_id, auth_type, scope)

def requires_auth(auth_type):
	def decorator(func, *args1):
		@wraps(func)
		def decorated(*args, **kwargs):
			global elScope
			scope = ''
			elScope = ''
			print('a',args)
			print('kwa',kwargs)
			for arg in kwargs:
				scope += kwargs[arg] + '/'
				elScope += kwargs[arg] + '/'
			scope = scope[:-1]
			elScope = elScope[:-1]
			print(elScope)
			if 'PROFILE_KEY' not in session:
				return redirect('/login')
			elif checkSession(session['PROFILE_KEY']['user_id'], auth_type, scope):
				return func(*args, **kwargs)
			else:
				return redirect('/unauthorized')
		return decorated
	return decorator
   


@app.route('/testo/<param1>/<param2>')
@requires_auth(PROPERTY_OWNER)
def testt(param1, param2):
  return param1 + param2

@app.route('/unauthorized', methods=[GET, POST, PUT, DELETE])
def unauthorized():
  return "No tiene los permisos necesarios para ejecutar la operación", 403

@app.route('/callback')
def callback_handling():
  # Maneja la respuesta desde el endpoint del token
  #resp = auth0.authorized_response()
  resp = auth0.authorize_access_token()
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

  #Idealmente con redis pero YOLO
  user = db.users.find_one({'auth0_id' : user_info['sub']})
  if not user: #POST User
    info = session['PROFILE_KEY']
    insert = db.users.insert_one({ 'auth0_id' :  info['user_id'] , 'username' : info['name'], 'email': info['email'], 'group' : USER,  'scope' : '/*--//--*/', 'horariosPermitidos' : []})
    return redirect('/welcome/' + info['name'])
  else:
    return redirect('/dashboard')

@app.route('/login')
def login():
  return auth0.authorize_redirect(redirect_uri='http://ec2-34-202-239-178.compute-1.amazonaws.com:8080/callback')

@app.route('/dashboardLogin')
def dashboardL_login():
  return auth0.authorize_redirect(redirect_uri='http://ec2-34-202-239-178.compute-1.amazonaws.com:8080/dashboardCallback')

@app.route('/dashboardCallback')
def dashboard_callback_handling():
  # Maneja la respuesta desde el endpoint del token
  #resp = auth0.authorized_response()
  resp = auth0.authorize_access_token()
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

  #Idealmente con redis pero YOLO
  user = db.users.find_one({'auth0_id' : user_info['sub']})
  if not user: #POST User
    info = session['PROFILE_KEY']
    insert = db.users.insert_one({ 'auth0_id' :  info['user_id'] , 'username' : info['name'], 'email': info['email'], 'group' : USER,  'scope' : '/*--//--*/', 'horariosPermitidos' : []})
    return redirect('/welcome/' + info['name'])
  else:
    #On development, localhost serves js and HTML
    if DEVELOPMENT_MODE:
      return redirect('http://localhost:8080/#/dashboard/' + session['PROFILE_KEY']['name'])
    #On production, server serves js and HTML
    else:
      return redirect('/security#/dashboard/' + session['PROFILE_KEY']['name'])

@app.route('/security')
@requires_auth(SECURITY)
def securityDashboard():
  return render_template('dist/index.html')

@app.route('/securityLogin')
def securityLogin():
  return render_template('loginDist/index.html')

@app.route('/static/js/<file>')
def servingJs(file):
  return send_from_directory('templates/dist/static/js', file)

@app.route('/static/css/<file>')
def servingCSS(file):
  return send_from_directory('templates/dist/static/css', file)

@app.route('/static/img/<file>')
def servingImages(file):
  return send_from_directory('templates/dist/static/img', file)

@app.route('/login/static/js/<file>')
def servingLoginJs(file):
  return send_from_directory('templates/loginDist/static/js', file)

@app.route('/login/static/css/<file>')
def servingLoginCSS(file):
  return send_from_directory('templates/loginDist/static/css', file)

@app.route('/login/static/img/<file>')
def servingLoginImages(file):
  return send_from_directory('templates/loginDist/static/img', file)

@app.route('/welcome/<usuario>')
@requires_auth(USER)
def welcome(usuario):
  return render_template('welcome.html')

@app.route('/dashboard')
@requires_auth(USER)
def post_login():
  return render_template('dashboard.html')

@app.route('/dashboard/collections')
@requires_auth(USER)
def collection_invoker():
  return render_template('collections.html')

@app.route('/collections')
@requires_auth(USER)
def collections_serving():
  return send_from_directory('collections', 'collections.js')

@app.route('/logout')
def logout():
  #Limpiar información de la sesión
  session.clear()
  #Redireccionar
  params = {'returnTo': url_for('logged_out', _external=True), 'client_id': 'AJqGQ4TtjF3Vw8pIGW1w-IUbGyplpsJa'}
  return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

@app.route('/logged_out')
def logged_out():
  return render_template('logged_out.html')

@app.route("/", methods=[GET])
def home():
  return redirect('/home')

@app.route('/home')
def hello():
  return render_template("index.html")

@app.route("/yale", methods=[GET])
@requires_auth(YALE)
def yale():
    respuesta = []
    #Encontrar todos las unidades residenciales
    for doc in db.unidadesResidenciales.find():
      #Agregar cada una al objeto
      respuesta.append(doc)
    #Retornar JSON
    return dumpJson(respuesta)

@app.route("/unidadesResidenciales/<unidad>", methods=[GET, PUT, DELETE])
@requires_auth(UR_ADMIN)
def unidadResidencial(unidad):
  if request.method == GET:
    respuesta = {}
    #Encontrar todos las unidades residenciales
    respuesta = db.unidadesResidenciales.find_one({"nombre" : unidad})
    #Retornar JSON
    return dumpJson(respuesta)
  elif request.method == PUT:
    #Convertir JSON a directorio python
    data = loads(request.data).decode('utf-8')
    #Verificar campos no nulos/vacíos
    valid = True
    try:
      valid = valid and (data['nombre'] != None or data['nombre'] != "")
      valid = valid and (data['direccion'] != None or data['direccion'] != "")
    except KeyError:
      return "Falta el nombre o la dirección de la unidad", 400

    try:
      valid = data['inmuebles'] == [] and False
      if not valid:
        return "No puede haber inmuebles asociados en la actualización de una unidad residencial", 400
    except KeyError:
      valid = True

    if not valid:
      return "No debe haber campos vacíos", 400
    #Actualizar en la base de datos
    nuevo = db.unidadesResidenciales.find_one_and_update({"nombre": unidad}, {'$set' : {'nombre': data['nombre'], 'direccion': data['direccion']}}, return_document=ReturnDocument.AFTER)
    return dumpJson(nuevo)
  elif request.method == DELETE:
    borrado = db.unidadesResidenciales.find_one_and_delete({"nombre" : unidad})
    return dumpJson(borrado)
  
@app.route("/unidadesResidenciales", methods=[POST])
@requires_auth(YALE)
def crearUnidad():
  if request.method == POST:
    if request.data == None or request.data == "":
      return "Debe enviar información", 400

    data = loads(request.data).decode('utf-8')
    valid = True
    try:
      valid = valid and (data['nombre'] != None or data['nombre'] != "")
      valid = valid and (data['direccion'] != None or data['direccion'] != "")
      valid = valid and (data['owner_user_id'] != None or data['owner_user_id'] != "")
      valid = valid and (data['security_user_id'] != None or data['security_user_id'] != "")
    except KeyError:
      return "Falta el nombre, la dirección de la unidad o el usuario administrador", 400

    try:
      valid = valid and (data['inmuebles'] == [])
      if not valid:
        return "No puede haber ningún inmueble asociado en la creación de una unidad residencial", 400
    except KeyError:
      valid = True

    if not valid:
      return "Solo el arreglo de inmuebles puede estar vacío, los demás atributos no", 400

    #Buscar el usuario propietario y seguridad
    owner_user_id = data['owner_user_id']
    owner_user = db.users.find_one({'auth0_id' : owner_user_id })

    security_user_id = data['security_user_id']
    security_user = db.users.find_one({'auth0_id' : security_user_id })

    #Si no encontró el usuario para asignarle la propiedad
    if not owner_user or not security_user:
      return "El usuario especificado para que sea asignado como administrador o seguridad (de unidad residencial), no existe", 400

    #Objeto nuevo para eliminar posibles campos adicionales del json
    sanitizedData = {}
    sanitizedData['nombre'] = data['nombre']
    sanitizedData['direccion'] = data['direccion']
    sanitizedData['inmuebles'] = []

    #Añadir scope al dueño y a la seguridad
    scope = data['nombre']
    db.users.find_one_and_update({'auth0_id' : owner_user_id}, {'$set': {'scope': scope, 'group': UR_ADMIN}})
    db.users.find_one_and_update({'auth0_id' : security_user_id}, {'$set': {'scope': scope, 'group': SECURITY}})

    #Insertar en mongoDB
    try:
      result = db.unidadesResidenciales.insert_one(sanitizedData)
      sanitizedData['_id'] = result.inserted_id
      return dumpJson(sanitizedData)
    except Exception as error:
      print(error)
      return "Ya existe una unidad residencial con ese nombre", 400

@app.route("/unidadesResidenciales/<unidad>/inmuebles", methods=[GET, POST])
@requires_auth(SECURITY)
def imuebles(unidad):
  if request.method == GET:
    unidad = db.unidadesResidenciales.find_one({ 'nombre' : unidad })
    if unidad == None:
      return "{}", 404
    else:
      return dumpJson(unidad['inmuebles'])
  elif request.method == POST:
    if request.data == None or request.data == "":
      return "Debe enviar información", 400
    
    data = loads(request.data).decode('utf-8')
    valid = True
    try:
      valid = valid and (data['localID'] != None or data['localID'] != "")
      valid = valid and (data['owner'] != None or data['owner'] != "")
      valid = valid and (data['owner_user_id'] != None or data['owner_user_id'] != "")
    except KeyError:
      return "Debe incluir el identificador local del inmueble", 400

    #Buscar el usuario propietario
    user_id = data['owner_user_id']
    user = db.users.find_one({'auth0_id' : user_id })

    #Si no encontró el usuario para asignarle la propiedad
    if not user:
      return "El usuario especificado para que sea asignado como propietario, no existe", 400

    #Objeto nuevo para eliminar posibles campos adicionales del json
    sanitizedData = {}
    sanitizedData['_id'] = ObjectId()
    sanitizedData['localID'] = data['localID']
    sanitizedData['hub'] = {}
    sanitizedData['owner'] = data['owner']
    sanitizedData['owner_user_id'] = data['owner_user_id']
    #Añadir al arreglo de inmuebles
    result = db.unidadesResidenciales.find_one_and_update({'nombre':unidad}, {'$push': {'inmuebles': sanitizedData}})
    #Añadir scope al dueño
    scope = unidad + '/' + sanitizedData['localID']
    db.users.find_one_and_update({'auth0_id' : user_id}, {'$set': {'scope': scope, 'group': PROPERTY_OWNER}})
    if result == None:
      return "No hay ninguna unidad con ese nombre", 404
    return dumpJson(result)

@app.route("/unidadesResidenciales/<unidad>/inmuebles/<localID>", methods=[GET, PUT, DELETE])
@requires_auth(PROPERTY_OWNER)
def inmuebles(unidad, localID):
  if request.method == GET:
    respuesta = []
    unidadRes = db.unidadesResidenciales.find_one({ 'nombre' : unidad })
    #Buscar inmueble dentro de la unidad residencial
    if unidadRes == None:
      return "{}", 404
    for inmueble in unidadRes['inmuebles']:
      if inmueble['localID'] == localID:
        respuesta = inmueble
        break
    #Lo retorna
    return dumpJson(respuesta)
  elif request.method == PUT:
    data = loads(request.data).decode('utf-8')
    valid = True
    try:      
      valid = valid and (data['localID'] != None or data['localID'] != "")
    except KeyError:
      return "Debe incluir el identificador local del minmueble", 400
    
    #Esta linea busca los documentos que tengan la propiedad nombre == unidad
    #Y luego actualiza el valor del campo inmuebles[x].localID a el nuevo identificador local del inmueble
    #inmuebles[x] corresponde al elemento tal que inmuebles[x].localID == antiguo identificador local del inmueble
    nuevo = db.unidadesResidenciales.find_one_and_update({'nombre': unidad,},
    {'$set': {'inmuebles.$[elemento].localID' : data['localID']}},
    array_filters=[ {'elemento.localID': {'$eq' : localID}} ],
    return_document=ReturnDocument.AFTER)
    if nuevo == None:
      return "No hay ninguna unidad con ese nombre o inmueble con ese ID", 404
    return dumpJson(nuevo)
  elif request.method == DELETE:
    #Esta linea busca los documentos que tengan la propiedad nombre == unidad
    #Y luego actualiza el valor del campo inmuebles, eliminando el elemento con 'localID' que entró por parámetro
    nuevo = db.unidadesResidenciales.find_one_and_update({'nombre': unidad,},
    {'$pull': {'inmuebles' : {'localID' : localID}}},
    return_document=ReturnDocument.AFTER)
    return dumpJson(nuevo)

@app.route("/unidadesResidenciales/<unidad>/inmuebles/<localID>/hub", methods=[GET, POST, PUT, DELETE])
@requires_auth(PROPERTY_OWNER)
def hub(unidad, localID):
  if request.method == GET:
    respuesta = []
    unidadRes = db.unidadesResidenciales.find_one({ 'nombre' : unidad })
    if unidadRes == None:
      return "{}", 404
    for inmueble in unidadRes['inmuebles']:
      if inmueble['localID'] == localID:
        respuesta = inmueble
        break
    if respuesta == []:
      return "El inmueble solicitado no presenta ningún hub asociado"
    #Retorna solo el Hub del inmueble buscado
    return dumpJson(respuesta['hub'])
  elif request.method == POST or request.method == PUT:
    if request.data == None or request.data == "":
      return "Debe enviar información", 400
    
    data = loads(request.data).decode('utf-8')
    valid = True
    try:
      valid = valid and (data['frecuencia'] != None or data['frecuencia'] != "")
      valid = valid and (data['fallosMaximos'] != None or data['fallosMaximos'] != "")
      valid = valid and (data['zona'] != None or data['zona']!="")
    except KeyError:
      return "Debe incluir la frecuencia, la zona y el número de fallos máximos del inmueble", 400

    #Objeto nuevo para eliminar posibles campos adicionales del json
    sanitizedData = {}
    sanitizedData['_id'] = ObjectId()
    sanitizedData['frecuencia'] = data['frecuencia']
    sanitizedData['fallosMaximos'] = data['fallosMaximos']
    sanitizedData['zona']=data['zona']
    sanitizedData['fallos'] = []
    sanitizedData['cerradura'] = {}

    #Esta linea busca los documentos que tengan la propiedad nombre == unidad
    #Y luego actualiza el valor del campo inmuebles[x].hub a el nuevo hub
    #inmuebles[x] corresponde al elemento tal que inmuebles[x].localID == identificador local del inmueble
    result = db.unidadesResidenciales.find_one_and_update({'nombre': unidad,},
    {'$set': {'inmuebles.$[elemento].hub' : sanitizedData}},
    array_filters=[ {'elemento.localID': {'$eq' : localID}} ],
    return_document=ReturnDocument.AFTER)
    if result == None:
      return "No hay ninguna unidad con ese nombre o inmueble con ese ID", 404
    return dumpJson(result)
  elif request.method == DELETE:
    #Esta linea busca los documentos que tengan la propiedad nombre == unidad
    #Y luego actualiza el valor del campo inmuebles[x].hub a el nuevo hub
    #inmuebles[x] corresponde al elemento tal que inmuebles[x].localID == identificador local del inmueble
    result = db.unidadesResidenciales.find_one_and_update({'nombre': unidad,},
    {'$set': {'inmuebles.$[elemento].hub' : {}}},
    array_filters=[ {'elemento.localID': {'$eq' : localID}} ],
    return_document=ReturnDocument.AFTER)
    if result == None:
      return "No hay ninguna unidad con ese nombre o inmueble con ese ID", 404
    return dumpJson(result)

@app.route("/unidadesResidenciales/<unidad>/inmuebles/<localID>/hub/cerradura", methods=[GET, POST, PUT, DELETE])
@requires_auth(PROPERTY_OWNER)
def cerradura(unidad, localID):
  if request.method == GET:
    respuesta = []
    unidadRes = db.unidadesResidenciales.find_one({ 'nombre' : unidad })
    if unidadRes == None:
      return "{}", 404
    for inmueble in unidadRes['inmuebles']:
      if inmueble['localID'] == localID:
        respuesta = inmueble
        break
    if respuesta['hub'] == {}:
      return "{}", 404
    return dumpJson(respuesta['hub']['cerradura'])
  elif request.method == POST or request.method == PUT:
    if request.data == None or request.data == "":
      return "Debe enviar información", 400
    
    data = loads(request.data).decode('utf-8')
    valid = True
    try:
      valid = valid and (data['bateriaCritica'] != None or data['bateriaCritica'] != "")
      valid = valid and (data['tiempoMaximo'] != None or data['tiempoMaximo'] != "")
      valid = valid and (data['frequencia'] != None or data['frequencia'] != "")
      valid = valid and (data['fallosMaximos'] != None or data['fallosMaximos'] != "")
    except KeyError:
      return "Debe incluir la frecuencia y el número de fallos máximos del inmueble", 400

    sanitizedData = {}
    sanitizedData['bateriaCritica'] = data['bateriaCritica']
    sanitizedData['tiempoMaximo'] = data['tiempoMaximo']
    sanitizedData['frequencia'] = data['frequencia']
    sanitizedData['fallosMaximos'] = data['fallosMaximos']
    sanitizedData['claves'] = []
    sanitizedData['emergencias'] = []
    sanitizedData['horariosPermitidos'] = []

    #Esta linea busca los documentos que tengan la propiedad nombre == unidad
    #Y luego actualiza el valor del campo inmuebles[x].hub a el nuevo hub
    #inmuebles[x] corresponde al elemento tal que inmuebles[x].localID == identificador local del inmueble
    result = db.unidadesResidenciales.find_one_and_update({'nombre': unidad,},
    {'$set': {'inmuebles.$[elemento].hub.cerradura' : sanitizedData}},
    array_filters=[ {'elemento.localID': {'$eq' : localID}} ],
    return_document=ReturnDocument.AFTER)
    if result == None:
      return "No hay ninguna unidad con ese nombre o inmueble con ese ID", 404
    return dumpJson(result)
  elif request.method == DELETE:
    #Esta linea busca los documentos que tengan la propiedad nombre == unidad
    #Y luego actualiza el valor del campo inmuebles[x].hub a un hub vacío (Equivalente a eliminarlo)
    #inmuebles[x] corresponde al elemento tal que inmuebles[x].localID == identificador local del inmueble
    result = db.unidadesResidenciales.find_one_and_update({'nombre': unidad,},
    {'$set': {'inmuebles.$[elemento].hub.cerradura' : {}}},
    array_filters=[ {'elemento.localID': {'$eq' : localID}} ],
    return_document=ReturnDocument.AFTER)
    if result == None:
      return "No hay ninguna unidad con ese nombre o inmueble con ese ID", 404
    return dumpJson(result)

@app.route("/unidadesResidenciales/<unidad>/inmuebles/<localID>/hub/cerradura/claves", methods=[GET, POST, PUT, DELETE])
@requires_auth(PROPERTY_OWNER)
def claves(unidad, localID):
  data = {}
  if request.data:
    data = loads(request.data).decode('utf-8')
  if request.method == GET:
    respuesta = []
    unidadRes = db.unidadesResidenciales.find_one({ 'nombre' : unidad })
    if unidadRes == None:
      return "{}", 404
    for inmueble in unidadRes['inmuebles']:
      if inmueble['localID'] == localID:
        respuesta = inmueble
        break
    if respuesta == []:
      return "No existe ningún inmueble en esa unidad residencial con ese localID", 404;
    return dumpJson(respuesta['hub']['cerradura']['claves'])
  elif request.method == POST or request.method == PUT:
    if request.data == None or request.data == "":
      return "Debe enviar información", 400
    
    valid = True
    try:
      valid = valid and (data['combinacion'] != None or data['combinacion'] != "")
    except KeyError:
      return "Debe incluir la frecuencia y el número de fallos máximos del inmueble", 400

    if not valid:
      return "rellene los campos vacíos", 400

    valid = valid and len(data['combinacion']) == 4

    if not valid:
      return "La combinación debe tener exactamente 4 caracteres", 400

    #Esta linea busca los documentos que tengan la propiedad nombre == unidad
    #Y luego inserta a el valor del campo inmuebles[x].hub.cerradura.claves la nueva combinación
    #inmuebles[x] corresponde al elemento tal que inmuebles[x].localID == identificador local del inmueble
    result = db.unidadesResidenciales.find_one_and_update({'nombre': unidad,},
    {'$push': {'inmuebles.$[elemento].hub.cerradura.claves' : str(data['combinacion'])}},
    array_filters=[ {'elemento.localID': {'$eq' : localID}} ],
    return_document=ReturnDocument.AFTER)
    if result == None:
      return "No hay ninguna unidad con ese nombre o inmueble con ese ID", 404
    return dumpJson(result)
  elif request.method == DELETE:
    clave = ""
    try:
       clave = data['clave']
    except KeyError:
      return "Debe enviar qué clave se va a borrar", 400
    #Esta linea busca los documentos que tengan la propiedad nombre == unidad
    #Y luego actualiza el valor del campo inmuebles, eliminando el elemento con 'localID' que entró por parámetro
    nuevo = db.unidadesResidenciales.find_one_and_update({'nombre': unidad,},
    {'$pull': {'inmuebles.$[elemento].hub.cerradura.claves' : {'$eq' : clave}}},
    array_filters=[ {'elemento.localID': {'$eq' : localID}} ],
    return_document=ReturnDocument.AFTER)
    if result == None:
      return "No hay ninguna unidad con ese nombre o inmueble con ese ID", 404
    return dumpJson(nuevo)


@app.route("/unidadesResidenciales/<unidad>/inmuebles/<localID>/hub/cerradura/gestionClaves", methods=[POST, PUT, DELETE])
def gestionClaves(unidad, localID):
  data = {}
  if request.data:
    data = loads(request.data).decode('utf-8')
  valid = True
  try:
    valid = valid and (data['indice'] != None or data['indice'] != "")
  except KeyError:
    return "Debe incluir el índice", 400
  if not valid:
    return "rellene los campos vacíos", 400
  indice = data['indice']
  if request.method == POST or request.method == PUT:
    if request.data == None or request.data == "":
      return "Debe enviar información", 400
    
    valid = True
    
    valid = valid and indice >= 0 and indice < 20
    
    if not valid:
      return "Debe ingresar un índice válido"
    
    esBorrado = False
    operacion = "1"
    if request.method == PUT:
      try:
        valid = valid and (data['esBorrado'] != None or data['esBorrado'] != "")
      except KeyError:
        return "Debe incluir la operación", 400
      
      op = data['esBorrado']
      valid = valid and (op==0 or op==1)
      if not valid:
        return "Debe incluir una operación válida", 400
      if op==1:
        esBorrado = True
      operacion = str(op+2)
    combinacion = ""
    if not esBorrado:
      try:
        valid = valid and (data['combinacion'] != None or data['combinacion'] != "")
      except KeyError:
        return "Debe incluir la combinación a incluir", 400

      if not valid:
        return "rellene los campos vacíos", 400
      
      combinacion = data['combinacion']
      valid = valid and len(combinacion) == 4
      
      if not valid:
        return "La combinación debe tener exactamente 4 caracteres", 400
      combinacion = ";"+combinacion
    respuesta = []
    unidadRes = db.unidadesResidenciales.find_one({ 'nombre' : unidad })
    if unidadRes == None:
      return "No existe ninguna unidad residencial con ese nombre", 404
    for inmueble in unidadRes['inmuebles']:
      if inmueble['localID'] == localID:
        respuesta = inmueble
        break
    if respuesta == []:
      return "No existe ningún inmueble en esa unidad residencial con ese localID", 404
    
    msg = ";"+str(indice)+combinacion
    msg = operacion+msg
    message = '{"msg":"'+msg+'", "usuario":"'+username+'"}'
    topic = "Centro/"+elScope+"/claves"
    mqtt.publish(topic, message.encode('utf-8'))
    return message, 200
    

@app.route("/unidadesResidenciales/<unidad>/inmuebles/<localID>/hub/cerradura/gestionClaves/borrarTodo", methods=[DELETE])
def borrarClaves(unidad, localID):
  if request.method == DELETE:
    respuesta = []
    unidadRes = db.unidadesResidenciales.find_one({ 'nombre' : unidad })
    if unidadRes == None:
      return "No existe ninguna unidad residencial con ese nombre", 404
    for inmueble in unidadRes['inmuebles']:
      if inmueble['localID'] == localID:
        respuesta = inmueble
        break
    if respuesta == []:
      return "No existe ningún inmueble en esa unidad residencial con ese localID", 404
    
    msg = "4"
    message = '{"msg":"'+msg+'", "usuario":"'+username+'"}'
    topic = "Centro/"+elScope+"/claves"
    mqtt.publish(topic, message.encode('utf-8'))
    return message, 200


@app.route("/cerradura/abrir", methods=[PUT])
def abrirCerradura():
  if request.method == PUT:
    msg = "ABRIR"
    mqtt.publish("Arduino007.recibir", msg)
    return msg, 200


@app.route("/cerradura/cerrar", methods=[PUT])
def cerrarCerradura():
  if request.method == PUT:
    msg = "CERRAR"
    mqtt.publish("Arduino007.recibir", msg)
    return msg, 200



@app.route("/unidadesResidenciales/<unidad>/inmuebles/<localID>/hub/cerradura/emergencias", methods=[GET, POST])
@requires_auth(PROPERTY_OWNER)
def emergencias(unidad, localID):
  data = {}
  if request.data:
    data = loads(request.data).decode('utf-8')
  if request.method == GET:
    respuesta = []
    unidadRes = db.unidadesResidenciales.find_one({ 'nombre' : unidad })
    if unidadRes == None:
      return "{}"
    for inmueble in unidadRes['inmuebles']:
      if inmueble['localID'] == localID:
        respuesta = inmueble
        break
    if respuesta == []:
      return respuesta
    elif respuesta['hub'] == {}:
      return "{}"
    elif respuesta['hub']['cerradura'] == {}:
      return "{}"
    return dumpJson(respuesta['hub']['cerradura']['emergencias'])
  elif request.method == POST or request.method == PUT:
    if request.data == None or request.data == "":
      return "Debe enviar información", 400
    valid = True
    try:
      valid = valid and (data['fecha'] != None or data['fecha'] != "")
      valid = valid and (data['tipo'] != None or data['tipo'] != "")
      valid = valid and (data['idEmergencia'] != None or data['idEmergencia'] != "")
    except KeyError:
      return "Debe incluir la fecha, el tipo y el id de la emergencia", 400

    if not valid:
      return "Rellene los campos vacíos", 400

    #7 ids diferentes de emergencia
    valid = valid and int(data['idEmergencia']) > 0 and int(data['idEmergencia']) < 9

    if not valid:
      return "El id de la emergencia debe estar entre 1 y 8", 400

    sanitizedData = {}
    sanitizedData['fecha'] = data['fecha']
    sanitizedData['tipo'] = data['tipo']
    sanitizedData['idEmergencia'] = data['idEmergencia']

    #Esta linea busca los documentos que tengan la propiedad nombre == unidad
    #Y luego inserta a el valor del campo inmuebles[x].hub.cerradura.claves la nueva combinación
    #inmuebles[x] corresponde al elemento tal que inmuebles[x].localID == identificador local del inmueble
    result = db.unidadesResidenciales.find_one_and_update({'nombre': unidad,},
    {'$push': {'inmuebles.$[elemento].hub.cerradura.emergencias' : sanitizedData}},
    array_filters=[ {'elemento.localID': {'$eq' : localID}} ],
    return_document=ReturnDocument.AFTER)
    if result == None:
      return "No hay ninguna unidad con ese nombre o inmueble con ese ID", 404
    return dumpJson(result)

@app.route("/p2/unidadesResidenciales/<unidad>/inmuebles/<localID>/hub/cerradura/emergencias", methods=[GET, POST])
def emergenciasP2(unidad, localID):
  data = {}
  if request.data:
    data = loads(request.data).decode('utf-8')
  if request.method == POST:
    sessionParam=json.loads(request.headers['sessionParam']).decode('utf-8')
    user = db.users.find_one({'auth0_id' : sessionParam['PROFILE_KEY']['user_id']})
    if False==checkSession(sessionParam['PROFILE_KEY']['user_id'], YALE, user['scope']):
      return "Hubo un error autenticando al usuario",403     
    if request.data == None or request.data == "":
      return "Debe enviar información", 400
    valid = True
    try:
      valid = valid and (data['fecha'] != None or data['fecha'] != "")
      valid = valid and (data['tipo'] != None or data['tipo'] != "")
      valid = valid and (data['idEmergencia'] != None or data['idEmergencia'] != "")
    except KeyError:
      return "Debe incluir la fecha, el tipo y el id de la emergencia", 400

    if not valid:
      return "Rellene los campos vacíos", 400

    #7 ids diferentes de emergencia
    valid = valid and int(data['idEmergencia']) > 0 and int(data['idEmergencia']) < 9

    if not valid:
      return "El id de la emergencia debe estar entre 1 y 8", 400

    sanitizedData = {}
    sanitizedData['fecha'] = data['fecha']
    sanitizedData['tipo'] = data['tipo']
    sanitizedData['idEmergencia'] = data['idEmergencia']

    #Esta linea busca los documentos que tengan la propiedad nombre == unidad
    #Y luego inserta a el valor del campo inmuebles[x].hub.cerradura.claves la nueva combinación
    #inmuebles[x] corresponde al elemento tal que inmuebles[x].localID == identificador local del inmueble
    result = db.unidadesResidenciales.find_one_and_update({'nombre': unidad,},
    {'$push': {'inmuebles.$[elemento].hub.cerradura.emergencias' : sanitizedData}},
    array_filters=[ {'elemento.localID': {'$eq' : localID}} ],
    return_document=ReturnDocument.AFTER)
    if result == None:
      return "No hay ninguna unidad con ese nombre o inmueble con ese ID", 404
    return dumpJson(result)

@app.route("/unidadesResidenciales/<unidad>/inmuebles/<localID>/hub/fallos", methods=[GET, POST])
@requires_auth(PROPERTY_OWNER)
def fallos(unidad, localID):
  data = {}
  if request.data:
    data = loads(request.data).decode('utf-8')
  if request.method == GET:
    respuesta = []
    unidadRes = db.unidadesResidenciales.find_one({ 'nombre' : unidad })
    if unidadRes == None:
      return "{}"
    for inmueble in unidadRes['inmuebles']:
      if inmueble['localID'] == localID:
        respuesta = inmueble
        break
    if respuesta == []:
      return respuesta
    elif respuesta['hub'] == {}:
      return "{}"
    return dumpJson(respuesta['hub']['fallos'])
  elif request.method == POST or request.method == PUT:
    if request.data == None or request.data == "":
      return "Debe enviar información", 400
    valid = True
    try:
      valid = valid and (data['fecha'] != None or data['fecha'] != "")
      valid = valid and (data['tipo'] != None or data['tipo'] != "")
      valid = valid and (data['idFallo'] != None or data['idFallo'] != "")
    except KeyError:
      return "Debe incluir la fecha, el tipo y el id del fallo", 400

    if not valid:
      return "Rellene los campos vacíos", 400

    #7 ids diferentes de emergencia
    valid = valid and int(data['idFallo']) > 0 and int(data['idFallo']) < 9

    if not valid:
      return "El id del fallo debe estar entre 1 y 8", 400

    sanitizedData = {}
    sanitizedData['fecha'] = data['fecha']
    sanitizedData['tipo'] = data['tipo']
    sanitizedData['idFallo'] = data['idFallo']

    #Esta linea busca los documentos que tengan la propiedad nombre == unidad
    #Y luego inserta a el valor del campo inmuebles[x].hub.cerradura.claves la nueva combinación
    #inmuebles[x] corresponde al elemento tal que inmuebles[x].localID == identificador local del inmueble
    result = db.unidadesResidenciales.find_one_and_update({'nombre': unidad,},
    {'$push': {'inmuebles.$[elemento].hub.fallos' : sanitizedData}},
    array_filters=[ {'elemento.localID': {'$eq' : localID}} ],
    return_document=ReturnDocument.AFTER)
    if result == None:
      return "No hay ninguna unidad con ese nombre o inmueble con ese ID", 404
    return dumpJson(result)

@app.route("/p2/unidadesResidenciales/<unidad>/inmuebles/<localID>/hub/fallos", methods=[GET, POST])
def fallosP2(unidad, localID):
  data = {}
  if request.data:
    data = loads(request.data).decode('utf-8')
  if request.method == POST:
    sessionParam=json.loads(request.headers['sessionParam']).decode('utf-8')
    user = db.users.find_one({'auth0_id' : sessionParam['PROFILE_KEY']['user_id']})
    if False==checkSession(sessionParam['PROFILE_KEY']['user_id'], YALE, user['scope']):
      return "Hubo un error autenticando al usuario",403     
    if request.data == None or request.data == "":
      return "Debe enviar información", 400
    valid = True
    try:
      valid = valid and (data['fecha'] != None or data['fecha'] != "")
      valid = valid and (data['tipo'] != None or data['tipo'] != "")
      valid = valid and (data['idFallo'] != None or data['idFallo'] != "")
    except KeyError:
      return "Debe incluir la fecha, el tipo y el id del fallo", 400

    if not valid:
      return "Rellene los campos vacíos", 400

    #7 ids diferentes de emergencia
    valid = valid and int(data['idFallo']) > 0 and int(data['idFallo']) < 9

    if not valid:
      return "El id del fallo debe estar entre 1 y 8", 400

    sanitizedData = {}
    sanitizedData['fecha'] = data['fecha']
    sanitizedData['tipo'] = data['tipo']
    sanitizedData['idFallo'] = data['idFallo']

    #Esta linea busca los documentos que tengan la propiedad nombre == unidad
    #Y luego inserta a el valor del campo inmuebles[x].hub.cerradura.claves la nueva combinación
    #inmuebles[x] corresponde al elemento tal que inmuebles[x].localID == identificador local del inmueble
    result = db.unidadesResidenciales.find_one_and_update({'nombre': unidad,},
    {'$push': {'inmuebles.$[elemento].hub.fallos' : sanitizedData}},
    array_filters=[ {'elemento.localID': {'$eq' : localID}} ],
    return_document=ReturnDocument.AFTER)
    if result == None:
      return "No hay ninguna unidad con ese nombre o inmueble con ese ID", 404
    return dumpJson(result)

@app.route("/unidadesResidenciales/<unidad>/inmuebles/<localID>/hub/cerradura/horariosPermitidos", methods=[GET, POST, PUT])
@requires_auth(PROPERTY_OWNER)
def horariosPermitidos(unidad, localID):
  print("data: ")
  print(request.data)
  if request.method == GET:
    respuesta = []
    user = db.users.find_one({'auth0_id' : session['PROFILE_KEY']['user_id']})
    return dumpJson(user['horariosPermitidos'])
  elif request.method == POST:
    if request.data == None or request.data == "":
      return "Debe enviar información", 400
    
    data = loads(request.data).decode('utf-8')
    valid = True
    try:
      valid = valid and (data['horaInicio'] != None or data['horaInicio'] != "")
      valid = valid and (data['horaFin'] != None or data['horaFin'] != "")
    except KeyError:
      return "Debe incluir la hora de inicio y la hora de fin", 400

    if not valid:
      return "Rellene los campos vacíos", 400

    #Verificar expresión regular y que las horas sean menores que 24
    valid = valid and re.search(TIME_REGEX, data['horaInicio']) and int(data['horaInicio'].split(":")[0]) < 24
    if not valid:
      return "El formato de la hora de inicio es incorrecto", 400

    valid = valid and re.search(TIME_REGEX, data['horaFin']) and int(data['horaFin'].split(":")[0]) < 24
    if not valid:
      return "El formato de la hora de fin es incorrecto", 400
    
    horaInicio = data['horaInicio']
    horaFin = data['horaFin']
    sanitizedData = {}
    sanitizedData['horaInicio'] = horaInicio
    sanitizedData['horaFin'] = horaFin
    
    user = db.users.find_one({'auth0_id' : session['PROFILE_KEY']['user_id']})
    if user == None:
      return "No hay ninguna unidad con ese nombre o inmueble con ese ID", 404
    
    if sanitizedData in user['horariosPermitidos']:
      return "El horario a agregar ya existe", 400
    #Esta linea busca los documentos que tengan la propiedad nombre == unidad
    #Y luego inserta a el valor del campo inmuebles[x].hub.cerradura.horariosPermitidos el nuevo horario
    #inmuebles[x] corresponde al elemento tal que inmuebles[x].localID == identificador local del inmueble
    result = db.users.find_one_and_update({'auth0_id' : session['PROFILE_KEY']['user_id']},
    {'$push': {'horariosPermitidos' : sanitizedData}},
    return_document=ReturnDocument.AFTER)
    if result == None:
      return "No hay ninguna unidad con ese nombre o inmueble con ese ID", 404
    
    message = '{"horaInicio":"'+horaInicio+'","horaFin":"'+horaFin+'","usuario":"'+username+'","operacion":1}'
    topic = "Centro/"+elScope+"/horarios"
    mqtt.publish(topic, message.encode('utf-8'))
    return dumpJson(result)
  elif request.method == PUT:
    if request.data == None or request.data == "":
      return "Debe enviar información", 400
    
    data = loads(request.data).decode('utf-8')
    valid = True
    try:
      valid = valid and (data['esBorrado'] != None or data['esBorrado'] != "")
    except KeyError:
      return "Debe incluir la hora de inicio y la hora de fin", 400
    if data['esBorrado'] == 0:
      try:
        valid = valid and (data['horaInicio'] != None or data['horaInicio'] != "")
        valid = valid and (data['horaFin'] != None or data['horaFin'] != "")
      except KeyError:
        return "Debe incluir la hora de inicio y la hora de fin", 400

      if not valid:
        return "Rellene los campos vacíos", 400

      #Verificar expresión regular y que las horas sean menores que 24
      valid = valid and re.search(TIME_REGEX, data['horaInicio']) and int(data['horaInicio'].split(":")[0]) < 24
      if not valid:
        return "El formato de la hora de inicio es incorrecto", 400

      valid = valid and re.search(TIME_REGEX, data['horaFin']) and int(data['horaFin'].split(":")[0]) < 24
      if not valid:
        return "El formato de la hora de fin es incorrecto", 400
      
      horaInicio = data['horaInicio']
      horaFin = data['horaFin']
      
      try:
        valid = valid and (data['nuevoInicio'] != None or data['nuevoInicio'] != "")
        valid = valid and (data['nuevoFin'] != None or data['nuevoFin'] != "")
      except KeyError:
        return "Debe incluir la nueva hora de inicio y la nueva hora de fin", 400

      if not valid:
        return "Rellene los campos vacíos", 400

      #Verificar expresión regular y que las horas sean menores que 24
      valid = valid and re.search(TIME_REGEX, data['nuevoInicio']) and int(data['nuevoInicio'].split(":")[0]) < 24
      if not valid:
        return "El formato de la nueva hora de inicio es incorrecto", 400

      valid = valid and re.search(TIME_REGEX, data['nuevoFin']) and int(data['nuevoFin'].split(":")[0]) < 24
      if not valid:
        return "El formato de la nueva hora de fin es incorrecto", 400
      
      nuevoInicio = data['nuevoInicio']
      nuevoFin = data['nuevoFin']

      user = db.users.find_one({'auth0_id' : session['PROFILE_KEY']['user_id']})
      if user == None:
        return "No hay ninguna unidad con ese nombre o inmueble con ese ID", 404
      hPermitidos = user['horariosPermitidos']
      if hPermitidos == None or len(hPermitidos)==0:
        return "El horario a cambiar no existe", 400
      
      band = False
      for hper in hPermitidos:
        if hper['horaInicio'] == horaInicio and hper['horaFin'] == horaFin:
          hper['horaInicio'] = nuevoInicio
          hper['horaFin'] = nuevoFin
          band = True
          break
      
      if not band:
        return "El horario a cambiar no existe", 400
      
      result = db.users.find_one_and_update({'auth0_id' : session['PROFILE_KEY']['user_id']},
      {'$set': {'horariosPermitidos': hPermitidos}},
      return_document=ReturnDocument.AFTER)
      if result == None:
        return "No hay ninguna unidad con ese nombre o inmueble con ese ID", 404
      message = '{"usuario":"'+username+'","operacion":2, "horaInicio":"'+horaInicio+'", "horaFin":"'+horaFin+'", "nuevoInicio":"'+nuevoInicio+'", "nuevoFin":"'+nuevoFin+'"}'
      topic = "Centro/"+elScope+"/horarios"
      print(message)
      mqtt.publish(topic, message.encode('utf-8'))
      return dumpJson(result)
    #hperm = hPermitidos[0]
    #horaInicioAnterior = hperm['horaInicio']
    #horaFinAnterior = hperm['horaFin']
    #message = ', "horaInicio":"'+horaInicioAnterior+'","horaFin":"'+horaFinAnterior+'"'
    elif data['esBorrado'] == 1:
      if request.data == None or request.data == "":
        return "Debe enviar información", 400
      data = loads(request.data).decode('utf-8')
      valid = True
      try:
        valid = valid and (data['horaInicio'] != None or data['horaInicio'] != "")
        valid = valid and (data['horaFin'] != None or data['horaFin'] != "")
      except KeyError:
        return "Debe incluir la hora de inicio y la hora de fin", 400

      if not valid:
        return "Rellene los campos vacíos", 400

      #Verificar expresión regular y que las horas sean menores que 24
      valid = valid and re.search(TIME_REGEX, data['horaInicio']) and int(data['horaInicio'].split(":")[0]) < 24
      if not valid:
        return "El formato de la hora de inicio es incorrecto", 400

      valid = valid and re.search(TIME_REGEX, data['horaFin']) and int(data['horaFin'].split(":")[0]) < 24
      if not valid:
        return "El formato de la hora de fin es incorrecto", 400
      
      horaInicio = data['horaInicio']
      horaFin = data['horaFin']
      
      user = db.users.find_one({'auth0_id' : session['PROFILE_KEY']['user_id']})
      if user == None:
        return "No hay ninguna unidad con ese nombre o inmueble con ese ID", 404
      hPermitidos = user['horariosPermitidos']
      if hPermitidos == None or len(hPermitidos)==0:
        return "El horario a eliminar no existe", 400
      
      sanitizedData = {}
      sanitizedData['horaInicio'] = horaInicio
      sanitizedData['horaFin'] = horaFin
      if sanitizedData in hPermitidos:
        hPermitidos.remove(sanitizedData)
      else:
        return "El horario a eliminar no existe", 400
      result = db.users.find_one_and_update({'auth0_id' : session['PROFILE_KEY']['user_id']},
      {'$set': {'horariosPermitidos': hPermitidos}},
      return_document=ReturnDocument.AFTER)
      if result == None:
        return "No hay ninguna unidad con ese nombre o inmueble con ese ID", 404
      message = '{"usuario":"'+username+'","operacion":3, "horaInicio":"'+horaInicio+'", "horaFin":"'+horaFin+'"}'
      topic = "Centro/"+elScope+"/horarios"
      print(message)
      mqtt.publish(topic, message.encode('utf-8'))
      return dumpJson(result)
    else:
      return "La operación dada no es válida", 400
  elif request.method == DELETE:
    return "holi", 200


@app.route("/unidadesResidenciales/<unidad>/emergencias", methods=[GET])
@requires_auth(SECURITY)
def emergenciasUnidad(unidad):
  if request.method == GET:
    respuesta = []
    unidadRes = db.unidadesResidenciales.find_one({ 'nombre' : unidad })
    if unidadRes == None:
      return "[]"
    try:
      for inmueble in unidadRes['inmuebles']:
        try:
          respuesta.append(inmueble['hub']['cerradura']['emergencias'])
        except KeyError as error:
          print(inmueble['localID'], ' no tiene ', str(error.args))
    except TypeError as error:
        print(inmueble['localID'], ' no tiene ', str(error.args))
    return dumpJson(respuesta)

@app.route("/yale/emergencias", methods=[GET])
@requires_auth(YALE)
def yaleEmergencias():
    respuesta = []
    #Encontrar todas las unidades residenciales
    for doc in db.unidadesResidenciales.find():
      try:
        #Por cada in mueble en cada unidad residencial
        for inmueble in doc['inmuebles']:
          try:
          #Agregar las emergencias a la respuesta
            respuesta += inmueble['hub']['cerradura']['emergencias']
          except KeyError as error:
            print(inmueble['localID'], ' no tiene ', str(error.args))
      except TypeError as error:
        print(inmueble['localID'], ' no tiene ', str(error.args))
    #Retornar JSON
    return dumpJson(respuesta)

@app.route('/yale/users')
@requires_auth(YALE)
def listarUsuarios():
  respuesta = []
  for doc in db.users.find():
    respuesta.append(doc)
  return dumpJson(respuesta)

@app.route('/users/checkAuth0/<ur_name>/<auth0_id>', methods=[GET])
@requires_auth(SECURITY)
def checkAuth0(ur_name, auth0_id):
  print('auth0_id: ', auth0_id)
  unidad = db.unidadesResidenciales.find_one({ 'nombre' : ur_name })
  respuesta = {}
  for inmueble in unidad['inmuebles']:
    try:
      if inmueble['owner_user_id'] == auth0_id: #If there is someone in the UR with that auth0_id, return their data
        user = db.users.find_one({'auth0_id': auth0_id})
        return dumpJson(user)
    except KeyError:
      print('missing owner_user_id: ', inmueble['localID'])
  return dumpJson(respuesta), 404

@app.route('/users/<usuario>', methods=[GET, PUT, DELETE])
@requires_auth(USER)
def usuario(usuario):
  data = {}
  if request.data:
    data = loads(request.data).decode('utf-8')
  if request.method == GET:
    user = db.users.find_one({'username': usuario})
    return dumpJson(user)
  elif request.method == PUT:
    name = data['nombre']
    phone = data['telefono']
    age = data['edad']
    user = db.users.find_one_and_update({"username": usuario}, {'$set' : {'nombre': name, 'telefono': phone, 'edad': age}}, return_document=ReturnDocument.AFTER)
    return dumpJson(user)
  elif request.method == DELETE:
    user = db.users.find_one_and_update({"username": usuario}, {'$set' : {'group': DISABLED}}, return_document=ReturnDocument.AFTER)
    return dumpJson(user)

@app.route('/unidadesResidenciales/<unidad>/reporteMensual/<mesReporte>', methods=[GET])
@requires_auth(UR_ADMIN)
def reportesUnidadResidencial(unidad, mesReporte):
  emergencias = []
  mes = 0
  try:
    mes = int(mesReporte)
  except Exception:
    return "Formato incorrecto del mes. Se esperaba un entero", 400
  unidadResidencial = db.unidadesResidenciales.find_one({ 'nombre' : unidad })
  if not unidadResidencial:
    return "Unidad no encontrada", 404
  
  for inmueble in unidadResidencial['inmuebles']:
    try:
    #Agregar las emergencias a la respuesta
      respuesta = inmueble['hub']['cerradura']['emergencias']
      for emergencia in respuesta:
        try:
          if int(emergencia['fecha'].split('-')[1]) == mes:
            emergencias.append(emergencia)
        except IndexError:
          pass
    except KeyError as error:
      print(inmueble['localID'], ' no tiene ', str(error.args))
  
  return dumps(emergencias)
  
@app.route("/unidadesResidenciales/<unidad>/inmuebles/<localID>/reporteMensual/<mesReporte>", methods=[GET])
@requires_auth(PROPERTY_OWNER)
def reportesInmuebles(unidad, localID, mesReporte):
  if request.method == GET:
    emergencias = []
    respuesta = []
    try:
      mes = int(mesReporte)
    except Exception:
      return "Formato incorrecto del mes. Se esperaba un entero", 400
    unidadRes = db.unidadesResidenciales.find_one({ 'nombre' : unidad })
    if unidadRes == None:
      return "No existe la unidad residencial", 404
    for inmueble in unidadRes['inmuebles']:
      if inmueble['localID'] == localID:
        respuesta = inmueble
        break
    if respuesta == []:
      return "No existe el inmueble '" + localID + "' dentro de la unidad residencial '" + unidad + "'", 404
    elif respuesta['hub'] == {}:
      return "El inmueble no tiene un hub asociado", 404
    elif respuesta['hub']['cerradura'] == {}:
      return "El inmueble no tiene una cerradura asociada", 404
    for emergencia in respuesta['hub']['cerradura']['emergencias']:
      try:
        if int(emergencia['fecha'].split('-')[1]) == mes:
          emergencias.append(emergencia)
      except IndexError:
        pass    
    return dumps(emergencias)


def dumpJson(obj):
  return dumps(obj, json_options=CANONICAL_JSON_OPTIONS)
