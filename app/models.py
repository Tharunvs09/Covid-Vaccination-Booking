from app import db

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

# Define VaccinationCentre model
class VaccinationCentre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    working_hours = db.Column(db.String(100), nullable=False)
    slots = db.Column(db.Integer, nullable=False, default=10)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    centre_id = db.Column(db.Integer, db.ForeignKey('vaccination_centre.id'), nullable=False)
    centre_name = db.Column(db.String(50), nullable=False)
    working_hours = db.Column(db.String(100), nullable=False)

    # Define the relationship between Booking and User models
    user = db.relationship('User', backref=db.backref('bookings', lazy=True))
    centre = db.relationship('VaccinationCentre', backref=db.backref('bookings', lazy=True))