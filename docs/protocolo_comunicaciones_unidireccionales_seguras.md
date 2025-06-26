# Protocolo de Comunicaciones Unidireccionales Seguras

A continuación se enumeran y describen los pasos que se sucederían en la transmisión de un mensaje de autenticación, suponiendo la correcta superación de todos los niveles de autenticación. Los encabezados indican el elemento actuando en cada momento. Además, en la siguiente figura se detalla un esquema simplificado del recorrido del mensaje a lo largo de los elementos que componen la red integrada segura.

![Flujo de mensajes de autenticación suponiendo autenticación exitosa](todocorrecto.png)

1. **Dispositivo Suscriptor**:
    1. Genera `DerivationNonce` y `SessionNonce`.
    2. Utiliza su `PSK`, su `DeviceID` y su `DerivationNonce` para generar la clave derivada.
    3. Genera el mensaje de autenticación cifrando los campos necesarios con la clave derivada. (ver sección de mensajes de autenticación)
    4. Envía el mensaje de autenticación a su *gateway* para ser reenviado al servidor de red. En este proyecto, como ejemplo, TTN.

2. **Servidor de red LoRaWAN**:
    1. Publica como *bróker* el mensaje recibido para que el UPF, suscriptor al *bróker*, obtenga el mensaje (equivalente a reenviarlo directamente al UPF, pero aprovechando la capacidad de *bróker* de TTN).

3. **UPF**:
    1. Identifica el tipo de payload a partir del campo `PayloadType`. Según el tipo, realiza decodificaciones previas o tratamientos especiales según se haya definido para ese tipo. En este caso, al ser un mensaje de autenticación, no realiza nada.
    2. Reenvía el mensaje al SMF.

4. **SMF**:
    1. Identifica a partir del campo `PayloadType` si es un mensaje de autenticación o de datos, en este caso, autenticación.
    2. Reenvía el mensaje al AMF para comenzar el primer nivel de autenticación.

5. **AMF**:
    1. Extrae el campo `DeviceID` del mensaje de autenticación.
    2. Envía el `DeviceID` al UDM, preguntándole si existe algún suscriptor registrado en la base de datos de suscriptores con dicho `DeviceID`.

6. **UDM**:
    1. Reenvía el `DeviceID` al UDR y espera la respuesta de este.

7. **UDR**:
    1. Comprueba si el `DeviceID` se encuentra en alguna fila de la base de datos de suscriptores. En este caso, sí.
    2. Contesta afirmativamente al UDM con la cadena “FL_Success”.

8. **UDM**:
    1. Contesta afirmativamente al AMF con la cadena “FL_Success”.

9. **AMF**:
    1. Da por superado el primer nivel de autenticación (autenticado a nivel de *visited network*).
    2. Reenvía el mensaje de autenticación al AUSF para comenzar el segundo nivel de autenticación.

10. **AUSF**:
    1. Extrae el `DeviceID` y el `DerivationNonce` del mensaje de autenticación.
    2. Envía el `DeviceID` y el `DerivationNonce` al UDM con el objetivo de que el UDR le genere la clave derivada.

11. **UDM**:
    1. Reenvía el `DeviceID` y el `DerivationNonce` al UDR.

12. **UDR**:
    1. Obtiene de la base de datos de suscriptores la `PSK` y la `SessionDuration` correspondientes al `DeviceID`.
    2. Genera la clave derivada a partir del `DeviceID`, `DerivationNonce` y la `PSK`.
    3. Contesta al UDM con la clave derivada y la `SessionDuration`.

13. **UDM**:
    1. Contesta al AUSF con la clave derivada y la `SessionDuration`.

14. **AUSF**:
    1. Utiliza la clave derivada y el `DerivationNonce` para descifrar el campo `HICC` del mensaje de autenticación.
    2. Genera el hash md5 del mensaje de autenticación sin el `HICC` y comprueba que los 3 primeros bytes coincidan con el `HICC`. En este caso, sí. Segundo nivel de autenticación superado. Integridad e identificación del mensaje confirmada a nivel de *home network*.
    3. Descifra `SessionNonce`.
    4. Envía `DeviceID`, clave derivada, `DerivationNonce`, `SessionNonce` y `SessionDuration` al SMF.

15. **SMF**:
    1. Crea una nueva fila en la base de datos de sesiones insertando los datos recibidos del AUSF en los campos correspondientes (ver sección de bases de datos).
    2. La sesión ha sido abierta para el suscriptor.

---

## Flujo de Mensajes - Mensaje de Autenticación Suponiendo Fallo en el Primer Nivel de Autenticación

Se presupone ahora que existe un fallo en el primer nivel de autenticación, es decir, en la identificación inicial del dispositivo por parte del AMF.

El flujo de mensajes será idéntico al flujo completo hasta el paso 6. En el paso 7, el UDR fallará al buscar el `DeviceID` y contestará al UDM y, a su vez, este al AMF con la cadena `FL_FAILURE`. El AMF descarta el mensaje de autenticación al no haberse superado el primer nivel de autenticación. Se marcan en azul los pasos que difieren.

![Flujo de mensajes de autenticación suponiendo fallo en el primer nivel de autenticación](falloFL.png)

1. **Dispositivo Suscriptor**:
    1. Genera `DerivationNonce` y `SessionNonce`.
    2. Utiliza su `PSK`, su `DeviceID` y su `DerivationNonce` para generar la clave derivada.
    3. Genera el mensaje de autenticación cifrando los campos necesarios con la clave derivada. (ver sección de mensajes de autenticación)
    4. Envía el mensaje de autenticación a su *gateway* para ser reenviado al servidor de red. En este proyecto, como ejemplo, TTN.

2. **Servidor de red LoRaWAN**:
    1. Publica como *bróker* el mensaje recibido para que el UPF, suscriptor al *bróker*, obtenga el mensaje (equivalente a reenviarlo directamente al UPF, pero aprovechando la capacidad de *bróker* de TTN).

3. **UPF**:
    1. Identifica el tipo de payload a partir del campo `PayloadType`. Según el tipo, realiza decodificaciones previas o tratamientos especiales según se haya definido para ese tipo. En este caso, al ser un mensaje de autenticación, no realiza nada.
    2. Reenvía el mensaje al SMF.

4. **SMF**:
    1. Identifica a partir del campo `PayloadType`, si es un mensaje de autenticación o de datos, en este caso, autenticación.
    2. Reenvía el mensaje al AMF para comenzar el primer nivel de autenticación.

5. **AMF**:
    1. Extrae el campo `DeviceID` del mensaje de autenticación.
    2. Envía el `DeviceID` al UDM, preguntándole si existe algún suscriptor registrado en la base de datos de suscriptores con dicho `DeviceID`.

6. **UDM**:
    1. Reenvía el `DeviceID` al UDR y espera la respuesta de este.

7. **<span style="color:blue">UDR</span>**:
    1. Comprueba si el `DeviceID` se encuentra en alguna fila de la base de datos de suscriptores. En este caso, no.
    2. Contesta negativamente al UDM con la cadena `FL_Failure`.

8. **<span style="color:blue">UDM</span>**:
    1. Contesta negativamente al AMF con la cadena `FL_Failure`.

9. **<span style="color:blue">AMF</span>**:
    1. El AMF confirma que ha fallado el primer nivel de autenticación.
    2. Se descarta el mensaje de autenticación.

---

## Flujo de Mensajes - Mensaje de Autenticación Suponiendo Fallo en el Segundo Nivel de Autenticación

Se presupone ahora un fallo en el segundo nivel de autenticación, es decir, el AUSF fallaría al igualar el `HICC` descifrado con el generado a partir de los campos correspondientes del mensaje recibido.

El flujo de mensajes será idéntico al flujo completo hasta el paso 13. En el paso 14, el AUSF fallará al comprobar que el `HICC` descifrado se corresponde con el generado a partir del hash obtenido del mensaje con campos descifrados a partir de la clave generada. Fallo en el segundo nivel de autenticación, se descarta el mensaje de autenticación. Se marcan en azul los pasos que difieren.

![Flujo de mensajes de autenticación suponiendo fallo en el segundo nivel de autenticación](falloSL.png)

1. **Dispositivo Suscriptor**:
    1. Genera `DerivationNonce` y `SessionNonce`.
    2. Utiliza su `PSK`, su `DeviceID` y su `DerivationNonce` para generar la clave derivada.
    3. Genera el mensaje de autenticación cifrando los campos necesarios con la clave derivada. (ver sección de mensajes de autenticación)
    4. Envía el mensaje de autenticación a su *gateway* para ser reenviado al servidor de red. En este proyecto, como ejemplo, TTN.

2. **Servidor de red LoRaWAN**:
    1. Publica como *bróker* el mensaje recibido para que el UPF, suscriptor al *bróker*, obtenga el mensaje (equivalente a reenviarlo directamente al UPF, pero aprovechando la capacidad de *bróker* de TTN).

3. **UPF**:
    1. Identifica el tipo de payload a partir del campo `PayloadType`. Según el tipo, realiza decodificaciones previas o tratamientos especiales según se haya definido para ese tipo. En este caso, al ser un mensaje de autenticación, no realiza nada.
    2. Reenvía el mensaje al SMF.

4. **SMF**:
    1. Identifica a partir del campo `PayloadType`, si es un mensaje de autenticación o de datos, en este caso, autenticación.
    2. Reenvía el mensaje al AMF para comenzar el primer nivel de autenticación.

5. **AMF**:
    1. Extrae el campo `DeviceID` del mensaje de autenticación.
    2. Envía el `DeviceID` al UDM, preguntándole si existe algún suscriptor registrado en la base de datos de suscriptores con dicho `DeviceID`.

6. **UDM**:
    1. Reenvía el `DeviceID` al UDR y espera la respuesta de este.

7. **UDR**:
    1. Comprueba si el `DeviceID` se encuentra en alguna fila de la base de datos de suscriptores. En este caso, sí.
    2. Contesta afirmativamente al UDM con la cadena `FL_Success`.

8. **UDM**:
    1. Contesta afirmativamente al AMF con la cadena `FL_Success`.

9. **AMF**:
    1. El AMF da por superado el primer nivel de autenticación (Autenticado a nivel de *visited network*).
    2. Reenvía el mensaje de autenticación al AUSF para comenzar el segundo nivel de autenticación.

10. **AUSF**:
    1. Extrae el `DeviceID` y el `DerivationNonce` del mensaje de autenticación.
    2. Envía el `DeviceID` y el `DerivationNonce` al UDM con el objetivo de que el UDR le genere la clave derivada.

11. **UDM**:
    1. Reenvía el `DeviceID` y el `DerivationNonce` al UDR.

12. **UDR**:
    1. Obtiene de la base de datos de suscriptores la `PSK` y la `SessionDuration` correspondientes al `DeviceID`.
    2. Genera la clave derivada a partir del `DeviceID`, `DerivationNonce` y la `PSK`.
    3. Contesta al UDM con la clave derivada y la `SessionDuration`.

13. **UDM**:
    1. Contesta al AUSF con la clave derivada y la `SessionDuration`.

14. **<span style="color:blue">AUSF</span>**:
    1. Utiliza la clave derivada y el `DerivationNonce` para descifrar el campo `HICC` del mensaje de autenticación.
    2. Genera el hash md5 del mensaje de autenticación sin el `HICC` y comprueba que los 3 primeros bytes coincidan con el `HICC`. En este caso, no. Segundo nivel de autenticación no superado.
    3. Se descarta el mensaje de autenticación.
