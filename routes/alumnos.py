from flask_restx import Namespace, Resource, fields
from flask import request, current_app
from config import db
from models.alumno import Alumno
from datetime import datetime
from functools import wraps
import jwt

ns = Namespace('students', description='Operaciones con alumnos')

alumno_modelo = ns.model('Alumno', {
    'nombre': fields.String(required=True, description='Nombre del alumno'),
    'apellido_paterno': fields.String(required=True, description='Apellido paterno'),
    'apellido_materno': fields.String(required=True, description='Apellido materno'),
    'matricula': fields.String(required=True, description='Matrícula del alumno'),
    'correo': fields.String(required=True, description='Correo electrónico')
})

alumno_respuesta = ns.model('AlumnoRespuesta', {
    'id': fields.Integer(description='ID del alumno'),
    'nombre': fields.String(description='Nombre del alumno'),
    'apellido_paterno': fields.String(description='Apellido paterno'),
    'apellido_materno': fields.String(description='Apellido materno'),
    'matricula': fields.String(description='Matrícula del alumno'),
    'correo': fields.String(description='Correo electrónico'),
    'fecha_alta': fields.String(description='Fecha de alta')
})


def token_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            parts = auth_header.split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]

        if not token:
            return {'mensaje': 'Token no proporcionado'}, 401

        try:
            jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return {'mensaje': 'Token expirado'}, 401
        except jwt.InvalidTokenError:
            return {'mensaje': 'Token inválido'}, 401

        return f(*args, **kwargs)
    return decorador


@ns.route('/')
class AlumnoList(Resource):
    @ns.doc('listar_alumnos', params={
        'fecha_inicio': 'Filtrar desde fecha (YYYY-MM-DD)',
        'fecha_fin': 'Filtrar hasta fecha (YYYY-MM-DD)'
    })
    def get(self):
        """Listar alumnos (con filtro opcional por rango de fechas)"""
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            try:
                inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
                fin = datetime.strptime(fecha_fin, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
            except ValueError:
                return {'mensaje': 'Formato de fecha inválido. Usa YYYY-MM-DD'}, 400

            alumnos = Alumno.query.filter(Alumno.fecha_alta >= inicio, Alumno.fecha_alta <= fin).all()
        else:
            alumnos = Alumno.query.all()

        return [a.to_dict() for a in alumnos]

    @ns.doc('crear_alumno', security='Bearer')
    @ns.expect(alumno_modelo)
    @token_requerido
    def post(self):
        """Crear un nuevo alumno (requiere JWT)"""
        datos = ns.payload

        if not datos.get('nombre') or not datos.get('matricula') or not datos.get('correo'):
            return {'mensaje': 'Campos nombre, matricula y correo son obligatorios'}, 400

        if Alumno.query.filter_by(matricula=datos['matricula']).first():
            return {'mensaje': 'La matrícula ya existe'}, 400

        nuevo_alumno = Alumno(
            nombre=datos['nombre'],
            apellido_paterno=datos['apellido_paterno'],
            apellido_materno=datos['apellido_materno'],
            matricula=datos['matricula'],
            correo=datos['correo']
        )
        db.session.add(nuevo_alumno)
        db.session.commit()
        return {'mensaje': 'Alumno creado', 'alumno': nuevo_alumno.to_dict()}, 201


@ns.route('/<int:id>')
@ns.param('id', 'ID del alumno')
class AlumnoResource(Resource):
    @ns.doc('obtener_alumno')
    def get(self, id):
        """Obtener un alumno por ID"""
        alumno = Alumno.query.get(id)
        if not alumno:
            return {'mensaje': 'Alumno no encontrado'}, 404
        return alumno.to_dict()

    @ns.doc('actualizar_alumno', security='Bearer')
    @ns.expect(alumno_modelo)
    @token_requerido
    def put(self, id):
        """Actualizar un alumno (requiere JWT)"""
        alumno = Alumno.query.get(id)
        if not alumno:
            return {'mensaje': 'Alumno no encontrado'}, 404

        datos = ns.payload
        alumno.nombre = datos['nombre']
        alumno.apellido_paterno = datos['apellido_paterno']
        alumno.apellido_materno = datos['apellido_materno']
        alumno.matricula = datos['matricula']
        alumno.correo = datos['correo']
        db.session.commit()
        return {'mensaje': 'Alumno actualizado', 'alumno': alumno.to_dict()}

    @ns.doc('eliminar_alumno', security='Bearer')
    @token_requerido
    def delete(self, id):
        """Eliminar un alumno (requiere JWT)"""
        alumno = Alumno.query.get(id)
        if not alumno:
            return {'mensaje': 'Alumno no encontrado'}, 404

        db.session.delete(alumno)
        db.session.commit()
        return {'mensaje': 'Alumno eliminado'}
