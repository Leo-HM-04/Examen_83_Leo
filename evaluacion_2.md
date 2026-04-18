# 🧪 Examen Técnico Backend 2

📅 **Fecha:** 2026-04-18
⏱️ **Horario:** 8:40 a 12:00

---

## 🎯 Objetivo

Desarrollar una API REST para la gestión de alumnos, implementando autenticación con **JWT**, buenas prácticas de arquitectura y un pipeline básico de **CI/CD con GitLab**.

---

## 📌 Requerimientos

### 👨‍🎓 CRUD de Alumnos

Implementar operaciones:

* Crear alumno
* Listar alumnos
* Obtener alumno por ID
* Actualizar alumno
* Eliminar alumno

---

### 📄 Estructura del Alumno

Campos mínimos:

* nombre
* apellido_paterno
* apellido_materno
* matricula
* correo
* fecha_alta (auto-generada)

---

### 🔎 Filtro por Fechas

Endpoint para consultar alumnos por rango de fecha:

```id="filtro1"
GET /students?fecha_inicio=2026-03-25&fecha_fin=2026-03-26
```

Formato requerido:

* `YYYY-MM-DD`

---

### 🔐 Autenticación (JWT)

* Endpoint de login:

```id="login1"
POST /auth/login
```

* Recibe:

  * usuario
  * contraseña

* Retorna:

  * token JWT

---

### 🔒 Protección de Rutas

Requieren token:

* POST /students
* PUT /students/{id}
* DELETE /students/{id}

Públicos:

* GET /students
* GET /students/{id}

---

## 📚 Endpoints

### 🔹 Auth

| Método | Endpoint    | Descripción |
| ------ | ----------- | ----------- |
| POST   | /auth/login | Genera JWT  |

---

### 🔹 Alumnos

| Método | Endpoint       | Descripción       |
| ------ | -------------- | ----------------- |
| GET    | /students      | Listar alumnos    |
| GET    | /students/{id} | Obtener alumno    |
| POST   | /students      | Crear alumno      |
| PUT    | /students/{id} | Actualizar alumno |
| DELETE | /students/{id} | Eliminar alumno   |

---

## 📄 Documentación

Disponible en Swagger:

```id="docs1"
/docs
```

---

## ⚙️ Manejo de Errores


---

# ⚙️ CI/CD con GitLab

Se implementa un pipeline básico usando **GitLab CI/CD** con dos ambientes:

* 🧪 **dev**
* 🚀 **prod**

---



## 🔁 Flujo

* Push a `develop` → ejecuta **dev**
* Push a `main` → ejecuta **prod**

---

## 🎯 Objetivo del CI/CD

* Validar pipeline funcional
* Separación de entornos
* Automatización básica

---

## 🌿 Control de Versiones

Ramas requeridas:

* main
* develop
* feature/jwt-auth

Flujo:

1. Crear `feature/jwt-auth`
2. Implementar autenticación
3. Merge → develop
4. Validación CI/CD
5. Merge → main

---

## 🧠 Buenas prácticas esperadas

* Código limpio
* Separación de responsabilidades
* Validaciones de datos
* Uso correcto de JWT
* Manejo de errores consistente



## 🚀 Frase Motivacional

> "No se trata de escribir código perfecto, sino de resolver problemas de forma inteligente. Cada error es un paso más hacia convertirte en un mejor desarrollador."




