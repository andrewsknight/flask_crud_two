# API REST de Usuarios con Flask y PostgreSQL

Una API REST completa para gestión de usuarios construida con Flask y PostgreSQL, que incluye operaciones CRUD, encriptación de contraseñas y manejo de variables de entorno.

## 🚀 Características

- ✅ **CRUD completo**: Crear, leer, actualizar y eliminar usuarios
- ✅ **Seguridad**: Contraseñas encriptadas con `pbkdf2:sha256`
- ✅ **Base de datos**: PostgreSQL con conexiones optimizadas
- ✅ **Variables de entorno**: Configuración flexible con `.env`
- ✅ **API REST**: Endpoints RESTful bien estructurados
- ✅ **Validación**: Manejo de errores y validaciones
- ✅ **Docker Ready**: Compatible con el setup de PostgreSQL

## 📋 Requisitos Previos

- Python 3.8+
- PostgreSQL (puede usar el Docker setup del proyecto anterior)
- pip (gestor de paquetes de Python)

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd <nombre-del-proyecto>
```

### 2. Crear entorno virtual
```bash
python -m venv venv

# En Linux/Mac
source venv/bin/activate

# En Windows
venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crea un archivo `.env` en la raíz del proyecto:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=midb
DB_USER=andres
DB_PASSWORD=mi_password_segura
```

### 5. Ejecutar la aplicación
```bash
python app.py
```

La API estará disponible en: `http://localhost:5000`

## 📁 Estructura del Proyecto

```
proyecto/
├── app.py                  # Aplicación principal Flask
├── ddbb/
│   └── connection.py       # Módulo de conexión a PostgreSQL
├── requirements.txt        # Dependencias Python
├── .env                   # Variables de entorno (crear)
└── README.md              # Este archivo
```

## 🔗 Endpoints de la API

### Base URL: `http://localhost:5000`

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/usuarios` | Crear nuevo usuario |
| `GET` | `/usuarios` | Listar todos los usuarios |
| `GET` | `/usuarios/<id>` | Obtener usuario por ID |
| `PUT` | `/usuarios/<id>` | Actualizar usuario |
| `DELETE` | `/usuarios/<id>` | Eliminar usuario |

## 📝 Ejemplos de Uso

### 1. Crear Usuario
```bash
curl -X POST http://localhost:5000/usuarios \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "email": "juan@example.com",
    "password": "mi_password_123"
  }'
```

**Respuesta:**
```json
{
  "id": 1,
  "nombre": "Juan Pérez",
  "email": "juan@example.com",
  "password": "pbkdf2:sha256:...",
  "fecha_creacion": "2025-06-03T10:30:00"
}
```

### 2. Listar Todos los Usuarios
```bash
curl -X GET http://localhost:5000/usuarios
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "nombre": "Juan Pérez",
    "email": "juan@example.com",
    "password": "pbkdf2:sha256:...",
    "fecha_creacion": "2025-06-03T10:30:00"
  }
]
```

### 3. Obtener Usuario por ID
```bash
curl -X GET http://localhost:5000/usuarios/1
```

### 4. Actualizar Usuario
```bash
curl -X PUT http://localhost:5000/usuarios/1 \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Carlos Pérez",
    "email": "juan.carlos@example.com",
    "password": "nuevo_password_456"
  }'
```

### 5. Eliminar Usuario
```bash
curl -X DELETE http://localhost:5000/usuarios/1
```

**Respuesta:**
```json
{
  "deleted": {
    "id": 1,
    "nombre": "Juan Pérez",
    "email": "juan@example.com"
  }
}
```

## 🗄️ Esquema de Base de Datos

La tabla `usuarios` se crea automáticamente con la siguiente estructura:

```sql
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## ⚙️ Configuración

### Variables de Entorno Disponibles

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `DB_HOST` | Host de PostgreSQL | `localhost` |
| `DB_PORT` | Puerto de PostgreSQL | `5432` |
| `DB_NAME` | Nombre de la base de datos | `midb` |
| `DB_USER` | Usuario de PostgreSQL | `andres` |
| `DB_PASSWORD` | Contraseña de PostgreSQL | `mi_password_segura` |

## 🐳 Usar con Docker PostgreSQL

Si tienes el setup de PostgreSQL con Docker del proyecto anterior:

1. **Ejecutar PostgreSQL:**
   ```bash
   cd ../postgres  # Si está en carpeta hermana
   ./run-postgres.sh
   ```

2. **Verificar conexión:**
   ```bash
   docker ps  # Verificar que PostgreSQL esté corriendo
   ```

3. **Ejecutar la API:**
   ```bash
   python app.py
   ```

## 🔧 Dependencias (requirements.txt)

```txt
Flask==2.3.3
psycopg2-binary==2.9.7
python-dotenv==1.0.0
Werkzeug==2.3.7
```

## 🧪 Pruebas con Postman/Insomnia

Puedes importar esta colección para probar todos los endpoints:

**Crear Usuario:**
- URL: `POST http://localhost:5000/usuarios`
- Body (JSON):
  ```json
  {
    "nombre": "Test User",
    "email": "test@example.com",
    "password": "test123"
  }
  ```

## ⚠️ Solución de Problemas

### Error de conexión a PostgreSQL
1. Verifica que PostgreSQL esté corriendo: `docker ps`
2. Revisa las credenciales en `.env`
3. Confirma que el puerto 5432 esté libre

### Error "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Error "tabla no existe"
La tabla se crea automáticamente al iniciar la app. Si hay problemas:
```python
# Ejecutar una vez para crear manualmente
from app import crear_tabla
crear_tabla()
```

## 🔒 Seguridad

- ✅ Contraseñas encriptadas con `pbkdf2:sha256`
- ✅ Email único por usuario
- ✅ Validación de entrada JSON
- ⚠️ **Para producción**: Agregar autenticación JWT, rate limiting, HTTPS

## 🚀 Mejoras Futuras

- [ ] Autenticación JWT
- [ ] Validación de email
- [ ] Paginación en listado
- [ ] Filtros de búsqueda
- [ ] Tests unitarios
- [ ] Documentación con Swagger
- [ ] Rate limiting
- [ ] Logs estructurados

## 📄 Licencia

Este proyecto es de uso libre para fines educativos y de desarrollo.

---

**¿Necesitas ayuda?** Abre un issue en el repositorio o revisa la sección de solución de problemas.# flask_crud_two
