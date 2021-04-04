from api import app


def test_register():
    response = app.test_client().post(
        '/register',
        data='name=XYZ&booking_number=987&dob=2010-04-01&car_category%22=3&datetime_rental_date=2021-04-07&datetime_rental_time=00%3A27&mileage=300',
        content_type='text/plain',
    )
    assert response.status_code == 201
    assert b'User : XYZ Created Successfully' in response.data
    print("Tested Registering User")


def test_register_same_user_again():
    response = app.test_client().post(
        '/register',
        data='name=XYZ&booking_number=987&dob=2010-04-01&car_category%22=3&datetime_rental_date=2021-04-07&datetime_rental_time=00%3A27&mileage=300',
        content_type='text/plain',
    )
    assert response.data == b'XYZ (987) already created!'
    assert response.status_code == 200
    print("Tested Registering Same User Again")


def test_return_car():
    response = app.test_client().post(
        '/return',
        data='booking_number=987&datetime_rental_date=2021-04-21&datetime_rental_time=01%3A28&mileage=500',
        content_type='text/plain',
    )

    assert response.status_code == 200
    assert b'Car Returned Successfully' in response.data
    print("Tested Returning Car")


def test_delete_user():
    # please check the user id
    response = app.test_client().delete(
        '/register',
        data=b'{user_id:7}',
        content_type='text/plain',
    )
    assert response.status_code == 200
    assert b'User - XYZ Deleted Successfully' in response.data
    print("Tested Deleting User")


test_register()
test_register_same_user_again()
test_return_car()
test_delete_user()


#python -m unittest test.py
