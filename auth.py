from unittest import result
from flask import Blueprint, render_template, request, url_for, redirect, flash
from .models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,logout_user,current_user
from . import db


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.json.get('email')
    password = request.json.get('password')
    remember = True if request.json.get('remember') else False
    user = Users.query.filter_by(email=email).first()
    resultado=''
    if not user or not check_password_hash(user.password, password):
        resultado='Please check your login details and try again.'
        
    login_user(user, remember=remember)
    resultado='User and password ok'    
    return resultado

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.json.get('email')
    password = request.json.get('password')
    confirm_password = request.json.get('coPassword')
    query = Users.query.filter_by(email=email).first()
    resultado=''
    if query is not None:
        resultado='Email address already exists'

    elif password != confirm_password:
        resultado='Wrong Password'

    else:
        new_user = Users(email = email,
                     first_name = request.form.get('firstname'),
                     last_name = request.form.get('lastname'),
                     password = generate_password_hash(password, method='sha256')
                )
        db.session.add(new_user)
        db.session.commit()
        resultado='ok'
    return resultado

@auth.route('/logout')
def logout():
    logout_user()
    respuesta= 'Logout'
    return respuesta
