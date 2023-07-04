import sqlite3
from flask import Flask


DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'admin123'


    create_database()

    # Import blueprints after creating the database
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/views')
    app.register_blueprint(auth, url_prefix='/')

    return app

def create_database():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS user (
                    CIN TEXT PRIMARY KEY UNIQUE,
                    Fname TEXT NOT NULL,
                    Lname TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    type_u TEXT
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS supplier (
                    Matricule INTEGER PRIMARY KEY,
                    name TEXT,
                    email TEXT UNIQUE,
                    adresse TEXT,
                    Tel INTEGER UNIQUE
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS product (
                    Code INTEGER PRIMARY KEY,
                    Libelle TEXT,
                    QTE INTEGER,
                    PU_A INTEGER,
                    PU_V INTEGER
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS client (
                    CIN_C TEXT PRIMARY KEY,
                    name TEXT,
                    email TEXT UNIQUE,
                    adresse TEXT,
                    Tel INTEGER UNIQUE
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS sale (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    Montant INTEGER,
                    client_id TEXT,
                    produits INTEGER,
                    FOREIGN KEY (client_id) REFERENCES client (CIN_C),
                    FOREIGN KEY (produits) REFERENCES product (Code)
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS shipment (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    Montant INTEGER,
                    Supplier_id TEXT,
                    produits INTEGER,
                    FOREIGN KEY (Supplier_id) REFERENCES supplier (Matricule),
                    FOREIGN KEY (produits) REFERENCES product (Code)
                )''')

    conn.commit()
    conn.close()
    print('Created Database!')



def get_product_list():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT Libelle FROM product , shipment Where product.Code = shipment.produits")
    products = c.fetchall()
    conn.close()
    return products