from flask import Blueprint, render_template , request , redirect 
from .models import User , Client , Product , Supplier , Shipment , Sale, db 
from werkzeug.security import check_password_hash

import re 



auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        CIN = request.form.get('CIN')
        password = request.form.get('password')

        # Vérification du modèle CIN
        cin_pattern = r"[A-Z]{2}[0-9]{5}"
        if not re.match(cin_pattern, CIN):
            error = "CIN invalide. Veuillez entrer un CIN valide."
            return render_template('login.html', error=error)

        # Vérification de l'utilisateur dans la base de données
        user = User.query.filter_by(CIN_U=CIN).first()
        if not user or not check_password_hash(user.password, password):
            error = "CIN ou mot de passe incorrect."
            return render_template('login.html', error=error)

        # Redirection en fonction du type d'utilisateur
        if user.type_u == 1:
            return redirect('/page1')
        elif user.type_u == 2:
            return redirect('/page2')
        elif user.type_u == 3:
            return redirect('/page3')
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<p> logout </p>"

@auth.route('/add_user', methods= ['GET','POST'])
def add_user():
    if request.method == 'POST':
        CIN = request.form.get('CIN')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        # Vérification du format CIN
        cin_pattern = r"[A-Z]{2}[0-9]{5}"
        if not re.match(cin_pattern, CIN):
            error = "CIN invalide. Veuillez entrer un CIN valide."
            return render_template('add_client.html', error=error)
        
         # Vérifie la valeur de 'role' et attribue la valeur correspondante à 'type_u'
        if role == 'option1':
            User.type_u = '1'
        elif role == ' option2':
            User.type_u = '2'
        elif role == 'option3':
            User.type_u = '3'
        else:
            return 'Erreur : aucun rôle sélectionné'

        # Créez un nouvel objet User et affectez les valeurs des champs
        new_user = User(CIN_U=CIN, Fname=first_name, Lname=last_name, email=email, password=password, type_u=role)

        # Ajoutez le nouvel utilisateur à la base de données
        db.session.add(new_user)
        db.session.commit()

    return render_template("add_user.html")

@auth.route('/add_client', methods= ['GET','POST'])
def add_client(): 
    if request.method == 'POST':
        # Récupérer les données du formulaire
        cin = request.form.get('cin')
        name = request.form.get('name')
        email = request.form.get('email')
        adresse = request.form.get('adresse')
        tel = request.form.get('tel')

        # Vérification du format CIN
        cin_pattern = r"[A-Z]{2}[0-9]{5}"
        if not re.match(cin_pattern, cin):
            error = "CIN invalide. Veuillez entrer un CIN valide."
            return render_template('add_client.html', error=error)

        # Créer un nouvel objet Client
        new_client = Client(CIN_C=cin, name=name, email=email, adresse=adresse, Tel=tel)

        # Ajouter le nouveau client à la base de données
        db.session.add(new_client)
        db.session.commit()

        # Rediriger vers la page de tableau des clients
        return redirect('/clients')

    return render_template("add_client.html")

@auth.route('/add_supplier', methods=['GET','POST'])
def add_suplier():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        matricule = request.form.get('matricule')
        name = request.form.get('name')
        email = request.form.get('email')
        adresse = request.form.get('adresse')
        tel = request.form.get('tel')

        # Créer un nouvel objet Supplier
        new_supplier = Supplier(Matricule=matricule, name=name, email=email, adresse=adresse, Tel=tel)

        # Ajouter le nouveau fournisseur à la base de données
        db.session.add(new_supplier)
        db.session.commit()

        # Rediriger vers la page de tableau des fournisseurs
        return redirect('/suppliers')
    
    return render_template("add_supplier.html")

@auth.route("add_sale", methods=['GET','POST'])
def add_sale():
    return render_template("add_vente.html")