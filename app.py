# Importing necessary modules
from flask import Flask, render_template, request, redirect, url_for, abort
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import Configuration
from database import db

# Setting up the Flask application
app = Flask(__name__)
app.config.from_object(Configuration) # Database URI
db.init_app(app)    # Initializing the SQLAlchemy database instance

#Importing the User and Therapist models
from models import User, Therapist, Resource, JournalEntry

# Setting up the login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Defining the user loader callback for the login manager
#@login_manager.user_loader
#def load_user(user_id):
#    return User.query.get(int(user_id))

# Defining routes and associated view functions for the application
@app.route('/')
def index():
    # If the user is authenticated, render the homepage with user information
    if current_user.is_authenticated:
        return render_template('homepage.html', current_user=current_user)
    # If not authenticated, render the index page    
    else:
        return render_template('index.html', current_user=current_user)
    

@app.route('/homepage')
@login_required
def homepage():
    # Render the homepage with user information 
    first_name = current_user.first_name
    return render_template('homepage.html', current_user=current_user, first_name=first_name)


@app.route('/journal')
@login_required
def journal():
    # Fetch journal entries for the logged-in user from the database
    journal_entries = current_user.journal_entries

    # Render the journal listing page with the journal entries
    return render_template('journal.html', journal_entries=journal_entries)

@app.route('/journal/entry/<int:entry_id>')
@login_required
def journal_entry(entry_id):
    # Fetch the specific journal entry from the database
    journal_entry = JournalEntry.query.get(entry_id)

    # Render the journal entry page with the journal entry details
    return render_template('journal_entry.html', journal_entry=journal_entry)

@app.route('/journal/new', methods=['GET', 'POST'])
@login_required
def new_journal_entry():
    # Handling POST request for creating a new journal entry
    if request.method == 'POST':
        # Extracting journal entry input from the form
        title = request.form['title']
        content = request.form['content']

        # Validating input and rendering error messages if necessary
        if not title or not content:
            return render_template('new_journal_entry.html', error='All fields are required.')

        # Create a new journal entry and associate it with the current user
        journal_entry = current_user.create_journal_entry(title, content)

        # Indicate successful creation and redirect to the journal entry details page
        return redirect(url_for('journal_entry', entry_id=journal_entry.id))
    
    # If it's a GET request, render the new journal entry page
    return render_template('new_journal_entry.html')

@app.route('/journal/entry/<int:entry_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_journal_entry(entry_id):
    # Fetch the specific journal entry from the database
    journal_entry = JournalEntry.query.get(entry_id)

    # Check if the current user is the owner of the journal entry
    if journal_entry.user != current_user:
        abort(403)  # Forbidden

    # Handle POST request for editing a journal entry
    if request.method == 'POST':
        # Extract new journal entry input from the form
        title = request.form['title']
        content = request.form['content']

        # Validate input and render error messages if necessary
        if not title or not content:
            return render_template('edit_journal_entry.html', error='All fields are required.', journal_entry=journal_entry)

        # Update the journal entry and commit the changes to the database
        journal_entry.title = title
        journal_entry.content = content
        db.session.commit()

        # Indicate successful edit and redirect to the journal entry details page
        return redirect(url_for('journal_entry', entry_id=journal_entry.id))

    # If it's a GET request, render the journal entry edit page
    return render_template('edit_journal_entry.html', journal_entry=journal_entry)

@app.route('/journal/entry/<int:entry_id>/delete', methods=['POST'])
@login_required
def delete_journal_entry(entry_id):
    # Fetch the specific journal entry from the database
    journal_entry = JournalEntry.query.get(entry_id)

    # Check if the current user is the owner of the journal entry
    if journal_entry.user != current_user:
        abort(403)  # Forbidden

    # Delete the journal entry and commit the changes to the database
    db.session.delete(journal_entry)
    db.session.commit()

    # Indicate successful deletion and redirect to the journal entries list page
    return redirect(url_for('journal'))



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Handling POST request for user signup
    if request.method == 'POST':
        # Extracting user input from the form
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        first_name = request.form['full_name']
        last_name = request.form['last_name']
        date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d')

        # Validating input and rendering error messages if necessary
        if not email or not password or not first_name or not last_name or not date_of_birth:
            return render_template('signup.html', error='All fields are required.')

        if password != confirm_password:
            return render_template('signup.html', error='Passwords do not match')

        # Check if email already exists in the database
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template('signup.html', error='Email already exists')

        # Hashing password and creating user instance
        hashed_password = generate_password_hash(password)
        user = User(email=email, password=hashed_password, first_name=first_name, last_name=last_name, date_of_birth=date_of_birth)

        # Adding user to the database
        db.session.add(user)
        db.session.commit()

        # Indicate successful sign-up and prompt to log in
        return render_template('login.html', message='Sign up successful! Please log in.')
    
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Handling POST request for user login
    if request.method == 'POST':
        # Extracting user input from the form
        email = request.form['email']
        password = request.form['password']

        # Querying user from the database
        user = User.query.filter_by(email=email).first()

        # Authenticating user and logging them in if valid
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('homepage'))  # Redirects to the homepage
        else:
            return render_template('login.html', error='Invalid email or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    # Logging out the user and redirecting to the index page
    logout_user()
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/team')
def team():
    return render_template('about_team.htm')


    

@app.route('/therapists')
def therapists():
    # Render the therapists page
    return render_template('therapists.html')

@app.route('/therapist2')
def therapist2():
    # Querying all therapists from the database
    therapists_list = Therapist.query.all()
    # Rendering the therapist2 page with the therapists list
    return render_template('therapist2.html', therapists=therapists_list)

@app.route('/resources', methods=['GET'])
def resources():
    resource = Resource.query.with_entities(Resource.name, Resource.link, Resource.media_type, Resource.category).all()
    return render_template('resources.html', resource=resource)

# Defining routes for about team page
@app.route('/about_team', methods=['GET'])
def about_team():
    return render_template('about_team.html')

# Defining routes for contact us page
@app.route('/contact_us', methods=['GET'])
def contact_us():
    return render_template('contact_us.html')

# Defining the user loader callback for the login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define example therapists and resources
example_therapists = [
    Therapist(name="Dr. Farida Odewale", credentials="MD, Psychiatrist", image="images/dr_godfred_owusu.jpg"),
    Therapist(name="Dr. Godfred Owusu", credentials="MD, Psychiatrist", image="images/dr_farida_odewale.jpg"),
    Therapist(name="Dr. Kwame Obeng", credentials="PhD, Psychologist", image="images/fred_ola.jpg"),
    Therapist(name="Dr. Abena Peprah", credentials="PhD, Psychologist", image="images/dr_abena_peprah.jpg"),
    Therapist(name="Fred Richards", credentials="LCSW, Therapist", image="images/dr_kwame_obeng.jpg"),
    Therapist(name="Maame Esiri", credentials="LMFT, Therapist", image="images/maame_esiri.jpg")
]

example_resources = [
    Resource(
        name='Understanding Anxiety',
        link='https://www.healthline.com/health/anxiety',
        media_type='article',
        category='mental health'
    ),
    Resource(
        name='How Stress Affects Your Brain',
        link='https://www.youtube.com/watch?v=WuyPuH9ojCE',
        media_type='video',
        category='mental health'
    ),
    Resource(
        name='The Social Context of Mental Health and Illness',
        link='https://www.coursera.org/learn/mental-health',
        media_type='Online Course',
        category='mental health'
    )
]

with app.app_context():
    db.create_all()

    # Insert example therapists if none exist yet
    if not Therapist.query.first():
        for therapist in example_therapists:
            db.session.add(therapist)

    # Insert example resources if none exist yet
    if not Resource.query.first():
        for resource in example_resources:
            db.session.add(resource)

    db.session.commit()



#Running the application with debug mode enabled
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)



