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
        if self.id == None:
            newUser = User(name=self.name, email=self.email, password=self.password)
        else:
            newUser = User(id=self.id, name=self.name, email=self.email, password=self.password)

        checkUser = User.query.filter(and_(User.name == self.name, User.password == self.password)).all()

        if len(checkUser) != 0:
            return -1  # USER ALREADY EXIST
        else:
            db.session.add(newUser)
            db.session.commit()

class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, nullable=False)
    reviewer_name = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)

    def addReview(self):
        newReview = Review(movie_id=self.movie_id, reviewer_name=self.reviewer_name, content=self.content, date=self.date)
        db.session.add(newReview)
        db.session.commit()

    def deleteReview(self):
        db.session.delete(self)
        db.session.commit()

