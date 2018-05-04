import base64
import sys
import hashlib
import redis
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
 
if __name__ == '__main__':
	app.run()