from rest_framework import serializers
from schedule_cab.models import Schedules
from schedule_cab.utils import (
    get_uber_time_estimate, get_travel_estimate,
)
from schedule_cab.tasks import check_and_book
from django.core.mail import send_mail
from schedule_cab.constants import CONSTANT_FACTOR, BOOKING_CONSTANT
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
import time
import datetime


class SchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedules
        fields = ('email', 'source_latitude', 'source_longitude',
                  'destination_latitude', 'destination_longitude',
                  'schedule_time', 'uber_arrival_time', 'travel_time',
                  'product_id', 'is_booked',)

    def create(self, validated_data):
        schedule_obj = Schedules.objects.create(**validated_data)
        redis_publisher = RedisPublisher(facility='alerts', broadcast=True)
        schedule_obj.uber_arrival_time = get_uber_time_estimate(
            schedule_obj.source_latitude, schedule_obj.source_longitude,
            schedule_obj.product_id)
        message = RedisMessage('{} Requested uber api for {}'.format(
            datetime.datetime.now().strftime('%H:%M:%S'),
            schedule_obj.email
        ))
        redis_publisher.publish_message(message)
        schedule_obj.travel_time = get_travel_estimate(
            schedule_obj.source_latitude, schedule_obj.source_longitude,
            schedule_obj.destination_latitude, schedule_obj.destination_longitude)
        message = RedisMessage('{} Requested map api for {}'.format(
            datetime.datetime.now().strftime('%H:%M:%S'),
            schedule_obj.email
        ))
        redis_publisher.publish_message(message)

        current_time = int(datetime.datetime.now().strftime('%s'))
        total_travel_time = schedule_obj.uber_arrival_time + schedule_obj.travel_time
        remaining_time = (
            schedule_obj.schedule_time - (current_time + total_travel_time)
        )
        if remaining_time <= BOOKING_CONSTANT:
            schedule_obj.is_booked = True
            msg = """Hi, You booked a cab with us for {}.
            Please leave now to reach earliest by {}""".format(
                time.strftime(
                    '%H:%M:%S', time.localtime(schedule_obj.schedule_time)
                ),
                time.strftime(
                    '%H:%M:%S', time.localtime((total_travel_time + current_time))
                )
            )
            send_mail('Book your uber', msg, 'nimishsinghal188@gmail.com',
                      [schedule_obj.email], fail_silently=False)
        else:
            check_and_book.apply_async(args=(schedule_obj.id,), countdown=remaining_time/CONSTANT_FACTOR)
        schedule_obj.save()
        return schedule_obj
