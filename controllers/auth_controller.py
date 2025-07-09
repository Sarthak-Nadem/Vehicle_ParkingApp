from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, LoginManager
from models.models import db, User, Admin

auth_bp = Blueprint('auth', __name__)
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    if user_id.startswith("admin_"):
        return Admin.query.get(int(user_id[6:]))
    return User.query.get(int(user_id))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check user
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('user.dashboard'))

        flash('Invalid credentials', 'danger')
    return render_template('login.html')


@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.password == password:
            # Manually prefix ID to identify admin in login manager
            admin.id = f"admin_{admin.id}"
            login_user(admin)
            return redirect(url_for('admin.dashboard'))

        flash('Invalid admin login', 'danger')
    return render_template('admin_login.html')


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
