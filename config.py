from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/examen_leo'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'clave_secreta_examen'
    app.config['JWT_SECRET_KEY'] = 'jwt_secret_examen_leo_2026'

    db.init_app(app)

    return app
