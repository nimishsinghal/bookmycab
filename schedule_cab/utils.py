import requests
from django.core.mail import send_mail
from bookmycab.settings import (
    GOOGLE_ACCESS_TOKEN, UBER_ACCESS_TOKEN, GOOGLE_API_URL, UBER_API_URL
)
from schedule_cab.models import Schedules


def get_uber_time_estimate(start_latitude, start_longitude, product_id=None):
    url = UBER_API_URL + 'estimates/time'
    headers = {
        'Authorization': 'Token ' + UBER_ACCESS_TOKEN
    }
    data = {
        'start_latitude': start_latitude,
        'start_longitude': start_longitude,
        'product_id': product_id
    }
    req = requests.get(url, headers=headers, data=data)
    if req.status_code == 200:
        return req.json()['times'][0]['estimate']
    return None


def get_uber_products(start_latitude, start_longitude):
    url = UBER_API_URL + 'products'
    headers = {
        'Authorization': 'Token ' + UBER_ACCESS_TOKEN
    }
    data = {
        'latitude': start_latitude,
        'longitude': start_longitude
    }
    req = requests.get(url, headers=headers, data=data)
    if req.status_code == 200:
        return req.json()
    return None


def get_travel_estimate(start_latitude, start_longitude,
                        destination_latitude, destination_longitude):
    url = GOOGLE_API_URL + 'distancematrix/json'
    payload = {
        'key': GOOGLE_ACCESS_TOKEN,
        'origins': '{},{}'.format(start_latitude, start_longitude),
        'destinations': '{},{}'.format(destination_latitude, destination_longitude)
    }
    req = requests.get(url, params=payload)
    if req.status_code == 200:
        return req.json()['rows'][0]['elements'][0]['duration']['value']
    return None    


def check_and_book(id):
    schedule_obj = Schedules.objects.filter(id=id).first()
    schedule_obj.uber_arrival_time = get_uber_time_estimate(
            schedule_obj.source_latitude, schedule_obj.source_longitude,
            schedule_obj.product_id)
    schedule_obj.travel_time = get_travel_estimate(
        schedule_obj.source_latitude, schedule_obj.source_longitude,
        schedule_obj.destination_latitude, schedule_obj.destination_longitude)

    current_time = datetime.datetime.now().strftime('%s')
    total_travel_time = schedule_obj.uber_arrival_time + schedule_obj.travel_time

    remaining_time = (
        scheduled_obj.schedule_time - (current_time + total_travel_time)
    )/CONSTANT_FACTOR
    if remaining_time <= BOOKING_CONSTANT:
        schedule_obj.is_booked = True
        msg = 'Please leave now to reach earliest by {}'.format(
            time.strftime(
                '%H:%M:%S', time.localtime((total_travel_time + current_time))
            )
        )
        send_email_to_user(msg, schedule_obj.email)
    else:
        recheck = datetime.datetime.fromtimestamp(current_time + remaining_time)
        check_and_book.apply_async(args=schedule_obj.id, eta=recheck)
