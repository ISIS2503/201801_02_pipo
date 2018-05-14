import base64
from datetime import datetime
import sys
import hashlib
import redis
from bson.json_util import dumps, loads, ObjectId, CANONICAL_JSON_OPTIONS
from flask import Flask,Response,request
 
app = Flask(__name__)
r = redis.Redis()
roles=['Lector','Escritor']
 
@app.route('/auth', methods=['POST'])
def auth():
    response = Response(content_type='text/plain', status=403)
    print("R",request.data)
    print("H",request.headers)
    print("F",request.form)
    print("A",request.args)
    print("REQ",request)
    try:
      auth = request.headers.get('Authorization')
      token = auth.split(' ')[1]
      data = base64.b64decode(token).decode("utf-8").split(':')
      username = data[0]
      password = bytes(data[1].strip(),'utf-8')
      m  = hashlib.md5(password)
      print("PASS",m.hexdigest())
      print("data: ",data,password)
      redis=r.get(username).decode('utf-8')
      print("REDIS",redis)
      digest=m.hexdigest()
      print("DIGEST",digest)
      if redis == digest:
          response.status_code = 200
    except:
      pass
    return response

@app.route('/superuser', methods=['POST'])
def superuser():
    print("DATA")
    response =  Response(content_type='text/plain', status=403)
    try:
      auth = request.headers.get('Authorization')
      token = auth.split(' ')[1]
      print(token)
      data = base64.b64decode(token).decode("utf-8").split(':')
      username = data[0]
      if username == 'microcontrolador':
          response.status_code = 200
    except:
      pass
    return response
 
@app.route('/acl', methods=['POST'])
def acl():
    print("DDDATA")
    response =  Response(content_type='text/plain', status=403)
    try:
      print("R",request.data)
      print("H",request.headers)
      print("F",request.form)
      print("A",request.args)
      print("REQ",request)
      auth = request.headers.get('Authorization')
      token = auth.split(' ')[1]
      data = base64.b64decode(token).decode("utf-8").split(':')[0]
      print("ENTRA")
      rol=request.form.get('acc')
      print(rol)
      print("ROLES",r.get(request.form.get("topic")).decode('utf-8').split(":"))
      for i in range(0,int(rol)):
     	 if(data[0] in r.get(request.form.get("topic")).decode('utf-8').split(":")[i]):
               response.status_code = 200
    except:
      pass
    return response
#Added functionalities for communication with redis
@app.route('/arduinoAccess', methods=['POST'])
def arduinoaccess():
    print(request.data)
    response =  Response(content_type='text/plain', status=500)
    data=loads(request.data)
    clave=data['clave']
    print(r.get('C:'+str(clave)))
    print(r.get(r.get('C:'+str(clave))))
    horarios=r.get((r.get('C:'+str(clave)))).split(',')
    for h in horarios:
     print(h)
     tiempoInicial=h.split('-')[0].split(':')
     tiempoFinal=h.split('-')[1].split(':')
     print(tiempoInicial,tiempoFinal)
     start_time = int(tiempoInicial[0])*60 + int(tiempoInicial[1])
     end_time = int(tiempoInicial[1])*60 + int(tiempoFinal[1])
     current_time =  datetime.now().hour*60 +datetime.now().minute
     if start_time <= current_time and end_time >= current_time:
        response.status_code=200
        break 
    return response

@app.route('/passwordAccess', methods=['POST','PUT','DELETE'])
def passwordAccess():
    print(request.data)
    response =  Response(content_type='text/plain', status=500)
    data=loads(request.data)
    clave=data.get('clave')
    usuario=data['usuario']
    numero=str(data['numero'])
    print(clave,usuario)
    if clave != None and clave !="":
      viejo = r.get('C:'+str(clave))
      claveAntigua=r.get('N:'+numero)
      print (viejo,claveAntigua)
      if (claveAntigua==None) and (request.method == 'PUT' or request.method == 'DELETE') or (claveAntigua!=None and request.method == 'POST'):
        return response
      if request.method == 'POST' and (viejo==None or viejo==""):
        r.set('C:'+str(clave),'U:'+usuario)
        r.set('N:'+numero,str(clave))
        response.status_code=200
      elif request.method == 'PUT':
        
        if clave==None or clave=='' or(claveAntigua==None or claveAntigua ==""):
          return response
	print('ENTRA')
        r.set('N:'+numero,str(clave))
        r.rename("C:"+claveAntigua,'C:'+str(clave))
        response.status_code=200
    else:
      if request.method != 'DELETE':
        return response
      if numero!="" and numero !=None:
        r.delete("N:"+numero)
        response.status_code=200
      else:
        for key in r.keys('*'):
          print(key,r.get(key))
          if r.get(key)==('U:'+usuario):
            r.delete(key)
        for i in range (1,20):
          r.delete('N:'+str(i))
        response.status_code=200
    return response

@app.route('/scheduleAccess', methods=['POST','PUT','DELETE'])
def scheduleaccess():
    print(request.data)
    response =  Response(content_type='text/plain', status=500)
    data=loads(request.data)
    horaInicio=data['horaInicio']
    horaFin=data['horaFin']
    usuario=data['usuario']
    print(horaInicio,horaFin,usuario)
    if usuario != None:
      viejo = r.get('U:'+str(usuario))
      print (viejo)
      if viejo == None and (request.method == 'PUT' or request.method == 'DELETE'):
        return response
      if request.method == 'DELETE':
        r.delete('U:'+str(usuario))
      elif request.method == 'POST' or request.method=='PUT':
        completo=str(horaInicio)+","+str(horaFin)
        if viejo==None and request.method=='POST':
          r.set('U:'+str(usuario),completo)
          response.status_code=200
        else: 
          index=viejo.index(completo)
          if index==-1:
            if request.method=='POST':
              viejo.append(","+completo)
              r.set('U:'+str(usuario),viejo)
          else:
            if request.method=='PUT':
              nuevoInicio=data['nuevoInicio']
              nuevoFin=data['nuevoFin']
              if nuevoInicio!=None and nuevoFin!=None:
                viejo.replace(completo,str(nuevoInicio+','+nuevoFin))
                r.set('U:'+str(usuario),viejo)
        return response
    return response

if __name__ == '__main__':
	app.run(port=8080,host='172.24.41.182')
