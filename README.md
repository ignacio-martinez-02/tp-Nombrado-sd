# 🔗 Sistema Integral de Nombrado (SIN) – TP 6

## 📚 Datos académicos

**Materia:** Sistemas Distribuidos  
**Carrera:** Ingeniería en Sistemas de Información  
**Año:** 4°  
**Trabajo Práctico N° 6: Nombrado**  
**Autores:**  
- Fraisinet, Máximo Exequiel  
- Leal, Pablo Valentín  
- Martínez, Ignacio Gabriel  
- Moreyra, Omar Sebastián  
- Guiffrey, Leando Ezequiel  

---

## 🧩 Descripción del proyecto

Este trabajo práctico implementa un **Sistema Integral de Nombrado (SIN)** en Python, que permite registrar, buscar y resolver nombres de recursos distribuidos.  
El sistema proporciona **transparencia de nombres y ubicación** en un entorno distribuido, siendo utilizado por ejemplos de **RPC (Remote Procedure Call)** y **RMI (Remote Method Invocation)**.

El objetivo es mostrar cómo se puede desacoplar la lógica de comunicación de la localización física de los servicios, emulando mecanismos de nombrado similares a DNS o GNS pero en un entorno educativo y local.

---

## ⚙️ Componentes principales

El proyecto está compuesto por los siguientes módulos:

| Archivo | Descripción |
|----------|--------------|
| `sin_name_service.py` | Servidor principal del **Sistema Integral de Nombrado (SIN)**. Mantiene el registro de nombres, tipos y ubicaciones de los recursos. |
| `rpc_server.py` | Servidor RPC. Registra sus funciones en el SIN y atiende llamadas remotas. |
| `rpc_client.py` | Cliente RPC. Consulta el SIN para ubicar el servicio y realiza invocaciones remotas. |
| `rmi_server.py` | Servidor RMI. Expone objetos remotos y los registra en el SIN. |
| `rmi_client.py` | Cliente RMI. Obtiene objetos remotos desde el SIN e invoca métodos sobre ellos. |
| `utils_protocol.py` | Módulo auxiliar para el envío y recepción de mensajes en formato JSON a través de sockets TCP. |

---

## 🧠 Funcionamiento general

1. El **Name Service (SIN)** escucha conexiones en el puerto `40000`.  
   Los servidores (RPC o RMI) se conectan a él para **registrarse** con un nombre lógico, tipo y metadatos.

2. Los clientes consultan el SIN mediante un comando `LOOKUP` para obtener la dirección IP y puerto del servicio deseado.

3. Una vez resuelto el nombre, el cliente establece una conexión directa con el servidor correspondiente y realiza la invocación remota.

De este modo, se logra:
- **Transparencia de ubicación:** los clientes no necesitan conocer la dirección física del servidor.
- **Flexibilidad:** cualquier tipo de recurso (servicio, archivo, proceso, objeto, etc.) puede registrarse.
- **Extensibilidad:** se pueden agregar metadatos, TTL, búsqueda por prefijo o consultas filtradas (`QUERY`).

---

## 🚀 Instrucciones de ejecución

A continuación se detalla cómo ejecutar cada componente en terminales separadas.

### 1️⃣ Iniciar el servidor del SIN

```bash
python3 sin_name_service.py
```
Salida esperada:
```nginx
SIN NameService listening on 127.0.0.1:40000
```
### 2️⃣ Iniciar el servidor RPC

En una nueva terminal:

```bash
python3 rpc_server.py
```

Salida esperada:
```ruby
RPC server listening on 127.0.0.1:<puerto>
```

### 3️⃣ Ejecutar el cliente RPC

En otra terminal:
```bash
python3 rpc_client.py
```

Salida esperada:
```bash
{'status': 'ok', 'result': 8}
{'status': 'ok', 'result': 28}
{'status': 'ok', 'result': 'hola desde cliente'}
```
### 4️⃣ Iniciar el servidor RMI

En una nueva terminal:
```bash
python3 rmi_server.py
```

Salida esperada:
```bash
RMI server listening on 127.0.0.1:<puerto>
```
### 5️⃣ Ejecutar el cliente RMI

En otra terminal:
```bash
python3 rmi_client.py
```

Salida esperada:
```python
object id: <uuid>
{'status': 'ok', 'result': 'Hola Nacho desde RMI object'}
{'status': 'ok', 'result': 30}
```
---
## 🧮 Ejemplo de flujo RPC y RMI

**RPC:**

1. rpc_server registra el servicio calculator_service en el SIN.
2. rpc_client hace LOOKUP en el SIN y obtiene la dirección del servidor.
3. Se invocan métodos remotos (add, mul, echo) usando JSON sobre TCP.

**RMI:**

1. rmi_server se registra como rmi_host en el SIN.
2. rmi_client solicita la exportación de un objeto (EXPORT) y recibe un object_id.
3. Luego invoca métodos sobre ese objeto remoto (greet, add).
---
## 🧱 Requisitos

- Python 3.8 o superior
- Sistema operativo: Linux / macOS / Windows
- No requiere librerías externas (solo módulos estándar)
---
## 🧰 Estructura del repositorio
```bash
.
├── sin_name_service.py
├── rpc_server.py
├── rpc_client.py
├── rmi_server.py
├── rmi_client.py
├── utils_protocol.py
└── README.md
```

