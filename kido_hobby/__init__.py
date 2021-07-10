from flask import Flask

from .models.student_model import db
from flask_sqlalchemy import SQLAlchemy
from .controllers.student_controller import student_route
from .config.flask_jwt import jwt
UPLOAD_FOLDER = '/uploads/users/avatars'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
    app.config["JWT_SECRET_KEY"] = "super-secret"
    with app.app_context():
        db.init_app(app)
        db.create_all()
        jwt.init_app(app)
    app.register_blueprint(student_route)
    return app