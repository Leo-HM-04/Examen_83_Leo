from flask_restx import Namespace, Resource, fields
from config import db
from models.usuario import Usuario
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
import jwt
import datetime

ns = Namespace('auth', description='Autenticación')

login_modelo = ns.model('Login', {
    'username': fields.String(required=True, description='Nombre de usuario'),
    'password': fields.String(required=True, description='Contraseña')
})

registro_modelo = ns.model('Registro', {
    'username': fields.String(required=True, description='Nombre de usuario'),
    'password': fields.String(required=True, description='Contraseña')
})


@ns.route('/registro')
class Registro(Resource):
    @ns.doc('registrar_usuario')
    @ns.expect(registro_modelo)
    def post(self):
        """Registrar un nuevo usuario"""
        datos = ns.payload

        if Usuario.query.filter_by(username=datos['username']).first():
            return {'mensaje': 'El usuario ya existe'}, 400

        nuevo_usuario = Usuario(
            username=datos['username'],
            password=generate_password_hash(datos['password'])
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return {'mensaje': 'Usuario registrado correctamente'}, 201


@ns.route('/login')
class Login(Resource):
    @ns.doc('login')
    @ns.expect(login_modelo)
    def post(self):
        """Iniciar sesión y obtener token JWT"""
        datos = ns.payload
        usuario = Usuario.query.filter_by(username=datos['username']).first()

        if not usuario or not check_password_hash(usuario.password, datos['password']):
            return {'mensaje': 'Usuario o contraseña incorrectos'}, 401

        token = jwt.encode({
            'user_id': usuario.id,
            'username': usuario.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

        return {'mensaje': 'Login exitoso', 'token': token}
