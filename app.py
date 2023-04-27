from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///safespace.db'
app.secret_key = 'my-secret-key'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d')

        if not email or not password or not first_name or not last_name or not date_of_birth:
            return render_template('signup.html', error='All fields are required.')

        if password != confirm_password:
            return render_template('signup.html', error='Passwords do not match')

        hashed_password = generate_password_hash(password)
        user = User(email=email, password=hashed_password, first_name=first_name, last_name=last_name, date_of_birth=date_of_birth)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid email or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/therapists')
def therapists():
    all_therapists = Therapist.query.all()
    return render_template('therapists.html', therapists=all_therapists)


@app.before_first_request
def create_tables():
    db.create_all()
    
    # Insert example therapists
    if not Therapist.query.first():
        example_therapists = [
            Therapist(name="Dr. Farida Odewale", credentials="MD, Psychiatrist", image="images/dr_farida_odewale.jpg"),
            Therapist(name="Dr. Godfred Owusu", credentials="MD, Psychiatrist", image="images/dr_godfred_owusu.jpg"),
            Therapist(name="Dr. Kwame Obeng", credentials="PhD, Psychologist", image="images/dr_kwame_obeng.jpg"),
            Therapist(name="Dr. Abena Peprah", credentials="PhD, Psychologist", image="images/dr_abena_peprah.jpg"),
            Therapist(name="Fred Ola", credentials="LCSW, Therapist", image="images/fred_ola.jpg"),
            Therapist(name="Maame Esiri", credentials="LMFT, Therapist", image="images/maame_esiri.jpg")
        ]

        for therapist in example_therapists:
            db.session.add(therapist)
        db.session.commit()


from models import User, Therapist
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)



from flask import Flask
import os

app = Flask(__name__)
print(os.path.abspath(__file__))
