from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required,logout_user,current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Login successful!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.index'))  # Redirect to a dashboard page
            else:
                flash('Incorrect password. Please try again.', category='error')
        else:
            flash('User not found. Please check your email.', category='error')

    return render_template("login.html", user=current_user )


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # check if user is already  in db
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('email already used')
            return redirect(url_for('auth.login'))

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
            new_user = User.create(email=email, username=username, password=password)

            flash('Registration successful! You can now log in.', category='success')
            return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
