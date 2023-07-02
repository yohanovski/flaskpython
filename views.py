from flask import Blueprint, render_template
from flask_login import login_required, current_user


views = Blueprint('views',__name__)
@views.route('/menu_1.html')
@login_required
def menu_1():
    return render_template("menu_1.html")