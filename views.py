from flask import Blueprint, render_template
from .models import User , UserMixin

views = Blueprint('views',__name__)
