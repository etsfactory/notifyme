<p align="center"><img width="100" src="./logo.png" alt="Notifyme logo"></p>

# Notifyme

Notify.me es un servicio creado en python para el manejo de notificaciones a usuarios de mensajes del bus de RabbitMQ. En principio las notificaciones se envían al email de los usuarios. La aplicación, mediante API, permite crear y modificar usuarios, así como tipos de notificaciones a los que los usuarios se pueden suscribir. Además se permite crear templates (plantillas para las notificaciones) de tal forma que se puede indicar en el mensaje y el asunto de la notificatión variables que porvengan en el mensaje del bus.

Notify.me crea una cola desde la que se conecta a los exchanges del bus que el usuario indique, de la forma que cuando llega un mensaje a uno de los exchanges conectados envía una notificación a los usuarios suscritos.

## Getting Started

Las instrucciones que vas a leer a continuación sirven para ejecutar notify.me en tu máquina para poder desarrollar en local o en una máquina de producción.

### Prerrequisitos

Para poder ejecutar notify.me necesitas una base de datos rethinkDB. Además necesitas tener funcionando un bus RabbitMQ del que poder recibir las notificaciones. 

Para instalar rethinkDB:
[Instalación de la base de datos rethinkDB](https://rethinkdb.com/docs/install/)

Para instalar rabbitMQ:
[Instalación del bus rabbitMQ](https://www.rabbitmq.com/download.html)

Otra opción recomensable es ejecutar rethinkDB y rabbitMQ desde sus contenedores oficiales en docker.

Por último, tienes que tener instalado **python3**.

### Instalación y configuración

Para ejecutar notifyme descarga este repositorio en tu máquina. Una vez descargado ejecuta en una terminal de comandos:

```bash
pip install -r requirements.txt
```

La configuración de notifyme se hace desde su fichero de **config.json** o mediante variables de entorno. La configuración está preparada para que puedas incluir directamente el valor que de cada variable o para que puedas incluir una ruta a un fichero externo config.ini indicando el nombre y su sección, por ejemplo: /configs/seccion/nombre_variable.

El nombre de las variables de entorno están definidas dentro del fichero **settings.py**

Variables que puedes definir:

- Bus:
    - host: La dirección ip del bus de rabbitMq
    - user: El usuario que has definido para rabbitmq (el que crea por defecto rabbitmq es *guest*)
    - password: La contraseña que has definido para el user de rabbitmq (el que se crea por defecto es *guest*)
    - queue_name: El nombre de la cola que va a crear notifyme en el bus para conectarse a los exchanges
    - error_exchange: El nombre de la cola de error para enviar mensajes de error

- SMTP
    - server: La dirección del SMTP para enviar los emails
    - port: El puerto desl servidor SMTP
    - email: Email del STMP desde el que sen envían los correos
    - password: Contraseña del email para enviar los correos
    - send_emails: Boolean, para bloquear el envío de emails
    - name: Nombre para mostrar en el remitente 
    - ttls: Boolea, para activar la conexión mediante ttls al servidor stmp 

- loggin
    - Dirección en la maquina para escribir los mensajes de log (tiene que existir una carpeta con el nombre notifyme y dentro un archivo notifyme.log)

- db
    - server: La dirección de la base de datos rethinkdb que has creado en la máquina
    - port: Puerto de la base de datos que has creado
    - refresh_database: Por si quieres reiniciar la base de datos cada vez que se inicia el servicio
    - user: User de la base de datos
    - password: Contraseña de la base de datos

- api
    - server: Dirección en la que se va a poner a escuchar la API
    - port: Puerto en el que se va a poner a escuchar la API

- default_template
    - text: Texto de la notificatión cuando se usa el template por defecto
    - subject: Asunto del template por defecto

Para arrancar el servicio ejecutar:

```bash
python3 notifyme.py
```

El servicio al arrancar crea las tablas de la base de datos en caso que no existan y configura una API en la dirección especificada en el fichero de configuración.

Para más información sobre las llamadas de la API que se crean echa un vistazo a la [documentación](https://etsfactory.github.io/notify.me)

## Contribuciones

Por favor lee: [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles y para saber cómo enviar peticiones de cambios.

## Autores

* **Diego López García** - [Github](https://github.com/Frostqui)

## Licencia

Este proyecto tiene una licencia GNU, echa un vistazo a [LICENSE](LICENSE) para más detalles.
