from enums import car_category_dict, base_day_rental, kilometer_price, car_availability


def get_kilometer_diff(start_mileage, end_mileage):
    return end_mileage-start_mileage


def get_days_elapsed(end_date_time, datetime_rental):
    diff = end_date_time - datetime_rental
    return diff.days


def return_car(booking_id, end_date_time, mileage, users):
    days_elapsed = int(get_days_elapsed(end_date_time, users.datetime_rental))
    kilometer_diff = int(get_kilometer_diff(users.mileage, mileage))
    if users.car_category == car_category_dict[1]:
        price = base_day_rental*days_elapsed
    elif users.car_category == car_category_dict[2]:
        price = (base_day_rental*days_elapsed*1.2)+(kilometer_price*kilometer_diff)
    else:
        price = (base_day_rental * days_elapsed * 1.7) + (kilometer_price * kilometer_diff *1.5)
    return price


def car_is_available(car_category, booked_cars):
    total_availibility = car_availability[car_category]
    if booked_cars < total_availibility:
        return True
    return False