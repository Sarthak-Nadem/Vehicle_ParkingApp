from models.models import db, User, Admin
from app import create_app

app = create_app()
app.app_context().push()

# Create tables
db.create_all()

# Add default admin
if not Admin.query.first():
    admin = Admin(username='admin', password='admin123')
    db.session.add(admin)
    db.session.commit()
    print("Admin created: username='admin', password='admin123'")
else:
    print("Admin already exists.")

print("Database and tables created.")
