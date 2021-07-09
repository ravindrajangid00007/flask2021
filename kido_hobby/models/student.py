from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Firstname = db.Column(db.String(80), unique=True, nullable=False)
    Lastname = db.Column(db.String(80), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    avatar_path = db.Column(db.String,nullable=True)
    def __repr__(self):
        return '<User %r>' % self.email