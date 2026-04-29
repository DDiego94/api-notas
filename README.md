Task Manager API

📌 Descripción

API REST desarrollada con FastAPI para la gestión de tareas y usuarios. Permite registro, autenticación mediante JWT y operaciones CRUD sobre tareas.

🚀 Tecnologías

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker
- JWT Authentication

⚙️ Funcionalidades

- Registro de usuarios
- Login con autenticación JWT
- CRUD de tareas
- Relación usuario - tareas
- Validación de datos con Pydantic

🐳 Ejecución con Docker

docker-compose up --build

🔗 Endpoints principales

- POST /register → Crear usuario
- POST /login → Obtener token JWT
- GET /tasks → Listar tareas
- POST /tasks → Crear tarea
- PUT /tasks/{id} → Actualizar tarea
- DELETE /tasks/{id} → Eliminar tarea

📈 Objetivo del proyecto

Simular un backend real listo para producción, aplicando buenas prácticas de desarrollo, estructura modular y autenticación segura.

👨‍💻 Autor

Diego Ditter
