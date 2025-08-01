from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, LoginManager
from models.models import db, User, Admin

auth_bp = Blueprint('auth', __name__)
login_manager = LoginManager()


# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    if user_id.startswith("admin_"):
        return Admin.query.get(int(user_id[6:]))
    return User.query.get(int(user_id))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        if not email or not password:
            flash("Email and password required", "danger")
            return redirect(url_for('auth.login'))

        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('user.dashboard'))

        flash("Invalid user credentials", "danger")

    return render_template('login.html')


@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        if not username or not password:
            flash("Username and password required", "danger")
            return redirect(url_for('auth.admin_login'))

        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.password == password:
            admin.id = f"admin_{admin.id}"
            login_user(admin)
            return redirect(url_for('admin.dashboard'))

        flash("Invalid admin credentials", "danger")

    return render_template('admin_login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        full_name = request.form['full_name'].strip()

        if not email or not password or not full_name:
            flash("All fields are required", "danger")
            return redirect(url_for('auth.register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("User already exists", "warning")
            return redirect(url_for('auth.register'))

        new_user = User(email=email, password=password, full_name=full_name)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
