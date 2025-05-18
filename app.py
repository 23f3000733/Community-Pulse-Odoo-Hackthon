from flask import Flask, render_template, request, redirect, url_for, flash
from extensions import db, login_manager
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import User, Event

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///community_pulse.db'

# Init extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

 # make sure User model is in models.py

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ------------------- REGISTER -------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered.", "danger")
            return redirect(url_for('register'))

        hashed_pw = generate_password_hash(password)
        new_user = User(name=name, email=email, phone=phone, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')


# ------------------- LOGIN -------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("Invalid email or password.", "danger")
            return redirect(url_for('login'))

        if user.is_banned:
            flash("Your account has been banned.", "warning")
            return redirect(url_for('login'))

        login_user(user)
        flash("Logged in successfully.", "success")
        return redirect(url_for('home'))

    return render_template('login.html')


# ------------------- LOGOUT -------------------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for('home'))


# ------------------- HOME -------------------
@app.route('/')
def home():
    return "Hello, Community Pulse!"

# Run Server
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
