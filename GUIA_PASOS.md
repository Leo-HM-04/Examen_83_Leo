# Guía Paso a Paso - Examen Backend con JWT y CI/CD

## Tabla de Contenidos

1. [Resumen del Proyecto](#resumen-del-proyecto)
2. [Endpoints de la API](#endpoints-de-la-api)
3. [Cómo Probar la API](#cómo-probar-la-api)
4. [Instalar Dependencias](#instalar-dependencias)
5. [Desvincular Repositorio Actual y Vincular a GitHub](#desvincular-repositorio-actual-y-vincular-a-github)
6. [Configurar GitLab con CI/CD](#configurar-gitlab-con-cicd)
7. [Flujo de Ramas (Git Flow)](#flujo-de-ramas-git-flow)

---

## Resumen del Proyecto

API REST para la gestión de alumnos con:

- CRUD completo de alumnos
- Filtro por rango de fechas
- Autenticación JWT
- Protección de rutas (POST, PUT, DELETE requieren token)
- Documentación Swagger en `/docs`
- Pipeline CI/CD con GitLab

---

## Endpoints de la API

### Auth

| Método | Endpoint         | Descripción              | Protegido |
|--------|------------------|--------------------------|-----------|
| POST   | `/auth/registro` | Registrar usuario        | No        |
| POST   | `/auth/login`    | Login (retorna JWT)      | No        |

### Students

| Método | Endpoint         | Descripción                        | Protegido |
|--------|------------------|------------------------------------|-----------|
| GET    | `/students/`     | Listar alumnos (con filtro fecha)  | No        |
| GET    | `/students/{id}` | Obtener alumno por ID              | No        |
| POST   | `/students/`     | Crear alumno                       | Sí (JWT)  |
| PUT    | `/students/{id}` | Actualizar alumno                  | Sí (JWT)  |
| DELETE | `/students/{id}` | Eliminar alumno                    | Sí (JWT)  |

### Filtro por Fechas

```
GET /students/?fecha_inicio=2026-03-25&fecha_fin=2026-03-26
```

---

## Cómo Probar la API

### 1. Registrar un usuario

```
POST http://localhost:5000/auth/registro
Content-Type: application/json

{
    "username": "admin",
    "password": "admin123"
}
```

### 2. Hacer Login y obtener el JWT

```
POST http://localhost:5000/auth/login
Content-Type: application/json

{
    "username": "admin",
    "password": "admin123"
}
```

**Respuesta:**
```json
{
    "mensaje": "Login exitoso",
    "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

### 3. Crear un alumno (con token)

```
POST http://localhost:5000/students/
Content-Type: application/json
Authorization: Bearer <tu_token_aquí>

{
    "nombre": "Leonardo",
    "apellido_paterno": "Pérez",
    "apellido_materno": "García",
    "matricula": "A001",
    "correo": "leonardo@correo.com"
}
```

### 4. Listar alumnos (público)

```
GET http://localhost:5000/students/
```

### 5. Obtener alumno por ID (público)

```
GET http://localhost:5000/students/1
```

### 6. Actualizar alumno (con token)

```
PUT http://localhost:5000/students/1
Content-Type: application/json
Authorization: Bearer <tu_token_aquí>

{
    "nombre": "Leonardo Updated",
    "apellido_paterno": "Pérez",
    "apellido_materno": "García",
    "matricula": "A001",
    "correo": "leonardo.updated@correo.com"
}
```

### 7. Eliminar alumno (con token)

```
DELETE http://localhost:5000/students/1
Authorization: Bearer <tu_token_aquí>
```

### 8. Filtrar por fecha (público)

```
GET http://localhost:5000/students/?fecha_inicio=2026-04-01&fecha_fin=2026-04-30
```

### 9. Documentación Swagger

Abrir en el navegador: `http://localhost:5000/docs`

---

## Instalar Dependencias

```bash
# Activar el entorno virtual
cd ExamenLeo
.\Scripts\Activate.ps1    # PowerShell
# o
.\Scripts\activate.bat    # CMD

# Volver a la raíz del proyecto
cd ..

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecutar la API

```bash
python app.py
```

La API estará disponible en `http://localhost:5000`

---

## Desvincular Repositorio Actual y Vincular a GitHub

### Paso 1: Desvincular el repositorio actual

```bash
# Ver el remote actual
git remote -v

# Eliminar el remote actual
git remote remove origin
```

### Paso 2: Crear repositorio nuevo en GitHub

1. Ve a https://github.com/new
2. Nombre del repositorio: `Examen_83` (o el nombre que prefieras)
3. Déjalo **público** o **privado** según prefieras
4. **NO** inicialices con README, .gitignore ni licencia
5. Click en **"Create repository"**

### Paso 3: Vincular al nuevo repositorio de GitHub

```bash
# Reemplaza TU_USUARIO con tu usuario de GitHub
git remote add origin https://github.com/TU_USUARIO/Examen_83.git

# Verificar que se vinculó correctamente
git remote -v
```

### Paso 4: Subir el proyecto a GitHub

```bash
# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Examen Backend - API REST con JWT y CI/CD"

# Subir a la rama main
git branch -M main
git push -u origin main
```

---

## Configurar GitLab con CI/CD

### Paso 1: Crear proyecto en GitLab

1. Ve a https://gitlab.com/projects/new
2. Click en **"Create blank project"**
3. Nombre: `Examen_83`
4. Visibilidad: **Public** o **Private**
5. **Desmarca** "Initialize repository with a README"
6. Click en **"Create project"**

### Paso 2: Agregar GitLab como remote adicional

```bash
# Agregar GitLab como segundo remote
# Reemplaza TU_USUARIO_GITLAB con tu usuario de GitLab
git remote add gitlab https://gitlab.com/TU_USUARIO_GITLAB/Examen_83.git

# Verificar los remotes
git remote -v
# Deberías ver tanto 'origin' (GitHub) como 'gitlab' (GitLab)
```

### Paso 3: Subir a GitLab

```bash
# Subir rama main a GitLab
git push gitlab main
```

### Paso 4: Crear la rama develop

```bash
# Crear rama develop desde main
git checkout -b develop

# Subir develop a GitLab
git push gitlab develop
```

### Paso 5: Crear la rama feature/jwt-auth

```bash
# Crear rama feature/jwt-auth desde develop
git checkout -b feature/jwt-auth

# Hacer un commit en esta rama (puede ser un cambio pequeño o simplemente push)
git push gitlab feature/jwt-auth
```

### Paso 6: Merge feature/jwt-auth → develop

```bash
# Cambiar a develop
git checkout develop

# Merge de feature/jwt-auth
git merge feature/jwt-auth

# Push a GitLab (esto dispara el pipeline de DEV)
git push gitlab develop
```

### Paso 7: Verificar pipeline DEV en GitLab

1. Ve a tu proyecto en GitLab
2. En el menú lateral: **Build > Pipelines**
3. Deberías ver un pipeline ejecutándose para la rama `develop`
4. Verifica que los jobs `build_dev` y `test_dev` pasen ✅

### Paso 8: Merge develop → main

```bash
# Cambiar a main
git checkout main

# Merge de develop
git merge develop

# Push a GitLab (esto dispara el pipeline de PROD)
git push gitlab main
```

### Paso 9: Verificar pipeline PROD en GitLab

1. Ve a **Build > Pipelines** en GitLab
2. Deberías ver un pipeline ejecutándose para la rama `main`
3. Verifica que los jobs `build_prod` y `test_prod` pasen ✅

### Paso 10: También subir todo a GitHub

```bash
# Subir todas las ramas a GitHub también
git push origin main
git checkout develop
git push origin develop
git checkout feature/jwt-auth
git push origin feature/jwt-auth
```

---

## Flujo de Ramas (Git Flow)

```
feature/jwt-auth  →  develop  →  main
      │                 │           │
      │           Pipeline DEV    Pipeline PROD
      │            (build+test)   (build+test)
      └── Implementación JWT
```

### Resumen del flujo:

1. ✅ `feature/jwt-auth` — Se implementa la autenticación JWT
2. ✅ Merge a `develop` — Se ejecuta pipeline DEV automáticamente
3. ✅ Validación en DEV — Se verifica que todo funcione
4. ✅ Merge a `main` — Se ejecuta pipeline PROD automáticamente
5. ✅ Producción lista

---

## Estructura del Proyecto

```
Examen_83/
├── app.py                  # Punto de entrada de la API
├── config.py               # Configuración de Flask y BD
├── requirements.txt        # Dependencias del proyecto
├── .gitlab-ci.yml          # Pipeline CI/CD
├── .gitignore              # Archivos ignorados por Git
├── GUIA_PASOS.md           # Esta guía
├── models/
│   ├── __init__.py
│   ├── alumno.py           # Modelo de Alumno
│   └── usuario.py          # Modelo de Usuario
└── routes/
    ├── __init__.py
    ├── alumnos.py           # Rutas CRUD de alumnos (con JWT)
    └── auth.py              # Rutas de autenticación (JWT)
```

---

## Notas Importantes

- La base de datos es MySQL: `examen_leo` en localhost
- Asegúrate de tener MySQL corriendo y la base de datos creada
- Las tablas se crean automáticamente al iniciar la app
- El token JWT expira en 2 horas
- Swagger está disponible en `/docs`
