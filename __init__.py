from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'admin123'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)  # Initialiser db avec l'application Flask

    # Importer les blueprints avant l'enregistrement
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/views')
    app.register_blueprint(auth, url_prefix='/')

    # Importer les tables après l'initialisation de db
    from .models import User, Supplier, Product, Client, Sale, Shipment

    create_database(app)  # Appeler la fonction sans argument

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')
