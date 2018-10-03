## Notify.me

### Introducción

Notify.me es un servicio creado en python para el manejo de notificaciones en RabbitMQ. La aplicación permite configurar usuarios junto a los mensajes a los que se va a querer suscribir el usuario. En principio la notificación al usuario se hace mediante correo electrónico, aunque la funcionalidad se puede ampliar para permitir otros servicios. Además se puede configurar una plantilla para el mensaje, es decir, se puede decidir que aspecto va a tener el mensaje de la notificación. Para la configuración en principio se puede hacer mendiante línea de comandos o mendiante API.

### Instrucciones

Para poder ejecutar el servicio hay que tener instalado **python**

Además, hay que instalar los paquetes con la versión indicada en el fichero advisory/requirements.txt.
Para ello, abrir una ventana de comandos y ejecutar:

```bash
pip install -r requirements.txt
```

Para arrancar el servicio ejecutar el comando:

```bash
python main.py
```

Para ejecutar los tests instalar py.test y ejecutar:

```bash
py.test
```
