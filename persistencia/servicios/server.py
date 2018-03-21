from flask import Flask, render_template, request
from pymongo import MongoClient, ReturnDocument
from bson.json_util import dumps, loads, ObjectId, CANONICAL_JSON_OPTIONS
import json
import re

#Constantes métodos REST
GET = 'GET'
POST = 'POST'
PUT = 'PUT'
DELETE = 'DELETE'

#Expresión regular para verificar horas [00:00] - [23:59]
TIME_REGEX = r"[0-2][0-9]:[0-5][0-9]"

#Instalación en windows ---------------------
#pip install flask
#En powershell poner la siguiente línea de código:
#$env:FLASK_APP = "server.py"
#Correr ejecutando el comando "flask run" estando parado en el directorio de este archivo

#Setup de mongoDB
#Puerto: 27017
#DB: Pipo-yale-persistencia
#COL: unidadesResidenciales

client = MongoClient('localhost', 27017)
db = client['Pipo-yale-persistencia']
app = Flask(__name__)

@app.route("/", methods=[GET])
def hello():
    return render_template("index.html")

@app.route("/yale", methods=[GET])
def yale():
    respuesta = []
    #Encontrar todos las unidades residenciales
    for doc in db.unidadesResidenciales.find():
      #Agregar cada una al objeto
      respuesta.append(doc)
    #Retornar JSON
    return dumpJson(respuesta)

@app.route("/unidadesResidenciales/<unidad>", methods=[GET, PUT, DELETE])
def unidadResidencial(unidad):
  if request.method == GET:
    respuesta = {}
    #Encontrar todos las unidades residenciales
    respuesta = db.unidadesResidenciales.find_one({"nombre" : unidad})
    #Retornar JSON
    return dumpJson(respuesta)
  elif request.method == PUT:
    #Convertir JSON a directorio python
    data = loads(request.data)
    #Verificar campos no nulos/vacíos
    valid = True
    try:
      valid = valid and (data['nombre'] != None or data['nombre'] != "")
      valid = valid and (data['direccion'] != None or data['direccion'] != "")
    except KeyError:
      return "Falta el nombre o la dirección de la unidad", 400

    try:
      valid = False and (data['inmuebles'] == [])
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
def crearUnidad():
  if request.method == POST:
    if request.data == None or request.data == "":
      return "Debe enviar información", 400

    data = loads(request.data)
    valid = True
    try:
      valid = valid and (data['nombre'] != None or data['nombre'] != "")
      valid = valid and (data['direccion'] != None or data['direccion'] != "")
    except KeyError:
      return "Falta el nombre o la dirección de la unidad", 400

    try:
      valid = valid and (data['inmuebles'] == [])
      if not valid:
        return "No puede haber ningún inmueble asociado en la creación de una unidad residencial", 400
    except KeyError:
      valid = True

    if not valid:
      return "Solo el arreglo de inmuebles puede estar vacío, los demás atributos no", 400

    #Objeto nuevo para eliminar posibles campos adicionales del json
    sanitizedData = {}
    sanitizedData['nombre'] = data['nombre']
    sanitizedData['direccion'] = data['direccion']
    sanitizedData['inmuebles'] = []
    #Insertar en mongoDB
    result = db.unidadesResidenciales.insert_one(sanitizedData)
    sanitizedData['_id'] = result.inserted_id
    return dumpJson(sanitizedData)

@app.route("/unidadesResidenciales/<unidad>/inmuebles", methods=[GET, POST])
def imuebles(unidad):
  if request.method == GET:
    respuesta = []
    unidad = db.unidadesResidenciales.find_one({ 'nombre' : unidad })
    return dumpJson(unidad['inmuebles'])
  elif request.method == POST:
    if request.data == None or request.data == "":
      return "Debe enviar información", 400
    
    data = loads(request.data)
    valid = True
    try:
      valid = valid and (data['localID'] != None or data['localID'] != "")
    except KeyError:
      return "Debe incluir el identificador local del inmueble", 400

    #Objeto nuevo para eliminar posibles campos adicionales del json
    sanitizedData = {}
    sanitizedData['_id'] = ObjectId()
    sanitizedData['localID'] = data['localID']
    sanitizedData['hub'] = {}
    #Añadir al arreglo de inmuebles
    result = db.unidadesResidenciales.find_one_and_update({'nombre':unidad}, {'$push': {'inmuebles': sanitizedData}})
    return dumpJson(sanitizedData)

@app.route("/unidadesResidenciales/<unidad>/inmuebles/<localID>", methods=[GET, PUT])
def inmuebles(unidad, localID):
  if request.method == GET:
    respuesta = []
    unidad = db.unidadesResidenciales.find_one({ 'nombre' : unidad })
    #Buscar inmueble dentro de la unidad residencial
    for inmueble in unidad['inmuebles']:
      if inmueble['localID'] == localID:
        respuesta = inmueble
        break
    #Lo retorna
    return dumpJson(respuesta)
  elif request.method == PUT:
    data = loads(request.data)
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
    
    return dumpJson(nuevo)

@app.route("/unidadesResidenciales/<unidad>/inmuebles/<localID>/hub", methods=[GET, POST, PUT])
def hub(unidad, localID):
  if request.method == GET:
    respuesta = []
    unidad = db.unidadesResidenciales.find_one({ 'nombre' : unidad })
    for inmueble in unidad['inmuebles']:
      if inmueble['localID'] == localID:
        respuesta = inmueble
        break
    #Retorna solo el Hub del inmueble buscado
    return dumpJson(respuesta['hub'])
  elif request.method == POST or request.method == PUT:
    if request.data == None or request.data == "":
      return "Debe enviar información", 400
    
    data = loads(request.data)
    valid = True
    try:
      valid = valid and (data['frecuencia'] != None or data['frecuencia'] != "")
      valid = valid and (data['fallosMaximos'] != None or data['fallosMaximos'] != "")
    except KeyError:
      return "Debe incluir la frecuencia y el número de fallos máximos del inmueble", 400

    #Objeto nuevo para eliminar posibles campos adicionales del json
    sanitizedData = {}
    sanitizedData['_id'] = ObjectId()
    sanitizedData['frecuencia'] = data['frecuencia']
    sanitizedData['fallosMaximos'] = data['fallosMaximos']
    sanitizedData['fallos'] = []
    sanitizedData['cerradura'] = {}

    #Esta linea busca los documentos que tengan la propiedad nombre == unidad
    #Y luego actualiza el valor del campo inmuebles[x].hub a el nuevo hub
    #inmuebles[x] corresponde al elemento tal que inmuebles[x].localID == identificador local del inmueble
    result = db.unidadesResidenciales.find_one_and_update({'nombre': unidad,},
    {'$set': {'inmuebles.$[elemento].hub' : sanitizedData}},
    array_filters=[ {'elemento.localID': {'$eq' : localID}} ],
    return_document=ReturnDocument.AFTER)
    return dumpJson(result)

@app.route("/unidadesResidenciales/<unidad>/inmuebles/<localID>/hub/cerradura", methods=[GET, POST, PUT, DELETE])
def cerradura(unidad, localID):
  if request.method == GET:
    respuesta = []
    unidad = db.unidadesResidenciales.find_one({ 'nombre' : unidad })
    for inmueble in unidad['inmuebles']:
      if inmueble['localID'] == localID:
        respuesta = inmueble
        break
    return dumpJson(respuesta['hub']['cerradura'])
  elif request.method == POST or request.method == PUT:
    if request.data == None or request.data == "":
      return "Debe enviar información", 400
    
    data = loads(request.data)
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
    return dumpJson(result)
  elif request.method == DELETE:
    #Esta linea busca los documentos que tengan la propiedad nombre == unidad
    #Y luego actualiza el valor del campo inmuebles[x].hub a un hub vacío (Equivalente a eliminarlo)
    #inmuebles[x] corresponde al elemento tal que inmuebles[x].localID == identificador local del inmueble
    result = db.unidadesResidenciales.find_one_and_update({'nombre': unidad,},
    {'$set': {'inmuebles.$[elemento].hub.cerradura' : {}}},
    array_filters=[ {'elemento.localID': {'$eq' : localID}} ],
    return_document=ReturnDocument.AFTER)
    return dumpJson(result)

@app.route("/unidadesResidenciales/<unidad>/inmuebles/<localID>/hub/cerradura/claves", methods=[GET, POST, PUT])
def claves(unidad, localID):
  if request.method == GET:
    respuesta = []
    unidad = db.unidadesResidenciales.find_one({ 'nombre' : unidad })
    for inmueble in unidad['inmuebles']:
      if inmueble['localID'] == localID:
        respuesta = inmueble
        break
    return dumpJson(respuesta['hub']['cerradura']['claves'])
  elif request.method == POST or request.method == PUT:
    if request.data == None or request.data == "":
      return "Debe enviar información", 400
    
    data = loads(request.data)
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
    return dumpJson(result)

@app.route("/unidadesResidenciales/<unidad>/inmuebles/<localID>/hub/cerradura/emergencias", methods=[GET, POST])
def emergencias(unidad, localID):
  if request.method == GET:
    respuesta = []
    unidad = db.unidadesResidenciales.find_one({ 'nombre' : unidad })
    for inmueble in unidad['inmuebles']:
      if inmueble['localID'] == localID:
        respuesta = inmueble
        break
    return dumpJson(respuesta['hub']['cerradura']['emergencias'])
  elif request.method == POST or request.method == PUT:
    if request.data == None or request.data == "":
      return "Debe enviar información", 400
    
    data = loads(request.data)
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
    return dumpJson(result)

@app.route("/unidadesResidenciales/<unidad>/inmuebles/<localID>/hub/cerradura/horariosPermitidos", methods=[GET, POST])
def horariosPermitidos(unidad, localID):
  if request.method == GET:
    respuesta = []
    unidad = db.unidadesResidenciales.find_one({ 'nombre' : unidad })
    for inmueble in unidad['inmuebles']:
      if inmueble['localID'] == localID:
        respuesta = inmueble
        break
    return dumpJson(respuesta['hub']['cerradura']['horariosPermitidos'])
  elif request.method == POST or request.method == PUT:
    if request.data == None or request.data == "":
      return "Debe enviar información", 400
    
    data = loads(request.data)
    valid = True
    try:
      valid = valid and (data['horaInicio'] != None or data['horaInicio'] != "")
      valid = valid and (data['horaFin'] != None or data['horaFin'] != "")
    except KeyError:
      return "Debe incluir la fecha, el tipo y el id de la emergencia", 400

    if not valid:
      return "Rellene los campos vacíos", 400

    #Verificar expresión regular y que las horas sean menores que 24
    valid = valid and re.search(TIME_REGEX, data['horaInicio']) and int(data['horaInicio'].split(":")[0]) < 24
    if not valid:
      return "El formato de la hora de inicio es incorrecto", 400

    valid = valid and re.search(TIME_REGEX, data['horaFin']) and int(data['horaFin'].split(":")[0]) < 24
    if not valid:
      return "El formato de la hora de fin es incorrecto", 400

    sanitizedData = {}
    sanitizedData['horaInicio'] = data['horaInicio']
    sanitizedData['horaFin'] = data['horaFin']

    #Esta linea busca los documentos que tengan la propiedad nombre == unidad
    #Y luego inserta a el valor del campo inmuebles[x].hub.cerradura.horariosPermitidos el nuevo horario
    #inmuebles[x] corresponde al elemento tal que inmuebles[x].localID == identificador local del inmueble
    result = db.unidadesResidenciales.find_one_and_update({'nombre': unidad,},
    {'$push': {'inmuebles.$[elemento].hub.cerradura.horariosPermitidos' : sanitizedData}},
    array_filters=[ {'elemento.localID': {'$eq' : localID}} ],
    return_document=ReturnDocument.AFTER)
    return dumpJson(result)

@app.route("/unidadesResidenciales/<unidad>/emergencias", methods=[GET])
def emergenciasUnidad(unidad, localID):
  if request.method == GET:
    respuesta = []
    unidad = db.unidadesResidenciales.find_one({ 'nombre' : unidad })
    for inmueble in unidad['inmuebles']:
      respuesta.append(inmueble['hub']['cerradura']['emergencias'])
    return dumpJson(respuesta)

#TODO probar método, puede que el find no retorne objetos python entonces puede putiarse
@app.route("/yale/emergencias", methods=[GET])
def yale():
    respuesta = []
    #Encontrar todos las unidades residenciales
    for doc in db.unidadesResidenciales.find():
      #Por cada in mueble en cada unidad residencial
      for inmueble in doc['inmuebles']:
        #Agregar las emergencias a la respuesta
        respuesta += inmueble['hub']['cerradura']['emergencias']
    #Retornar JSON
    return dumpJson(respuesta)

def dumpJson(obj):
  return dumps(obj, json_options=CANONICAL_JSON_OPTIONS)
