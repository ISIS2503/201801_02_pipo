from flask import Flask, render_template, jsonify
from pymongo import MongoClient
from bson.json_util import dumps, CANONICAL_JSON_OPTIONS
import json

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

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/yale")
def yale():
    respuesta = []
    #Encontrar todos las unidades residenciales
    for doc in db.unidadesResidenciales.find():
      #Agregar cada una al objeto
      respuesta.append(doc)
    #Retornar JSON
    return dumps(respuesta, json_options=CANONICAL_JSON_OPTIONS)

@app.route("/unidadesResidenciales/<unidad>")
def unidadResidencial(unidad):
  respuesta = []
  #Encontrar todos las unidades residenciales
  for doc in db.unidadesResidenciales.find({"nombre" : unidad}):
    #Agregar cada una al objeto (si es que encontró)
    respuesta.append(doc)
  #Retornar JSON
  return dumps(respuesta, json_options=CANONICAL_JSON_OPTIONS)
  