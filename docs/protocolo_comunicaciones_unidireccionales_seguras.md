
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
