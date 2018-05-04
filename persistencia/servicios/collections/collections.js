//Importa el json al HTML con el nombre de la variable "collections"
var collections = 
[
  {
    "nombre": "Propietario - Toscana",
    "peticiones": [
      {
        "method": "GET",
        "url": "http://172.24.42.64/unidadesResidenciales/Toscana/inmuebles/1234",
        "body": ""
      },
      {
        "method": "PUT",
        "url": "http://172.24.42.64/unidadesResidenciales/Toscana/inmuebles/1234",
        "body": "{\"localID\" : \"1234\"}"
      },
      {
        "method": "DELETE",
        "url": "http://172.24.42.64/unidadesResidenciales/Toscana/inmuebles/1234",
        "body": ""
      },
      {
        "method": "GET",
        "url": "http://172.24.42.64/unidadesResidenciales/Toscana/inmuebles/1234/hub",
        "body": ""
      },
      {
        "method": "POST",
        "url": "http://172.24.42.64/unidadesResidenciales/Toscana/inmuebles/1234/hub",
        "body": "{\"frecuencia\" : 10, \"fallosMaximos\" : 3, \"zona\" : \"norte\"}"
      },
      {
        "method": "PUT",
        "url": "http://172.24.42.64/unidadesResidenciales/Toscana/inmuebles/1234/hub",
        "body": "{\"frecuencia\" : 15, \"fallosMaximos\" : 4, \"zona\" : \"norte\"}"
      },
      {
        "method": "GET",
        "url": "http://172.24.42.64/unidadesResidenciales/Toscana/inmuebles/1234/hub/cerradura",
        "body": ""
      },
      {
        "method": "POST",
        "url": "http://172.24.42.64/unidadesResidenciales/Toscana/inmuebles/1234/hub/cerradura",
        "body": "{\"bateriaCritica\" : 10, \"tiempoMaximo\" : 90, \"frequencia\" : 4, \"fallosMaximos\" : 3}"
      },
      {
        "method": "PUT",
        "url": "http://172.24.42.64/unidadesResidenciales/Toscana/inmuebles/1234/hub/cerradura",
        "body": "{\"bateriaCritica\" : 15, \"tiempoMaximo\" : 60, \"frequencia\" : 10, \"fallosMaximos\" : 5}"
      },
      {
        "method": "DELETE",
        "url": "http://172.24.42.64/unidadesResidenciales/Toscana/inmuebles/1234/hub/cerradura",
        "body": ""
      },
      {
        "method": "GET",
        "url": "http://172.24.42.64/unidadesResidenciales/Toscana/inmuebles/1234/hub/cerradura/claves",
        "body": ""
      },
      {
        "method": "POST",
        "url": "http://172.24.42.64/unidadesResidenciales/Toscana/inmuebles/1234/hub/cerradura/claves",
        "body": "{\"combinacion\" : \"1234\"}"
      },
      {
        "method": "PUT",
        "url": "http://172.24.42.64/unidadesResidenciales/Toscana/inmuebles/1234/hub/cerradura/claves",
        "body": "{\"combinacion\" : \"5678\"}"
      },
      {
        "method": "DELETE",
        "url": "http://172.24.42.64/unidadesResidenciales/Toscana/inmuebles/1234/hub/cerradura/claves",
        "body": "{\"clave\" : \"1234\"}"
      },
      {
        "method": "GET",
        "url": "http://172.24.42.64/unidadesResidenciales/Toscana/inmuebles/1234/hub/cerradura/emergencias",
        "body": ""
      },
      {
        "method": "GET",
        "url": "http://172.24.42.64/unidadesResidenciales/Toscana/inmuebles/1234/hub/cerradura/horariosPermitidos",
        "body": ""
      },
      {
        "method": "POST",
        "url": "http://172.24.42.64/unidadesResidenciales/Toscana/inmuebles/1234/hub/cerradura/horariosPermitidos",
        "body": "{\"horaInicio\" : \"10:00\", \"horaFin\" : \"3:00\"}"
      },
      {
        "method": "DELETE",
        "url": "http://172.24.42.64/unidadesResidenciales/Toscana/inmuebles/1234/hub/cerradura/horariosPermitidos",
        "body": ""
      },
      {
        "method" : "GET",
        "url" : "http://172.24.42.64/unidadesResidenciales/Toscana/inmuebles/1234/reporteMensual/5",
        "body" : ""
      },
      {
        "method": "DELETE",
        "url": "http://172.24.42.64/unidadesResidenciales/Toscana/inmuebles/1234/hub",
        "body": ""
      }
    ]
  },
  {
    "nombre": "Seguridad - Toscana",
    "peticiones": [
      {
        "method": "GET",
        "url": "http://172.24.42.64/unidadesResidenciales/Toscana/emergencias",
        "body": ""
      }
    ]
  },
  {
    "nombre": "Administrador UR - Toscana",
    "peticiones": [
      {
        "method": "GET",
        "url": "http://172.24.42.64/unidadesResidenciales/Toscana",
        "body": ""
      },
      {
        "method": "PUT",
        "url": "http://172.24.42.64/unidadesResidenciales/Toscana",
        "body": "{\"nombre\" : \"Toscana\", \"direccion\" : \"Cll 19 # 3-32\"}"
      },
      {
        "method": "GET",
        "url": "http://172.24.42.64/unidadesResidenciales/Toscana/inmuebles",
        "body": ""
      },
      {
        "method": "POST",
        "url": "http://172.24.42.64/unidadesResidenciales/Toscana/inmuebles",
        "body": "{\"localID\" : \"201\", \"owner\" : \"Pepito Perez\", \"owner_user_id\" : \"user\"}"
      },
      {
          "method" : "GET",
          "url" : "http://172.24.42.64/unidadesResidenciales/Toscana/reporteMensual/5",
          "body" : ""
      },
      {
          "method" : "DELETE",
          "url" : "http://172.24.42.64/unidadesResidenciales/Toscana",
          "body" : ""
      }
    ]
  },
  {
    "nombre": "Usuario CRUD - js.diaz",
    "peticiones": [
      {
        "method": "GET",
        "url": "http://172.24.42.64/users/js.diaz",
        "body": ""
      },
      {
        "method": "PUT",
        "url": "http://172.24.42.64/users/js.diaz",
        "body": ""
      },
      {
        "method": "DELETE",
        "url": "http://172.24.42.64/users/js.diaz",
        "body": ""
      }
    ]
  },
  {
    "nombre": "Yale - usuarios/emerg/UR",
    "peticiones": [
      {
        "method": "GET",
        "url": "http://172.24.42.64/yale",
        "body": ""
      },
      {
        "method": "POST",
        "url": "http://172.24.42.64/unidadesResidenciales",
        "body": "{\"nombre\" : \"Andes\",\"direccion\" : \"Cra 3 # 19-91\", \"owner_user_id\" : \"user\", \"security_user_id\" : \"user1\", \"inmuebles\" : []}"
      },
      {
        "method": "GET",
        "url": "http://172.24.42.64/yale/emergencias",
        "body": ""
      },
      {
        "method": "GET",
        "url": "http://172.24.42.64/yale/users",
        "body": ""
      }
    ]
  }
];