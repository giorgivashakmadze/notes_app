from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    info = request.form
    print(info)
    return render_template("login.html", text='testing')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not email or not username or not password or not confirm_password:
            flash('All fields are required', category='error')
        elif len(email) < 4 or '@' not in email:
            flash('Email is too short or does not include "@" symbol', category='error')
        elif len(username) < 2:
            flash('Username too short', category='error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters long', category='error')
        elif password != confirm_password:
            flash('Passwords do not match', category='error')
        else:
            # we have to has password here
            hashed_password = generate_password_hash(password, method='sha256')
            # create user instance and add to db
            new_user = User(email=email, username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! You can now log in.', category='success')
            return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth.route('/logout')
def logout():
    return "<h1>logout</h1>"
