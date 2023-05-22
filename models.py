# Importing the necessary modules
from database import db
from flask_login import UserMixin
from datetime import datetime

# Creating the User model class that inherits from UserMixin and db.Model
class User(UserMixin, db.Model):
    # Defining the table columns for the User model
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)

    def create_journal_entry(self, title, content):
        """
        Create a new journal entry associated with the user.
        Args:
            title (str): The title of the journal entry.
            content (str): The content of the journal entry.
        Returns:
            JournalEntry: The created journal entry instance.
        """
        entry = JournalEntry(user=self, title=title, content=content)
        db.session.add(entry)
        db.session.commit()
        return entry

# Creating the Therapist model class that inherits from db.Model
class Therapist(db.Model):
    # Defining the table columns for the Therapist model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    credentials = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(200), nullable=False)

# Creating the Resource model class that inherits from db.Model    
class Resource(db.Model):
    # Defining the table columns for the Resource model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    media_type = db.Column(db.String(80), nullable=False)  # "video", "article", "course"
    category = db.Column(db.String(80), nullable=False)  # "mental health", etc.

# JournalEntry model represents a journal entry in the system
class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('journal_entries', lazy=True))
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
