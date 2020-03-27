# Panel de control de notifyme

Este es un proyecto creado con **Vue** y **axios**. El proyecto se conecta a la API generada por el servicio de notifyme.

## Desarrollo en local

Para el desarrollo en local, en primer lugar se recomienda crear un fichero .env.development. Este fichero sirve
para establecer la URL de la API de notifyme, para ello:

```
VUE_APP_NOTIFYME_HOST="http:localhost:/8003"
```

Si no existe el fichero .env.development por defecto se usa el valor que se encuentre en el fichero **.env**. El valor de este fichero además se usa en producción si se lanza el comando del build de npm.

Además, se puede sobreescribir el valor de estos ficheros si existe el fichero de config.ini indicado en el fichero **readConfig.js**. En este fichero se lee el config.ini y se busca el valor de la variable así:

```javascript
setEnvParam("APIS", "notifyme_host", "VUE_APP_NOTIFYME_HOST");
```
El primer valor de la función es la sección del config.ini y el segundo valor la variable que se va a leer. El resultado se guarda dentro de la varible indicada como tercer argumento.

Una vez establecida la ruta a la API ya se puede ejecutar el proyecto en local:

```
npm install
npm run serve
```

Por defecto se levanta la web en la URL: [localhost:8080](localhost:8080)


## Puesta en producción

Para poner el panel de control en producción lo único que hay que hacer es ejecutar:

```
npm install
npm run build
```

Se generará la carpeta **dist** con los archivos ya compilados.
