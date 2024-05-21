from django.db import models

from django.contrib.auth.models import User

# class Trip(models.Model):
#     origin = models.CharField(max_length=255)
#     destination = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.origin} to {self.destination}"

# class TripDetail(models.Model):
#     origin = models.CharField(max_length=255)
#     destination = models.CharField(max_length=255)

# class User(models.Model):
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     email = models.EmailField(unique=True, max_length=50)
#     password = models.CharField(max_length=20)

#     class Meta:
#         db_table = 'users'

class StationInfo(models.Model):
    start_station = models.CharField(max_length=255)
    end_station = models.CharField(max_length=255)
    transfer_stations = models.JSONField(default=list)
    bus_stations = models.JSONField(default=list)


# class AccessibilityStation(models.Model):
#     station_name = models.CharField(max_length=100)
#     accessible = models.BooleanField(default=True)

#     def __str__(self):
#         return f"{self.station_name} ({'Accessible' if self.accessible else 'Not accessible'})"
    

class AccessibleStation(models.Model):
    # Define fields based on the structure of Accessible_MTA_Stations.xlsx
    station_name = models.CharField(max_length=255)
    line = models.CharField(max_length=255)

class AllStation(models.Model):
    # Define fields based on the structure of All Station.csv
    station_id = models.CharField(max_length=255)
    station_name = models.CharField(max_length=255)
    line = models.CharField(max_length=255)

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    search_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.origin} to {self.destination}"


    