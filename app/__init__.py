from flask import Flask
from .database import db
from .main.main import main
from .admin.admin import admin


def create_app():
    app = Flask(__name__)
    app.config.from_object(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dnevnik.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '89cc5d9cb82627334e1af8b5ed890c116378c55d652160277b4f445ec7c5e37e'
    app.config['FLASK_ENV'] = 'development'

    db.init_app(app)

    app.register_blueprint(main, url_prefix='/main')
    app.register_blueprint(admin, url_prefix='/admin')

    return app