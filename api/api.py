from __future__ import absolute_import
from flask import request, render_template, make_response
from flask_restful import Resource, abort
import datetime
from models import UserModel, db
from config import api, app
import os
from enums import car_category_dict
from utils import return_car, car_is_available


def get_booked_car_category(car_category):
    print("In get_booked_car_category")
    count = UserModel.query.filter(UserModel.car_category == car_category).count()
    print("count :"+str(count))
    return (count)


def abort_if_booking_number_doesnt_exists(booking_id):
    users = UserModel.query.filter(UserModel.booking_number == booking_id).first()
    if not users:
        abort("Booking Id is not valid...")
    else:
        return users.id


def abort_if_user_doesnt_exist(user_id):
    user = UserModel.query.filter(UserModel.id == user_id).first()
    if user:
        return user.name
    else:
        abort("User Id is not valid...")


class Home(Resource):
    def get(self):
        return make_response(render_template('home.html', users=UserModel.query.all()))


class Register(Resource):

    def post(self):
        data = request.get_data()
        my_json = data.decode('utf8').replace("'", '"').split("&")
        name = my_json[0].split("=")[1].replace("+"," ")
        booking_number = my_json[1].split("=")[1]
        dob = my_json[2].split("=")[1]
        car_category_key = my_json[3].split("=")[1]
        date = my_json[4].split("=")[1]
        time = my_json[5].split("=")[1].replace("%3A", ":")
        mileage = int(my_json[6].split("=")[1])

        existing_user = UserModel.query.filter(
            UserModel.booking_number == booking_number and (UserModel.name == name and UserModel.dob == dob)).first()
        if existing_user:
            return make_response(f'Hi {name} There is already a user with your details!')
        dob = datetime.datetime.strptime(dob, '%Y-%m-%d')
        datetime_rental = date + " " + time
        datetime_rental = datetime.datetime.strptime(datetime_rental, '%Y-%m-%d %H:%M')
        car_category = car_category_dict[int(car_category_key)]
        count = get_booked_car_category(car_category)
        if car_is_available(car_category, count):
            user = UserModel(
                name=name,
                booking_number=booking_number,
                dob=dob,
                car_category=car_category,
                datetime_rental=datetime_rental,
                mileage=mileage
            )
            db.session.add(user)
            db.session.commit()
            return make_response(render_template('success_register.html', name=name, booking_number=booking_number,
                                                 users=UserModel.query.all()), 201)
        else:
            return make_response(f'Hi {name}... Please Select Another Car Category... Category {car_category}is Full!')

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('register.html'), 200, headers)

    def delete(self):
        user_id = request.data.decode('utf-8').split(":")[1].rstrip("}")
        name = abort_if_user_doesnt_exist(user_id)
        user = UserModel.query.filter(UserModel.id == user_id).first()
        db.session.delete(user)
        db.session.commit()
        return make_response(render_template('user_deleted.html', name=name, users=UserModel.query.all()))


class Return(Resource):
    def post(self):
        data = request.get_data()
        my_json = data.decode('utf8').replace("'", '"').split("&")
        booking_id = my_json[0].split("=")[1]
        date = my_json[1].split("=")[1]
        time = my_json[2].split("=")[1].replace("%3A", ":")
        mileage = int(my_json[3].split("=")[1])
        user_id = abort_if_booking_number_doesnt_exists(booking_id)
        datetime_end_rental = (date + " " + time)
        end_date_time = datetime.datetime.strptime(datetime_end_rental, '%Y-%m-%d %H:%M')
        users = UserModel.query.filter(UserModel.booking_number == booking_id).first()
        price = return_car(booking_id, end_date_time, mileage, users)
        return make_response(render_template('return_car.html', booking_id=booking_id, price=price, user_id=user_id,
                                             users=UserModel.query.all()))

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('return.html'), 200, headers)


api.add_resource(Home, '/')
api.add_resource(Register, '/register')
api.add_resource(Return, '/return')


if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        #db.create_all()
        pass
    app.run(debug=True)
