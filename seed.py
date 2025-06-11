from app import create_app
from app.models import db, Role, User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # db.create_all()  # HAPUS atau KOMENTARI baris ini

    # Seed Role
    if not Role.query.filter_by(name='admin').first():
        admin_role = Role(name='admin')
        user_role = Role(name='user')
        db.session.add(admin_role)
        db.session.add(user_role)
        db.session.commit()

    # Seed Admin User
    if not User.query.filter_by(email='admin@example.com').first():
        admin = User(
            email='admin@example.com',
            password=generate_password_hash('admin123'),
            role_id=Role.query.filter_by(name='admin').first().id
        )
        db.session.add(admin)
        db.session.commit()

    print("✅ Seed berhasil!")
