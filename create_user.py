from app import app
from models import db, User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

with app.app_context():
    hashed_pw = bcrypt.generate_password_hash("admin123").decode("utf-8")
    user = User(username="admin", password=hashed_pw, role="admin")

    db.session.add(user)
    db.session.commit()
    print("Admin user created!")