from flask import Flask

from kido_hobby.models.student import db
from kido_hobby.student import api
from flask_sqlalchemy import SQLAlchemy
UPLOAD_FOLDER = '/uploads/users/avatars'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
    with app.app_context():
        db.init_app(app)
        db.create_all()
        api.init_app(app)

    return app