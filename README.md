# Proyecto Nuclora5G
## Universidad de Oviedo - Cátedra Thin5G

### Trabajo original desarrollado por Dan García Carrillo, Diego Arias Sal e Ignacio Rodriguez Larrad, como parte de un proyecto académico realizado en la Escuela Politécnica de Ingeniería de Gijón, Universidad de Oviedo, con la colaboración de la Cátedra Thin5G.

<p align="center">
  <img src="nuclora5G_logo.png" alt="Mi Logo" width="300">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/LoRaWAN-IoT-green?style=for-the-badge&logo=wifi">
  <img src="https://img.shields.io/badge/5G-IOT Integration-steelblue?style=for-the-badge&logo=globe">
  <img src="https://img.shields.io/badge/Versión-1.0.0-brightgreen?style=for-the-badge">
</p>

# 📡 Sistema 5G-LoRaWAN Integrado y Seguro

Este proyecto busca desarrollar un sistema **5G-LoRaWAN integrado y seguro**, capaz de gestionar de forma conjunta las transmisiones unidireccionales provenientes de dispositivos IoT dentro de una red LoRaWAN, utilizando funcionalidades inspiradas en redes 5G, garantizando la seguridad de las transmisiones y funcionando sobre los componentes de un núcleo 5G standalone, buscando aprovechar su infraestructura y arquitectura.

El proyecto quiere ofrecer una primera solución que, en el futuro, facilite la gestión conjunta y segura de redes LoRaWAN y 5G en entornos que requieren el uso simultáneo de ambas tecnologías, como la industria, ciudades inteligentes, entre otros, sentando así una base sólida para el desarrollo de futuras iteraciones y mejoras del mismo.

## 🎯 Objetivos

### Objetivo Principal

Obtener un sistema o entorno **5G-LoRaWAN integrado y seguro** capaz de gestionar las transmisiones unidireccionales provenientes de dispositivos IoT, que formen parte de una red LoRaWAN, tanto a nivel de datos como de autenticación, mediante el uso de los componentes y la arquitectura de red de un núcleo 5G standalone.

### Objetivos Secundarios

1. Crear un protocolo de comunicaciones para transmisiones unidireccionales que garantice la integridad, autenticación y confidencialidad de las mismas, aplicable a transmisiones provenientes de dispositivos IoT en redes LoRaWAN.

2. Imitar, en lo posible, las funciones de los componentes de un núcleo 5G Standalone durante la gestión de las transmisiones provenientes de dispositivos IoT u otras transmisiones unidireccionales.

## 🔐 Protocolo de Comunicaciones Unidireccionales Seguras

Con el fin de lograr estos objetivos, se ha diseñado un **nuevo protocolo de comunicaciones unidireccionales seguras**, el cual:
- Se adapta a cualquier tipo de red o transmisión undireccional, siendo necesario solo que los mensajes enviados por los dispositivos sigan los formatos correctos indicados por el protocolo.
- Permite cumplir con las limitaciones propias de redes como LoRaWAN, al requerir de bytes fijos mínimos en el formato requerido por la estructura sus mensajes.
- Sirve como guía para la implementación lógica del sistema 5G-LoRaWAN integrado.
- Aporta seguridad, confidencialidad e integridad a las transmisiones unidireccionales, imitando los protocolos y mecanismos de seguridad de las redes 5G.

## ⚙️ Modos de Despliegue

El proyecto puede utilizarse en tres formas principales:

1. **Sistema 5G-LoRaWAN integrado seguro*  
   Integración con el núcleo de una red 5G, aprovechando su arquitectura para ofrecer una solución IoT segura, robusta y escalable, de manera contenerizada o no.

2. **Gestor seguro independiente de transmisiones LoRaWAN unidireccionales **  
   Utiliza el protocolo de comunicaciones unidireccionales seguras para la gestión segura de transmisiones LoRaWAN unidireccionales, adaptando los mensajes enviados por los dispositivos IoT
   al formato del protocolo.

3. **Gestor seguro de transmisiones unidireccionales*  
   El protocolo, por su naturaleza independiente, puede ser utilizado para gestionar cualquier tipo de transmisión undireccional en cualquier tipo de red, sin las limitaciones propias de LoRaWAN, ya que, el protocolo solo requiere que los mensajes enviados por los dispositivos se adapten al formato del protocolo en su estructura básica, no existiendo límites reales para con el tamaño de los mensajes (fuera del sistema integrado o gestor LoRaWAN) y siendo facilmente adaptable a nuevas necesidades.
---

## Ficha Técnica del Proyecto

| Categoría           | Especificación                                                                                                                                                                                                                                                                                                                                                               |
|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Nombre del Proyecto** | Nuclora: Entorno 5G-LoRaWAN integrado seguro                                                                                                                                                                                                                                                                                                                            |
| **Versión**            | 1.0                                                                                                                                                                                                                                                                                                                                                                       |
| **Tipo de Software**   | Plataforma de integración IoT 5G-LoRaWAN mediante protocolo propio                                                                                                                                                                                                                                                                                                         |
| **Plataformas Soportadas** | Linux, Windows                                                                                                                                                                                                                                                                                                                                                             |
| **Tecnologías Utilizadas** | Python, SQLite, Docker, MQTT, LoRaWAN, TTN, 5G *standalone*, IoT                                                                                                                                                                                                                                                                                                         |
| **Licencia**            | GPL-3.0 license                                                                                                                                                                                                                                                                                                                                                            |
| **Función Principal**   | Gestión segura de transmisiones unidireccionales LoRaWAN, mediante un nuevo protocolo que imita los planos de control y datos de 5G para adaptar la autenticación, gestión de sesión y transmisión segura a las restricciones de LoRaWAN y las transmisiones unidireccionales, funcionando sobre los componentes de un núcleo 5G *standalone*.                                 |
| **Requisitos mínimos**  | Procesador: 1 núcleo virtual (mínimo 500 MHz); Memoria RAM: 2 GB; Espacio en disco: 500 MB disponibles; Sistema operativo: Linux Ubuntu 22.04 LTS (Jammy Jellyfish) o superior, o Windows 11; *Consumo típico observado: 0.17 GHz CPU, 1.03 GB RAM, 0.49 MB/s escritura en disco*                                                                                              |
| **Tipos de Despliegue** | Entorno integrado seguro contenerizado; Entorno integrado seguro no contenerizado; Gestor independiente de transmisiones LoRaWAN, no contenerizado                                                                                                                                                                                                                        |
| **Última Actualización** | 10 de junio de 2025                                                                                                                                                                                                                                                                                                                                                        |
| **Repositorio Oficial** | [https://github.com/teslardterra/proyecto-nuclora5g](https://github.com/teslardterra/proyecto-nuclora5g)                                                                                                                                                                                                                                                                  |


## 📖 Documentación

Puedes encontrar la documentación completa en el directorio [`docs/`](docs/). También puede valerse de los siguientes enlaces directos:

- 🧩 [Arquitectura de la integración](docs/arquitectura_red_integrada.md)
- 🛡️ [Mecanismos de ciberseguridad](docs/mecanismos_ciberseguridad.md)
- 🛰️ [Protocolo de Comunicaciones Unidireccionales Seguras](docs/protocolo_comunicaciones_unidireccionales_seguras.md)   
- ⚙️ [Despliegue y Configuración](docs/despliegue_configuracion.md)  
- 📜 [Licencia](LICENSE)  


Para más detalles sobre el proyecto, revisa los archivos en `docs/`.

---

📌 *Este proyecto está en desarrollo y sujeto a cambios.*
