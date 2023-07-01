from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func 

class User(db.Model, UserMixin):
        CIN_U = db.Column(db.String(20), primary_key=True, unique=True)
        Fname = db.Column(db.String(20))
        Lname = db.Column(db.String(20))
        email = db.Column(db.String(150), unique=True)
        password = db.Column(db.String(20))
        type_u = db.Column(db.String)

class Supplier(db.Model):
        Matricule = db.Column(db.Integer, primary_key=True, unique=True)
        name = db.Column(db.String(20))
        email = db.Column(db.String(150), unique = True)
        adresse = db.Column(db.String(150))
        Tel = db.Column(db.Integer, unique= True)

class Product(db.Model): 
        Code = db.Column(db.Integer, primary_key=True, unique=True)
        Libelle = db.Column(db.String(20))
        QTE = db.Column(db.Integer)
        PU_A = db.Column(db.Integer)
        PU_V = db.Column(db.Integer)

class Client(db.Model):
        CIN_C = db.Column(db.String(20), primary_key=True, unique=True)
        name = db.Column(db.String(20))
        email = db.Column(db.String(150), unique = True)
        adresse = db.Column(db.String(150))
        Tel = db.Column(db.Integer, unique= True)

class Sale(db.Model):
        id =  db.Column(db.Integer, primary_key=True, unique=True, autoincrement= True)
        date = db.Column(db.DateTime(timezone=True), default=func.now())
        Montant = db.Column(db.Integer)
        client_id = db.Column(db.String, db.ForeignKey('client.CIN_C'))
        produits = db.Column(db.Integer , db.ForeignKey('produit.Code'))
        products = db.relationship('Product')


class Shipment(db.Model):
        id =  db.Column(db.Integer, primary_key=True, unique=True, autoincrement= True)
        date = db.Column(db.DateTime(timezone=True), default=func.now())
        Montant = db.Column(db.Integer)
        Supplier_id = db.Column(db.String, db.ForeignKey('supplier.Matricule'))
        produits = db.Column(db.Integer , db.ForeignKey('produit.Code'))
        products = db.relationship('Product')

         




        