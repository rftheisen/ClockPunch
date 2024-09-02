from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clockin.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_manager = db.Column(db.Boolean, default=False)

class TimeRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    clock_in = db.Column(db.DateTime, nullable=False)
    clock_out = db.Column(db.DateTime)

def create_test_user(username, password, is_manager=False):
    with app.app_context():
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"User '{username}' already exists.")
            return

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, is_manager=is_manager)
        db.session.add(new_user)
        db.session.commit()
        print(f"User '{username}' created successfully.")

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    if user.is_manager:
        records = TimeRecord.query.all()
    else:
        records = TimeRecord.query.filter_by(user_id=user.id).all()
    return render_template('dashboard.html', user=user, records=records)

@app.route('/clock_in', methods=['POST'])
def clock_in():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    last_record = TimeRecord.query.filter_by(user_id=user_id).order_by(TimeRecord.id.desc()).first()
    if last_record and not last_record.clock_out:
        flash('You are already clocked in')
    else:
        new_record = TimeRecord(user_id=user_id, clock_in=datetime.now())
        db.session.add(new_record)
        db.session.commit()
        flash('Clocked in successfully')
    return redirect(url_for('dashboard'))

@app.route('/clock_out', methods=['POST'])
def clock_out():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    last_record = TimeRecord.query.filter_by(user_id=user_id).order_by(TimeRecord.id.desc()).first()
    if last_record and not last_record.clock_out:
        last_record.clock_out = datetime.now()
        db.session.commit()
        flash('Clocked out successfully')
    else:
        flash('You are not clocked in')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create a test user and a test manager
        create_test_user('employee', 'employee123', is_manager=False)
        create_test_user('manager', 'manager123', is_manager=True)
    app.run(debug=True)
