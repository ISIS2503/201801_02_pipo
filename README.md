# 201810_02_pipo

## Integrantes

+ Juan Sebastián Díaz Serrano - 201532686
+ Carlos Mario Sarmiento Pinilla - 201512466
+ Sergio Eduardo Cárdenas Landazábal - 201613444
+ Sergio Guzmán Mayorga - 201614859
+ Julián Alberto Manrique Puerto - 201615449

## EXPERIMENTO I INTERMEDIO:
+ Para esta entrega se usó la máquina virtual con ip 172.24.42.33 del estudiante Sergio Guzmán.
+ El programa P se encuentra en la carpeta de entidad virtual y al haberse construido con maven se le de hacer clean and build antes de correrlo.
+ LINK DE LA ENTREGA: https://youtu.be/zIY5MJsavyg
### Para esta entrega se hizo la siguiente repartición de roles:
+ Entidad física (preparación): Juan Sebastián Díaz y Carlos Mario Sarmiento. Como tal no hubo commits de esta parte.
+ Entidad física (código de arduino): Sergio Cárdenas y Julián Manrique. Como todo se trabajó desde la máquina local de Sergio, él fue el responsable de hacer commits de esta parte.
+ Entidad virtual (Node-red y Programa P): Sergio Guzmán. Él se encargó de hacer commits relacionados con la creación de flujos y el programa P.
Se hace la especificación de esta repartición para justificar la no uniformidad de los commits realizados y de cierta manera informar que todo el grupo trabajó de forma equitativa.
## EXPERIMENTO I FINAL: 
+ El diagrama de despliegue de esta entrega se encuentra en la documentacin.
+ El software del Bridge, del programa P1 y P2 se encuentra en la carpeta de la entidad virtual bajo la subcarpeta de Mensajera.
+ El REST Mock se encuentra en la carpeta de entidad virtual. Tiene 3 operaciones particulares: GET (Retorna 200), POST (Escribe mensajes en un archivo) y PUT (Activa el modo de escritura sobre el archivo).
+ En la carpeta de persistencia se encuentran los servicios REST hechos en FLASK junto con sus colecciones. 
+ Link de la entrega: https://www.youtube.com/watch?v=yYp-H7bFBOI&feature=youtu.be
+ Para este aparte particular se va a tener una matriz de esfuerzos en la carpeta docs para simbolizar cual fue el aporte de cada integrante del grupo. A su vez el documento final está en dicha carpeta.

## EXPERIMENTO II INTERMEDIO: 
+ El link de la parte de la entidad física se encuentra acá: https://youtu.be/YIpmc0j0udE 
+ El alcance de la entidad física se encuentra en la carpeta entidadFisica, mientras que el aseguramiento de servicios se encuentra en entidadVirtual/persistencia/servicios
+ Se tomó como decisión de diseño que la operacin de actualizar claves, agregar usuarios y loggearse fueran hechas con el API de Auth0. En la base de datos de mongo se persiste la información relevante del usuario (correo, username, id de auth0, rol, scope).
+ Se modificó el flujo de node red para simular el cambio de claves en el arduino. Este flujo es llamado por el programa RestClavesCerradura/cerradura/cerradura.servicios

## EXPERIMENTO II FINAL:
+ El link de la parte de la entidad física se encuentra acá: https://youtu.be/1vRMXkxcLVo
+ El alcance de la entidad física se encuentra en la carpeta entidadFisica, mientras que el aseguramiento de servicios se encuentra en entidadVirtual/persistencia/servicios
+ Los usuarios y claves, junto con sus permisos y el script de redis se tienen en la carpeta entidadFisica
+ Los resultados de las nuevas pruebas de carga se encuentran en la carpeta docs junto con el esfuerzo del experimento
+ El servicio de verificación del HealthCheck del hub se implementó como un loop infinito que se inicia con un servicio rest en el RestMOCK
+ La activación y desactivación de alarmas se agregó al REST de claves como una funcionalidad que impacta directamente al hub
+ Se asume que cada inmueble solo tiene un propietario y que todas las claves del Arduino son de este propietario

## EXPERIMENTO III FINAL:
+ El link de todo el experimento realizado está acá: 
+ Se modificó la entidad física para que se mande el mensaje de apertura con <Id de arduino>\t0\t<Timeout>\t<Clave>
+ Se modificó Node Red para que con cada cambio en los servicios de horarios y de claves se modifique la BD interna del Hub
+ Aprovechando la BD con la que se conectaba mosquitto en el Hub, se usó la misma para poder comunciarse con Redis y validar claves y horarios
+ P1 y P2 ahora también procesan fallos y los pasan a sus respectivos flujos
+ La interfaz se realizó en la carpeta Dashboard
+ El SAD se puede encontrar en la carpeta docs junto con la matriz de esfuerzos
+ El programa que simula el loop infinito de "Yale" se dejó como un programa simple en java que se comunica por MQTT asegurado en la carpeta entidadVirtual/Mensajeria
+ Se creó un flujo aparte de hub "testFlow.json" para bombardear el speed que muestra en tiempo real eld ashboard de seguridad.
