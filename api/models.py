from config import db


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_number = db.Column(db.String(100), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    car_category = db.Column(db.String, nullable=False)
    datetime_rental = db.Column(db.DateTime, nullable=False)
    mileage = db.Column(db.Integer, nullable=False)

    def __init__(self, name, booking_number, dob, car_category, datetime_rental, mileage):
        self.name = name
        self.booking_number = booking_number
        self.dob = dob
        self.car_category = car_category
        self.datetime_rental = datetime_rental
        self.mileage = mileage

    def __repr__(self):
        return '<User %r %r>' % (self.name, self.booking_number)