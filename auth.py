import sqlite3
from flask import Blueprint, render_template, request, redirect
from werkzeug.security import check_password_hash
import re


DB_NAME = "database.db"

auth = Blueprint('auth', __name__)

@auth.route('', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        CIN = request.form.get('CIN')
        password = request.form.get('password')

        # Verification of CIN pattern
        cin_pattern = r"[A-Z]{2}[0-9]{5}"
        if not re.match(cin_pattern, CIN):
            error = "Invalid CIN. Please enter a valid CIN."
            return render_template('login.html', error=error)

        # Verification of user in the database
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        c.execute("SELECT * FROM user WHERE CIN = ?", (CIN,))
        user = c.fetchone()

        # Redirect based on user type
        if user[5] == 'ADMIN':
            return redirect("/menu_1")
        elif user[5] == 'EMP_VENTES':
            return redirect('/menu_2')
        elif user[5] == 'EMP_APPS':
            return redirect('/menu_3')

        conn.close()

        if not user or not check_password_hash(user[4], password):
            error = "Incorrect CIN or password."
            return render_template('login.html', error=error)

        
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<p>logout</p>"

@auth.route('/add_user', methods=['GET','POST'])
def add_user():
    if request.method == 'POST':
        CIN = request.form.get('CIN')
        first_name = request.form.get('Fname')
        last_name = request.form.get('Lname')
        email = request.form.get('email')
        password = request.form.get('password1')
        role = request.form.get('role')

        # Verification of CIN pattern
        cin_pattern = r"[A-Z]{2}[0-9]{5}"
        if not re.match(cin_pattern, CIN):
            error = "Invalid CIN. Please enter a valid CIN."
            return render_template('add_client.html', error=error)

        # Check the value of 'role' and assign corresponding value to 'type_u'
        if role == 'option1':
            type_u = 'ADMIN'
        elif role == 'option2':
            type_u = 'EMP_VENTES'
        elif role == 'option3':
            type_u = 'EMP_APPS'
        else:
            return 'Error: No role selected'

        # Connect to the database
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        # Insert a new user
        c.execute("INSERT INTO user (CIN, Fname, Lname, email, password, type_u) VALUES (?, ?, ?, ?, ?, ?)",
                  (CIN, first_name, last_name, email, password, type_u))

        conn.commit()
        conn.close()

        return redirect("/user")

    return render_template("add_user.html")

@auth.route('/add_client', methods=['GET','POST'])
def add_client():
    if request.method == 'POST':
        cin = request.form.get('CIN')
        fname = request.form.get('Fname')
        lname = request.form.get ('Lname')
        email = request.form.get('email')
        adresse = request.form.get('adresse')
        tel = request.form.get('telephone')

        cin_pattern = r"[A-Z]{2}[0-9]{5}"
        if not re.match(cin_pattern, cin):
            error = "Invalid CIN. Please enter a valid CIN."
            return render_template('add_client.html', error=error)

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        c.execute("INSERT INTO client (CIN_C, Fname_c, Lname_c, email, adresse, Tel) VALUES (?, ?, ?, ?, ?, ?)",
          (cin, fname, lname, email, adresse, tel))


        conn.commit()
        conn.close()

        return redirect('/client')

    return render_template("add_client.html")

@auth.route('/add_supplier', methods=['GET','POST'])
def add_supplier():
    if request.method == 'POST':
        matricule = request.form.get('matricule')
        name = request.form.get('name')
        email = request.form.get('email')
        adresse = request.form.get('adresse')
        tel = request.form.get('tel')

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        c.execute("INSERT INTO supplier (Matricule, name, email, adresse, Tel) VALUES (?, ?, ?, ?, ?)",
                  (matricule, name, email, adresse, tel))

        conn.commit()
        conn.close()

        return redirect('/supplier')

    return render_template("add_supplier.html")

@auth.route("/add_sale", methods=['GET', 'POST'])
def add_sale():
    if request.method == 'POST':
        id_v = request.form.get('id_v')
        date_vente = request.form.get('date')
        montant_v = request.form.get('montant')
        CIN_C = request.form.get('CIN')
        code_p = request.form.get('id_p')
        qte_v = request.form.get('qte')

        cin_pattern = r"[A-Z]{2}[0-9]{5}"
        if not re.match(cin_pattern, CIN_C):
            error = "Invalid CIN. Please enter a valid CIN."
            return render_template('add_client.html', error=error)

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        # Vérification de l'existence du client_id dans la table client
        c.execute("SELECT * FROM Client WHERE client_id = ?", (CIN_C,))
        client = c.fetchone()
        if not client:
            error = "Invalid client_id. Please enter a valid client_id."
            return render_template('add_vente.html', error=error)

        # Vérification de l'existence du code_p dans la table produits
        c.execute("SELECT * FROM Produits WHERE code_p = ?", (code_p,))
        produit = c.fetchone()
        if not produit:
            error = "Invalid product code. Please enter a valid product code."
            return render_template('add_vente.html', error=error)

        # Vérification de la disponibilité de la quantité de vente dans la table produits
        c.execute("SELECT QTE FROM Produits WHERE code_p = ?", (code_p,))
        qte_dispo = c.fetchone()
        if not qte_dispo or int(qte_dispo[0]) < int(qte_v):
            error = "Insufficient quantity available for sale."
            return render_template('add_vente.html', error=error)

        # Mise à jour de la quantité dans la table produits
        nouvelle_qte = int(qte_dispo[0]) - int(qte_v)
        c.execute("UPDATE Produits SET QTE = ? WHERE code_p = ?", (nouvelle_qte, code_p))

        # Insertion de la vente dans la table Shipment
        c.execute("INSERT INTO Shipment (id, date, Montant, client_id, Code_p, qte_vente) VALUES (?, ?, ?, ?, ?, ?)",
                  (id_v, date_vente, montant_v, CIN_C, code_p, qte_v))

        conn.commit()
        conn.close()

    return render_template("add_vente.html")



@auth.route("/add_app", methods=['GET','POST'])
def add_app():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        app_id = request.form.get('id_app')
        date_app = request.form.get('date')
        montant_app = request.form.get('Montant_A')
        matricule_fournisseur = request.form.get('matricule')
        code = request.form.get('id_c')
        qte_app = request.form.get('qte')

        # Valider les données (vous pouvez ajouter vos propres validations ici)

        # Vérifier si le matricule_fournisseur existe dans la table fournisseur
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM supplier WHERE Matricule = ?", (matricule_fournisseur,))
        fournisseur_exist = c.fetchone() is not None
        conn.close()

        if not fournisseur_exist:
            # Afficher un message d'erreur ou effectuer une action appropriée
            return "Le fournisseur spécifié n'existe pas."

        # Insérer les données dans la table Shipment
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO shipment (id, date, Montant, supplier_id, Code_p, Qte_app) VALUES (?, ?, ?, ?, ?, ?)",
                  (app_id, date_app, montant_app, matricule_fournisseur, code, qte_app))
        conn.commit()
        conn.close()

        # Rediriger vers le route /shipment
        return redirect('/shipment')
    
    # Rendre le template du formulaire avec la liste des produits
    return render_template("add_app.html")


@auth.route("/add_product", methods=['GET','POST'])
def add_product():
    if request.method == 'POST':
        code = request.form.get('id_c')
        libelle = request.form.get('Libelle')
        qte = request.form.get('qte')
        pu_a = request.form.get('PU_A')
        pu_v = request.form.get('PU_V')
        supplier_id = request.form.get('matricule')

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        # Vérification de l'existence du supplier_id dans la table supplier
        c.execute("SELECT Matricule FROM supplier WHERE Matricule = ?", (supplier_id,))
        supplier = c.fetchone()

        if supplier:
            c.execute("INSERT INTO product (Code, Libelle, QTE, PU_A, PU_V) VALUES (?, ?, ?, ?, ?)",
                      (code, libelle, qte, pu_a, pu_v))
            conn.commit()
            conn.close()

            return redirect('/product')
        else:
            error = "Le supplier_id n'existe pas."
            return render_template('add_products.html', error=error)
    return render_template("add_products.html")


@auth.route('/menu_1')
def menu_1():
    return render_template('menu_1.html')

@auth.route('/menu_2')
def menu_2():
    return render_template('menu_2.html')

@auth.route('/menu_3')
def menu_3():
    return render_template('menu_3.html')


@auth.route('/user')
def Users():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user")
    data = cursor.fetchall()
    conn.close()
    return render_template('user.html', users=data)

@auth.route('/supplier')
def Suppliers():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM supplier")
    data = cursor.fetchall()
    conn.close()
    return render_template('supplier.html', suppliers=data)

@auth.route('/client')
def Clients():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM client")
    data = cursor.fetchall()
    conn.close()
    return render_template('client.html', clients=data)

@auth.route('/product')
def Products():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM product")
    data = cursor.fetchall()
    conn.close()
    return render_template('product.html', products=data)

@auth.route('/shipment')
def Shipments():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shipment")
    data = cursor.fetchall()
    conn.close()
    return render_template('shipment.html', shipments=data)

@auth.route('/sale')
def Sales():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sale")
    data = cursor.fetchall()
    conn.close()
    return render_template('sale.html', sales=data)



