from bson.json_util import dumps, loads, ObjectId, CANONICAL_JSON_OPTIONS
import base64
from datetime import datetime
import sys
import redis
import json
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
    auth = request.headers.get('Authorization')
    token = auth.split(' ')[1]
    data = base64.b64decode(token).decode("utf-8").split(':')
    username = data[0]
    print(username,data[1])
    password = bytes(data[1].strip()).encode('utf-8')
    print (password)
    m  = hashlib.md5(password)
    print("PASS",m.hexdigest())
    print("data: ",data,password)
    redis=r.get(username).decode('utf-8')
    print("REDIS",redis)
    digest=m.hexdigest()
    print("DIGEST",digest)
    if redis == digest:
        response.status_code = 200
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
    data=loads(request.data.decode('utf-8'))
    clave=data['clave']
    print(r.get('C:'+str(clave)))
    print(r.get(r.get('C:'+str(clave))))
    horarios=r.get((r.get('C:'+str(clave)))).decode('utf-8').split(',')
    for h in horarios:
        print(h)
        tiempoInicial=h.split('-')[0].split(':')
        tiempoFinal=h.split('-')[1].split(':')
        print(tiempoInicial,tiempoFinal)
        start_time = int(tiempoInicial[0])*60 + int(tiempoInicial[1])
        end_time = int(tiempoFinal[0])*60 + int(tiempoFinal[1])
        #Agregado el 7 por la diferencia horaria de la máquina de aws
        hour=datetime.now().hour-5
        if hour<0:
          hour=24+hour
        current_time = hour*60 +datetime.now().minute
        print(hour,datetime.now().minute)
        print(start_time,current_time,end_time)
        if start_time <= current_time and end_time >= current_time:
            response.status_code=200
            break 
    return response

@app.route('/passwordAccess', methods=['POST','PUT','DELETE'])
def passwordAccess():
    print(request.data)
    response =  Response(content_type='text/plain', status=500)
    data=loads(request.data.decode('utf-8'))
    clave=data.get('clave')
    usuario=data['usuario']
    numero=str(data['numero'])
    print(clave,usuario)
    if clave != None and clave !="":
        viejo = r.get('C:'+str(clave))
        claveAntigua=r.get('N:'+numero)
        print ("HOLA",viejo,claveAntigua)
        if (claveAntigua==None) and (request.method == 'PUT' or request.method == 'DELETE'):
            return response
        print("VIEJO",viejo)
        if request.method == 'POST':
            if claveAntigua!=None and claveAntigua!="":
               r.rename('C:'+claveAntigua.decode('utf-8'),'C:'+str(clave))
            r.set('C:'+str(clave),'U:'+usuario)
            r.set('N:'+numero,str(clave))
            response.status_code=200
        elif request.method == 'PUT':
            if clave==None or clave=='' or(claveAntigua==None or claveAntigua ==""):
                return response
            claveAntigua=claveAntigua.decode('utf-8')
            r.set('N:'+numero,str(clave))
            r.rename('C:'+claveAntigua.decode('utf-8'),'C:'+str(clave))
            response.status_code=200
    else:
        if request.method != 'DELETE':
            return response
        if numero!="" and numero !=None:
            r.delete("C:"+r.get("N:"+numero).decode('utf-8'))
            r.delete("N:"+numero)
            response.status_code=200
        else:
          for key in r.keys('*'):
              print(key,r.get(key).decode('utf-8'))
              if r.get(key).decode('utf-8')==('U:'+usuario):
                  r.delete(key)
          for i in range (1,20):
              r.delete('N:'+str(i))
          response.status_code=200
    return response

@app.route('/scheduleAccess', methods=['POST','PUT','DELETE'])
def scheduleaccess():
    print(request.data)
    response =  Response(content_type='text/plain', status=500)
    data=loads(request.data.decode('utf-8'))
    horaInicio=data['horaInicio']
    horaFin=data['horaFin']
    usuario=data['usuario']
    print(horaInicio,horaFin,usuario)
    if usuario != None:
        completo=str(horaInicio)+"-"+str(horaFin)
        viejo = r.get('U:'+str(usuario)).decode('utf-8')
        print (viejo)
        if viejo == None and (request.method == 'PUT' or request.method == 'DELETE'):
            return response
        if viejo==None and request.method=='POST':
            r.set('U:'+str(usuario),completo)
            response.status_code=200
        else:
            nuevoInicio=data.get('nuevoInicio')
            nuevoFin=data.get('nuevoFin')
            if completo not in viejo:
                if request.method=='POST':
                    viejo+=(","+completo)
                r.set('U:'+str(usuario),viejo)
                response.status_code=200
            else:
                if request.method=='DELETE':
                    remplazo=''
                    viejo=viejo.replace(','+completo,remplazo)
                    viejo=viejo.replace(completo+',',remplazo)
                elif request.method=='PUT' and nuevoInicio!="" and nuevoInicio!=None and nuevoFin!='' and nuevoFin!=None :
                    nuevoInicio=data['nuevoInicio']
                    nuevoFin=data['nuevoFin']
                    remplazo=str(nuevoInicio)+"-"+str(nuevoFin)
                    viejo=viejo.replace(','+completo,','+remplazo)
                    viejo=viejo.replace(completo+',',remplazo+',')
                r.set('U:'+str(usuario),viejo)
                response.status_code=200
    return response


if __name__ == '__main__':
    app.run(port=8082,host='localhost')
