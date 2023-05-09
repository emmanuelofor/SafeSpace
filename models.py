# Importing the necessary modules
from app import db
from flask_login import UserMixin

# Creating the User model class that inherits from UserMixin and db.Model
class User(UserMixin, db.Model):
    # Defining the table columns for the User model
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)

# Creating the Therapist model class that inherits from db.Model
class Therapist(db.Model):
    # Defining the table columns for the Therapist model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    credentials = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(200), nullable=False)
    
    
