from config import create_app, db
from flask_restx import Api
from routes.alumnos import ns as alumnos_ns
from routes.auth import ns as auth_ns

app = create_app()

api = Api(app,
    title='API Gestión de Alumnos',
    version='1.0',
    description='API REST para la gestión de alumnos con autenticación JWT',
    doc='/docs',
    authorizations={
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Escribe: Bearer <tu_token>'
        }
    }
)

api.add_namespace(alumnos_ns, path='/students')
api.add_namespace(auth_ns, path='/auth')

with app.app_context():
    from models.alumno import Alumno
    from models.usuario import Usuario
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
