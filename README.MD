# LEADS
## Introducción
Esta aplicación tiene como fin permitir la carga de estudiantes en una base de datos a traves del endpoint "POST /estudiantes", también tiene como propósito el envio de la información previamente cargada a traves de solicitudes GET a los enpoints /resultados y resultados /{registro_id}. 
Los endpoints estan segurizados con JWT, para evitar el uso de personal no previamente autorizado para su uso.
La base de datos usada es PostgreSQL y se empaqueto el proyecto usando Docker-compose.
## Endpoints
### POST /login
Al enviarle el formulario con usuario y contraseña correcta, nos envia un token que se debe agregar como header de autorización. Esta funcionalidad se hizo con JWT, para la segurización de todos los endpoints.
Un ejemplo de los datos esperados por este endpoint:

{
  "email": "string@example.com",
  "password": "string"
}

### GET /estudiantes/
Carga un template HTML en el cual hay un formulario para ingresar los valores requeridos para cargar un estudiante y también hay un script que se encarga de transformar estos valores en un formato JSON legible por el endpoint siguiente y enviar una solicitud POST al apretar el boton de guardado del formulario.
Las funciones obtener_carreras y obtener_materias se encargan retornar todas las carreras y materias al template para que aparezcan como opciones en el formulario.
### POST /estudiantes/
Recibe el JSON previamente formulado y verifica que el correo no haya sido usado previamente, en ese caso envia una respuesta acorde.
Luego se verifica que todas las carreras que se enviaron a través del formulario existan en la base de datos. En caso de que alguna carrera o materia no esté presente en la BBDD, se retornará un error.
También estan los validadores de campos específicos, que se comentaran mas adelante.
Luego de todas las validaciones, se agrega el nuevo estudiante a la base de datos y retorna un mensaje de éxito y el id del estudiante cargado.

Se adjunta un ejemplo de JSON para ser cargado en este endpoint:

{
  "nombre_completo": "Juan Pérez",
  "correo": "juan@example.com",
  "direccion": "Calle Falsa 123",
  "telefono": "123456789",
  "edad": 20,
  "carreras": ["Ingeniería"],
  "materias": ["Ingeniería - Cálculo", "Ingeniería - Física"]
}

### GET /resultados/
Al recibir una solicitud, responde con todos los resultados de la base de datos de estudiantes, paginados de a 10 entradas y ordenados por ID de estudiante.
### GET /resultados/{registro_id}
Permite hacer una búsqueda por ID de estudiante y nos devuelve la información del mismo en formato JSON.
## Modelos y validacion:
### Estudiante:
Modelo de estudiante para la base de datos PostgreSQL

- id: Identificador único del estudiante (int) 
- nombre_completo: Nombre completo del estudiante (str, min=3, max=100 carácteres).
- correo: Dirección de correo electrónico del estudiante (EmailStr)
- direccion: Dirección del estudiante (str,min_length=7, max_length=100)
- telefono: Número de teléfono del estudiante(str, se valida que solo haya numeros).
- edad:  Edad del estudiante (int, min=18).

#### Relaciones:

- Carreras: Lista de carreras asociadas al estudiante.
- Materias: Lista de materias en las que está inscrito el estudiante.

---

### Carrera
Modelo de Carrera para la base de datos PostgreSQL.

- id:  Identificador único de la carrera(Integer).
- nombre: Nombre de la carrera (str).

#### Relaciones:

- estudiantes: Lista de estudiantes asociados a esta carrera.
- materias: Lista de materias asociadas a esta carrera.

---

### Materia
Modelo de Materia para la base de datos PostgreSQL.

- id: Identificador único de la materia (Integer).
- nombre: Nombre de la materia (str).

#### Relaciones:

- carrera:  Carrera a la que pertenece esta materia.
- estudiante: Estudiante asociado a esta materia.

## Seguridad

Para poder hacer uso de los endpoints, se debe tener un header de autorizacion de este tipo:

-H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWluQGdtYWlsLmNvbSIsInBhc3N3b3JkIjoiYWRtaW4ifQ.__YSG1TZyvJ-z7cxtBg5OyHqGFYmqW_Sd15ZqIr6B8E'

Este mismo se genera ingresando las credenciales siguientes en el endponit /login:

{
  "email": "admin@gmail.com",
  "password": "admin"
}

## Estructura del proyecto:

- Dockerfile: Archivo de configuración de imagen de docker
- README.MD: Este archivo
- config :
  - database.py : Archivo donde se declara la conexión a la base de datos
- docker-compose.yml: Archivo de configuración de Docker-compose
- jwt_manager.py: Creación y Validación de tokens
- main.py: Archivo de ejecucion del proyecto.
- middleware
  - jwt_bearer.py: Archivo de configuración de bearer de JWT
- models
  - models.py: Modelos SQLALchemy de la aplicación
- requirements.txt: Requerimientos de la aplicación
- routers 
  - estudiante.py : Mini app de procesado y busqueda de estudiantes
  - user.py : Mini app de carga y procesado de token para el usuario
- schemas
  - estudiante_schema.py : Validaciones de pydantic para el modelo estudiante
  - user_schema.py : Validaciones de pydantic para user
- templates
  - estudiante_form.html: Html con formulario de ingreso de estudiante