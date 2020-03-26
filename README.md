<p align="center"><img width="250" src="./logo.png" alt="Notifyme logo"></p>

<p align="center">
  ![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)
  <br>
  ![Python](https://img.shields.io/badge/python-v3-3776AB?logo=python)
  ![Vue](https://img.shields.io/badge/Vue-v3-4FC08D?logo=vue.js)
</p>

# Notifyme

Notifyme es un servicio de gestión de notificaciones para colas RabbitMQ.

El servicio se puede configurar para enviar emails a los usuarios suscritos a exchanges y keys cada vez que llega un mensaje al bus. 

Además, se pueden crear plantillas para los mensajes de tal forma que se pueden incluir variables que vengan incluídas dentro del mensaje enviado al bus.

Además de una API, el servicio ofrece un panel de control para gestionar de forma más sencilla las notificaciones.

Notifyme está pensado para no modificar el bus al que se conecta. El servicio crea su propia cola para no eliminar mensajes del bus al ser leídos.

La base de datos es RethinkDB, el backend está desarrollado con Python y el frontend con Vue.

## Getting Started

Las instrucciones que vas a leer a continuación sirven para ejecutar notify.me en tu máquina para poder desarrollar en local o en una máquina de producción.

### Prerrequisitos

Para poder ejecutar notify.me necesitas una base de datos RethinkDB. Además necesitas tener funcionando un bus RabbitMQ del que poder recibir las notificaciones. 

Para instalar rethinkDB:
[Instalación de la base de datos rethinkDB](https://rethinkdb.com/docs/install/)

Para instalar rabbitMQ:
[Instalación del bus rabbitMQ](https://www.rabbitmq.com/download.html)

Otra opción recomensable es ejecutar rethinkDB y rabbitMQ desde sus contenedores oficiales en docker:

```bash
docker run --name some-rethink -v "$PWD:/data" -d rethinkdb
docker run --name rabbitmq bitnami/rabbitmq:latest
```

Por último, tienes que tener instalado **python3**.

### Instalación y configuración

### Arrancar el servicio y la API

Para ejecutar notifyme descarga este repositorio en tu máquina. Una vez descargado ejecuta en una terminal de comandos:

```bash
pip install -r requirements.txt
```

La configuración de notifyme se hace desde su fichero de **config.json** o mediante variables de entorno. 

La configuración está preparada para que puedas incluir directamente el valor que de cada variable o para que puedas incluir una ruta a un fichero externo **config.ini** indicando el nombre y su sección, por ejemplo: /configs/seccion/nombre_variable.

El nombre de las variables de entorno están definidas dentro del fichero **settings.py**

Variables que puedes definir:

- **Bus**:
    - host: La dirección ip del bus de rabbitMQ
    - user: El usuario que has definido para rabbitMQ (el que crea por defecto rabbitMQ es *guest*)
    - password: La contraseña que has definido para el user de rabbitMQ (el que se crea por defecto es *guest*)
    - queue_name: El nombre de la cola que va a crear notifyme en el bus para conectarse a los exchanges
    - error_exchange: El nombre de la cola de error para enviar mensajes de error

- **SMTP**:
    - server: La dirección del SMTP para enviar los emails
    - port: El puerto desl servidor SMTP
    - email: Email del STMP desde el que sen envían los correos
    - password: Contraseña del email para enviar los correos
    - send_emails: Boolean, para bloquear el envío de emails
    - name: Nombre para mostrar en el remitente 
    - ttls: Boolea, para activar la conexión mediante ttls al servidor stmp 

- **loggin**:
    - Dirección en la maquina para escribir los mensajes de log (tiene que existir una carpeta con el nombre notifyme y dentro un archivo notifyme.log)

- **db**:
    - server: La dirección de la base de datos rethinkdb que has creado en la máquina
    - port: Puerto de la base de datos que has creado
    - refresh_database: Por si quieres reiniciar la base de datos cada vez que se inicia el servicio
    - user: User de la base de datos
    - password: Contraseña de la base de datos

- **api**:
    - server: Dirección en la que se va a poner a escuchar la API
    - port: Puerto en el que se va a poner a escuchar la API

- **default_template**
    - text: Texto de la notificatión cuando se usa el template por defecto
    - subject: Asunto del template por defecto

Una configuración típica sería:

```json
{
  "bus": {
    "host": "localhost",
    "user": "guest",
    "password": "guest",
    "queue_name": "notifyme",
    "error_exchange": "notifymeError"
  },
  "smtp": {
    "server": "smtp.gmail.com",
    "port": "465",
    "email": "<TU EMAIL DE GMAIL>",
    "password": "<CONTRASEÑA DEL EMAIL>",
    "name": "Nombre del remitente",
    "send_emails": true,
    "ttls": true
  },
  "logging": {
    "root_path": "<RUTA AL FICHERO DE LOGGIN>"
  },
  "db": {
    "server":"localhost",
    "port": "28015",
    "refresh_database": false,
    "user": "admin",
    "password": ""
  },
  "api": {
    "server": "0.0.0.0",
    "port": 8003
  },
  "default_template": {
    "text": "Ha llegado un mensaje desde el bus",
    "subject": "Nueva notificación"
  }
}
```

Para arrancar el servicio ejecutar:

```bash
python3 notifyme.py
```

El servicio al arrancar crea las tablas de la base de datos en caso que no existan y configura una API en la dirección especificada en el fichero de configuración.

Para más información sobre las llamadas de la API que se crean echa un vistazo a la [documentación](https://etsfactory.github.io/notify.me)

### Arrancar el panel de control

Para arrancar el panel de control tienes que tener instalado **node** y **npm** en la máquina.

A continuación hay que dirigirse mediante terminal a la carpeta **frontend** para ejecutar:

```
npm install
npm run serve
```

En caso de que se quiera compilar para usar en producción:

```
npm install
npm run build
```

El proyecto compilado se genera en la carpeta **dist** dentro de **frontend**.

Para más detalles ver el [**README.md** de la carpeta **frontend**](/frontend/README.md)

## Contribuciones

Por favor lee: [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles y para saber cómo enviar peticiones de cambios.

## Autores

* **Diego López García** - [Github](https://github.com/Frostqui)

## Licencia

Este proyecto tiene una licencia GNU, echa un vistazo a [LICENSE](LICENSE) para más detalles.
