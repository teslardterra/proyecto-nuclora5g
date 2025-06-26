# Despliegue y Configuración
Se distinguen dos casos para el despliegue, que se abordan en las siguientes secciones. En ambos, se supone un despliegue local con todos los componentes y elementos en el mismo sistema anfitrión.

## Despliegue Contenerizado

Para este tipo de despliegue, se supone la existencia de un núcleo 5G Standalone virtualizado mediante contenedores docker (siguiendo estándares 3GPP), desplegado en el equipo anfitrión, con al menos los siguientes componentes: NRF, AMF, AUSF, SMF, UPF, UDM y UDR. Además, se supone un sistema Linux.

No entra en el ámbito de este proyecto, el cómo desplegar dicho núcleo 5G standalone, si bien, se recomiendan opciones abiertas como los repositorios de OAI, utilizada para las pruebas y test de esta integración, o Free5GC. Ambas opciones cuentan con guías propias completas en sus respectivos repositorios y webs (OAI: https://gitlab.eurecom.fr/oai/cn5g/oai-cn5g-fed, Free5GC: https://free5gc.org/)

Se supone, si cumple lo anterior, que los contenedores se encuentran en la misma red docker. En caso contrario, o si se desea utilizar una red distinta, puede crearse una red de contenedores y agregar contenedores a ella con los siguientes comandos (si alguno falla por problemas de permisos, agregar sudo al comienzo de cada uno):

Nota: Los valores entre < > indican variables que el lector/usuario deberá sustituir con los datos necesarios.
### Crear red (bridge para que puedan verse entre ellos)
```bash
docker network create --driver bridge <nombre_red>

### Agregar contenedores a la red

docker network connect <nombre_red> <id_o_nombre_del_contenedor>
```

Deberán añadirse todos los contenedores a la red, es decir, repetir el comando connect para todos los contenedores.

Para conocer el nombre o ID de los contenedores desplegados, puede utilizarse el comando:

```bash
### Listar contenedores
docker ps -a
```
Una vez identificados los contenedores desplegados (cada núcleo 5G cuenta con sus pasos específicos de despliegue, consultar la guía correspondiente del núcleo utilizado) en su red asignada, puede configurarse la integración.

En este caso, descargar del repositorio el directorio despliegue-contenerizado.

El contenido del directorio sigue la estructura mostrada en la siguiente imagen, contando con una carpeta para cada componente del núcleo 5G, con los archivos correspondientes a agregar a dichos componentes.



Una vez descargado, dirigirse al archivo despliegue-contenerizado/NRF/utils_NRF.py y abrirlo con un editor de texto o código. Modificar las líneas 33 a 38 (función return_addresses), cambiando los nombres de los contenedores de ejemplo oai-upf, oai-smf, etc. con los correspondientes a los contenedores desplegados por el lector/usuario. Ejemplo: oai-smf pasa a mi_upf (ver nombres de sus contenedores ejecutando el comando docker ps -a en la terminal). El NRF utiliza esta información para descubrir las direcciones en la red (variables por redundancia) de los distintos componentes del núcleo. En la siguiente imagen se muestra el lugar en el que deben realizarse estos cambios.



Ahora, dirigirse al archivo despliegue-contenerizado/AMF/utils_AMF.py y sustituir en la línea 4:
ADDR_NRF = (socket.gethostbyname("oai-nrf"), 5050)
por el nombre o id del contenedor NRF del lector/usuario. En la siguiente imagen se muestra este cambio. Deberá repetirse este paso para los archivos utils_X.py de los siguientes componentes: AUSF, SMF, UPF, UDM y UDR, encontrados en las direcciones despliegue-contenerizado/X/utils_X.py, siendo X el componente.


Editar ahora el archivo despliegue-contenerizado/UPF/mqtt_ttn_reciver_UPF.py, modificando las líneas 10 a 15 con los datos del tópico del bróker al que estén suscritos los dispositivos IoT de los que se busque recibir las transmisiones LoRaWAN en el sistema integrado. En el caso de esta integración y por motivos explicados con anterioridad, se ha utilizado TTN. El cómo vincular dispositivos a TTN, crear tópicos y obtener los datos de usuario y contraseña, no entran dentro del ámbito de este proyecto. (Puede consultarse una guía creada por TTN en https://www.thethingsindustries.com/docs/integrations/other-integrations/mqtt/). En la siguiente imagen se muestra un ejemplo de estos cambios.



Tras realizar los cambios, deberán copiarse las subcarpetas despliegue-contenerizado/X al interior de los contenedores correspondientes. Para ello, pueden ejecutarse los siguientes comandos:

```bash
docker cp <ruta>/despliegue-contenerizado/AMF <Id_o_nombre_contenedor_AMF>:/ 
docker cp <ruta>/despliegue-contenerizado/AUSF <Id_o_nombre_contenedor_AUSF>:/ 
docker cp <ruta>/despliegue-contenerizado/SMF <Id_o_nombre_contenedor_SMF>:/ 
docker cp <ruta>/despliegue-contenerizado/UPF <Id_o_nombre_contenedor_UPF>:/ 
docker cp <ruta>/despliegue-contenerizado/UDM <Id_o_nombre_contenedor_UDM>:/ 
docker cp <ruta>/despliegue-contenerizado/UDR <Id_o_nombre_contenedor_UDR>:/ 
docker cp <ruta>/despliegue-contenerizado/NRF <Id_o_nombre_contenedor_NRF>:/ 

### Copiar al AMF
docker cp <ruta>/despliegue-contenerizado/AMF <Id_o_nombre_contenedor_AMF>:/ 

### Copiar al AUSF
docker cp <ruta>/despliegue-contenerizado/AUSF <Id_o_nombre_contenedor_AUSF>:/ 

###  Copiar al SMF
docker cp <ruta>/despliegue-contenerizado/SMF <Id_o_nombre_contenedor_SMF>:/ 

###  Copiar al UPF
docker cp <ruta>/despliegue-contenerizado/UPF <Id_o_nombre_contenedor_UPF>:/ 

###  Copiar al UDM
docker cp <ruta>/despliegue-contenerizado/UDM <Id_o_nombre_contenedor_UDM>:/ 

###  Copiar al UDR
docker cp <ruta>/despliegue-contenerizado/UDR <Id_o_nombre_contenedor_UDR>:/ 

###  Copiar al NRF
docker cp <ruta>/despliegue-contenerizado/NRF <Id_o_nombre_contenedor_NRF>:/

```
Una vez copiadas las carpetas, se deberá abrir una ventana o pestaña de terminal nueva por cada componente, salvo el UPF que requiere dos, 8 en total (no es completamente necesario, pero ayuda a visualizar los registros y avisos durante el funcionamiento).

En la correspondiente ventana escogida para cada componente, ejecutar los siguientes comandos en orden para arrancar el despliegue contenerizado:

Nota: Cerrar alguna de las ventanas implica la parada de la ejecución de la integración en ese componente, por tanto, no cerrar durante el tiempo que se desee mantener el entorno integrado en funcionamiento.

Si es la primera vez que se realiza el arranque o despliegue en el sistema:

```bash
###  Ventana para NRF
docker exec -it <Id_o_nombre_contenedor_NRF> /bin/bash
cd NRF
apt-get update
apt-get upgrade
apt-get install -y python3
python3 server_NRF.py

###  Ventana para AMF
docker exec -it <Id_o_nombre_contenedor_AMF> /bin/bash
cd AMF
apt-get update
apt-get upgrade
apt-get install -y python3
python3 server_AMF.py

###  Ventana para AUSF
docker exec -it <Id_o_nombre_contenedor_AUSF> /bin/bash
cd AUSF
apt-get update
apt-get upgrade
apt-get install -y python3
python3 server_AUSF.py

###  Ventana para SMF
docker exec -it <Id_o_nombre_contenedor_SMF> /bin/bash
cd SMF
apt-get update
apt-get upgrade
apt-get install -y python3
apt-get install -y pip
apt-get install python3-cryptography
python3 create_SessionsLoRa_db.py
python3 server_SMF.py

###  Ventana para UDM
docker exec -it <Id_o_nombre_contenedor_UDM> /bin/bash
cd UDM
apt-get update
apt-get upgrade
apt-get install -y python3
python3 server_UDM.py

###  Ventana para UDR
docker exec -it <Id_o_nombre_contenedor_UDR> /bin/bash
cd UDR
apt-get update
apt-get upgrade
apt-get install -y python3
apt-get install -y pip
apt-get install python3-cryptography
pip install pycryptodome --break-system-packages
python3 create_SubscribersLoRa_db.py
python3 create_TransmissionsLoRa_db.py
python3 server_UDR.py

###  Ventana para UPF 1
docker exec -it <Id_o_nombre_contenedor_UPF> /bin/bash
cd UPF
apt-get update
apt-get upgrade
apt-get install -y python3
python3 server_UPF.py

###  Ventana para UPF 2
docker exec -it <Id_o_nombre_contenedor_UPF> /bin/bash
cd UPF
apt-get install -y python3-paho-mqtt
python3 mqtt_ttn_reciver_UPF.py

```
Si se ha realizado el arranque o despliegue con anterioridad en el sistema:


```bash
###  Ventana para NRF
docker exec -it <Id_o_nombre_contenedor_NRF> /bin/bash
cd NRF
python3 server_NRF.py

###  Ventana para AMF
docker exec -it <Id_o_nombre_contenedor_AMF> /bin/bash
cd AMF
python3 server_AMF.py

###  Ventana para AUSF
docker exec -it <Id_o_nombre_contenedor_AUSF> /bin/bash
cd AUSF
python3 server_AUSF.py

###  Ventana para SMF
docker exec -it <Id_o_nombre_contenedor_SMF> /bin/bash
cd SMF
python3 server_SMF.py

###  Ventana para UDM
docker exec -it <Id_o_nombre_contenedor_UDM> /bin/bash
cd UDM
python3 server_UDM.py

###  Ventana para UDR
docker exec -it <Id_o_nombre_contenedor_UDR> /bin/bash
cd UDR
python3 server_UDR.py

###  Ventana para UPF 1
docker exec -it <Id_o_nombre_contenedor_UPF> /bin/bash
cd UPF
python3 server_UPF.py

###  Ventana para UPF 2
docker exec -it <Id_o_nombre_contenedor_UPF> /bin/bash
cd UPF
python3 mqtt_ttn_reciver_UPF.py

```
Tras esto, el despliegue está completo, pudiendo el entorno integrado recibir las transmisiones LoRaWAN sobre el núcleo 5G a través del bróker de TTN u otra red LoRaWAN, como si el núcleo 5G fuese el servidor de aplicación de la red LoRaWAN.

Se recuerda que para la aceptación de transmisiones, el dispositivo IoT debe estar suscrito en la base de datos de suscriptores, realizado esto fuera de banda.


## Despliegue No Contenerizado

Este tipo de despliegue, más sencillo que el anterior, supone que el sistema anfitrión posee un núcleo 5G SA no contenerizado, ejecutándose todos sus componentes en el anfitrión de forma directa, o que se desea hacer un despliegue como gestor independiente de transmisiones LoRaWAN, es decir, sin un núcleo 5G (manteniendo las aportaciones del nuevo protocolo en cuanto a seguridad y gestión, pero no las de independencia y hardware de un núcleo 5G SA 3GPP).

Descargar el directorio `despliegue-no-contenerizado`, el cual contiene una subcarpeta nombrada como cada componente de un núcleo 5G SA. Para este despliegue no contenerizado, no importa dónde se sitúen los directorios en el sistema, quedando a disposición del lector/usuario.

Deben instalarse varias dependencias generales para el funcionamiento. Puede realizarse con los siguientes comandos:

```bash
apt-get update
apt-get upgrade
apt-get install -y python3
apt-get install -y pip
apt-get install python3-cryptography
pip install pycryptodome --break-system-packages # Nota: Si no desea sobreescribir el entorno existente de Python puede crear un entorno nuevo (o sustituir este comando por sudo apt-get install python3-pycryptodome, pero no siempre funciona).
apt-get install -y python3-paho-mqtt
Modificar el archivo despliegue-no-contenerizado/UPF/mqtt_ttn_reciver_UPF.py, modificando las líneas 10 a 15 con los datos del tópico del bróker al que estén suscriptos los dispositivos IoT de los que se busque recibir las transmisiones LoRaWAN en el sistema. El cómo vincular dispositivos a TTN, crear tópicos y obtener los datos de usuario y contraseña, no entran dentro del ámbito de este proyecto. (Puede consultarse una guía creada por TTN en https://www.thethingsindustries.com/docs/integrations/other-integrations/mqtt/).

A continuación un ejemplo de los cambios a realizar en dicho archivo:



Ahora, abrir una ventana o pestaña de terminal nueva por cada componente, salvo el UPF que requiere dos, 8 en total (no es completamente necesario, pero ayuda a visualizar los registros y avisos durante el funcionamiento).

Finalmente, en este tipo de despliegue no contenerizado, basta con ejecutar los siguientes comandos, en su correspondiente ventana o pestaña, para el arranque del sistema:

Nota: Cerrar alguna de las ventanas implica la parada de la ejecución de la integración en ese componente, por tanto, no cerrar durante el tiempo que se desee mantener el entorno integrado en funcionamiento.

bash
Copiar
Editar
# Ventana para NRF
cd <ruta donde se encuentre la carpeta despliegue-no-contenerizado>/NRF
python3 server_NRF.py

# Ventana para AMF
cd <ruta donde se encuentre la carpeta despliegue-no-contenerizado>/AMF
python3 server_AMF.py

# Ventana para AUSF
cd <ruta donde se encuentre la carpeta despliegue-no-contenerizado>/AUSF
python3 server_AUSF.py

# Ventana para SMF
cd <ruta donde se encuentre la carpeta despliegue-no-contenerizado>/SMF
python3 create_SessionsLoRa_db.py
python3 server_SMF.py

# Ventana para UDM
cd <ruta donde se encuentre la carpeta despliegue-no-contenerizado>/UDM
python3 server_UDM.py

# Ventana para UDR
cd <ruta donde se encuentre la carpeta despliegue-no-contenerizado>/UDR
python3 server_UDR.py

# Ventana para UPF 1
cd <ruta donde se encuentre la carpeta despliegue-no-contenerizado>/UPF
python3 server_UPF.py

# Ventana para UPF 2
cd <ruta donde se encuentre la carpeta despliegue-no-contenerizado>/UPF
python3 mqtt_ttn_reciver_UPF.py

