from app import app
from models.models import db, Admin

with app.app_context():
    db.create_all()

    # Check if admin exists
    if not Admin.query.first():
        default_admin = Admin(username='admin', password='admin123')  # Change password later
        db.session.add(default_admin)
        db.session.commit()
        print("✅ Admin user created.")
    else:
        print("⚠️ Admin already exists.")
