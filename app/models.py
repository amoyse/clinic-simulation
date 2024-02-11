from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(128))

class FinancialTransactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(128))
    recipient = db.Column(db.String(128))
    amount = db.Column(db.String(128))

class Prescriptions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(128))
    doctor_name = db.Column(db.String(128))
    medicine = db.Column(db.String(128))

class HealthRecords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(128))
    date_of_birth = db.Column(db.String(128))
