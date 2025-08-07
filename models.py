from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

# This db object will be linked to the Flask app in app.py
db = SQLAlchemy()

class Land(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    area = db.Column(db.Float, nullable=False)
    soil_type = db.Column(db.String(100))
    irrigation_type = db.Column(db.String(100))

class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(15), unique=True)
    daily_wage = db.Column(db.Integer, nullable=False)
    skills = db.Column(db.Text)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='Pending')
    field_id = db.Column(db.Integer, db.ForeignKey('land.id'), nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'), nullable=True)
    
    field = db.relationship('Land', backref=db.backref('tasks', lazy=True))
    worker = db.relationship('Worker', backref=db.backref('tasks', lazy=True))

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100))
    stock = db.Column(db.Float, nullable=False, default=0)
    unit = db.Column(db.String(20))
    alert_threshold = db.Column(db.Float)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False) # 'Income' or 'Expense'
    date = db.Column(db.Date, nullable=False, default=func.now())