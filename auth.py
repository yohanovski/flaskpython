import sqlite3
from flask import Blueprint, render_template, request, redirect
from werkzeug.security import check_password_hash
import re


DB_NAME = "database.db"

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
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

        return redirect("login.html")

    return render_template("add_user.html")

@auth.route('/add_client', methods=['GET','POST'])
def add_client():
    if request.method == 'POST':
        cin = request.form.get('cin')
        name = request.form.get('name')
        email = request.form.get('email')
        adresse = request.form.get('adresse')
        tel = request.form.get('tel')

        cin_pattern = r"[A-Z]{2}[0-9]{5}"
        if not re.match(cin_pattern, cin):
            error = "Invalid CIN. Please enter a valid CIN."
            return render_template('add_client.html', error=error)

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        c.execute("INSERT INTO client (CIN_C, name, email, adresse, Tel) VALUES (?, ?, ?, ?, ?)",
                  (cin, name, email, adresse, tel))

        conn.commit()
        conn.close()

        return redirect('login.html')

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

        return redirect('/suppliers')

    return render_template("add_supplier.html")

@auth.route("add_sale", methods=['GET','POST'])
def add_sale():
    return render_template("add_vente.html")

@auth.route('/menu_1')
def menu_1():
    return render_template('menu_1.html')

@auth.route('/menu_2')
def menu_2():
    return render_template('menu_2.html')

@auth.route('/menu_3')
def menu_3():
    return render_template('menu_3.html')

