from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Schedules(models.Model):

    email = models.EmailField(max_length=70, blank=True, null=True)
    source_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    source_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    destination_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    destination_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    schedule_time = models.IntegerField(db_index=True)
    install_ts = models.DateTimeField(auto_now_add=True)
    update_ts = models.DateTimeField(auto_now=True, blank=True)
    uber_arrival_time = models.IntegerField(null=True)
    travel_time = models.IntegerField(null=True)
    product_id = models.CharField(max_length=255, null=True)
    is_booked = models.BooleanField(default=False)

    class Meta:
        db_table = 'schedule_cab'
