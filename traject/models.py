from djongo import models
from django.db.models import Sum
from datetime import timedelta
from django.utils import timezone

class Trip(models.Model):
    current_location = models.CharField(max_length=255)  # Current location of the driver
    pickup_location = models.CharField(max_length=255)  # Location where the load is picked up
    dropoff_location = models.CharField(max_length=255)  # Location where the load is dropped off
    current_cycle = models.IntegerField()  # Current driving cycle (e.g., 1, 2, etc.)
    distance_traveled = models.FloatField(default=0)  # Distance traveled in miles

    def __str__(self):
        return f"Trip from {self.current_location} to {self.dropoff_location}"

class ELDLog(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)  # Associated trip
    start_time = models.DateTimeField()  # Start time of the log
    end_time = models.DateTimeField(null=True, blank=True)  # End time of the log
    driving_hours = models.FloatField(default=0)  # Total driving hours
    sleep_start = models.DateTimeField(null=True, blank=True)  # Start time of sleep
    sleep_end = models.DateTimeField(null=True, blank=True)  # End time of sleep
    sleep_duration = models.FloatField(default=0)  # Total sleep duration in hours
    onduty_start = models.DateTimeField(null=True, blank=True)  # Start time of on-duty
    onduty_end = models.DateTimeField(null=True, blank=True)  # End time of on-duty
    onduty_duration = models.FloatField(default=0)  # Total on-duty duration in hours
    offduty_start = models.DateTimeField(null=True, blank=True)  # Start time of off-duty
    offduty_end = models.DateTimeField(null=True, blank=True)  # End time of off-duty
    offduty_duration = models.FloatField(default=0)  # Total off-duty duration in hours

    def __str__(self):
        return f"ELD Log for {self.trip}"