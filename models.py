import hashlib
import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, func


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def addUser(self):
        newUser = User(name=self.name, email=self.email, password=self.password)
        # TODO - Check if user already exists

        db.session.add(newUser)
        db.session.commit()