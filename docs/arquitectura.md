# Arquitectura de Red Integrada 5G-LoRaWAN

Para la integración, se parte de la base de que se mantienen intactas tanto la estructura principal de la red 5G como de la red LoRaWAN. La idea consiste en sustituir el servidor de aplicaciones final de la red LoRaWAN (gestor final) por el UPF, por ser el único componente del núcleo 5G con acceso a redes exteriores.

El proceso de autenticación y sesión inicial mediante transmisiones bidireccionales entre el dispositivo LoRaWAN y su servidor de red LoRaWAN se mantiene idéntico al explicado en la sección anterior y se presupone seguro. Ahora bien, una vez autenticado en su servidor de red, los mensajes de datos unidireccionales de la red LoRaWAN que serán recibidos por el servidor de red y compartidos al servidor de aplicaciones, ahora el UPF, seguirán dos nuevos formatos. Estos mensajes de datos LoRaWAN pasan a dividirse en mensajes de autenticación de la red integrada y mensajes de datos de la red integrada. En las figuras siguientes se ilustran los procesos descritos.

![Flujo de mensajes de autenticación LoRaWAN](TFG_latex/Texto/Desarrollo/Figuras/authlorawan.png)

*Figura 1: Flujo de mensajes de autenticación LoRaWAN*

![Nuevos mensajes de la red integrada](TFG_latex/Texto/Desarrollo/Figuras/datoslorawan.png)

*Figura 2: Nuevos mensajes de la red integrada*

Una vez los nuevos mensajes de la integración sean compartidos por el servidor de red con el UPF, este extraerá la carga útil del mensaje, eliminando cabeceras propias añadidas por el servidor de red, que no serán necesarias, y lo reenviará al SMF, por ser este la única conexión permanente del UPF con otro componente del núcleo 5G (en plano de control y sin contar el NRF).

El SMF, encargado en 5G del manejo de sesiones, detectará si el mensaje recibido tiene formato de autenticación de la red integrada o de datos. En caso de mensaje de autenticación, lo reenviará al AMF para que comience un proceso de autenticación que imitará la estructura del de 5G, más robusto que el de LoRaWAN.

La naturaleza unidireccional de las comunicaciones en el sistema integrado, al contrario que la bidireccional de 5G, no permite realizar múltiples de los pasos que realiza una autenticación 5G completa, por lo que, la seguridad de la integración se centra en el concepto general de cada paso, imitándolo mediante procesos con objetivos similares que se adecúen a las limitaciones unidireccionales, en lugar de replicarlo. Si la autenticación se produce satisfactoriamente, se abrirá una sesión de datos para el usuario de la red integrada.

En caso de mensaje de datos, el SMF comprobará si existe una sesión abierta para el usuario en la red integrada, si es así, y el mensaje de datos es correcto, se reenviará al UDM y este a su vez al UDR para su almacenamiento y registro.

Para dotar de capacidad al núcleo 5G de realizar estos nuevos procesos con los datos recibidos desde la red LoRaWAN, se añadirán múltiples programas (*scripts*) independientes a cada uno de los componentes para realizar las funciones que le correspondan. Además, se dotará al sistema de tres nuevas bases de datos: sesiones, situada en el SMF, suscriptores, y transmisiones, ambas situadas en el UDR. Las nuevas funciones de cada componente y la estructura de las nuevas bases de datos se detallan en secciones posteriores.

Los usuarios (dispositivos IoT) provenientes de la red LoRaWAN deberán estar suscritos a la red integrada, registrándose mediante un proceso fuera de banda (*out of band*).

Los mensajes, ya sean de autenticación como de datos, viajarán cifrados y se garantizará en todo momento su confidencialidad y autenticación. En el caso de un mensaje de autenticación, también se garantiza su integridad y, en caso de mensajes de datos, el sistema integrado es capaz de detectar la pérdida de mensajes anteriores, aunque no de solicitar su retransmisión (por limitación unidireccional de la transmisión).

La arquitectura de la integración, los componentes originales de las redes 5G y LoRaWAN y aquellos añadidos o modificados, se representan en la siguiente figura.

![Arquitectura de Red Integrada 5G-LoRaWAN](TFG_latex/Texto/Desarrollo/Figuras/EsquemaBaseTotal.png)

*Figura 3: Arquitectura de Red Integrada 5G-LoRaWAN*

En las siguientes secciones, se profundizará en cada uno de los campos mencionados en esta sección. Comenzando por los tipos de mensajes de la red integrada, es decir, aquellos provenientes de la red LoRaWAN pero con nuevo formato, para seguir con los campos de las distintas nuevas bases de datos, procesos de cifrado, flujos de mensajes, etc.

