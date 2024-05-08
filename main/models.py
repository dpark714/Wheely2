from django.db import models

class Trip(models.Model):
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.origin} to {self.destination}"

class TripDetail(models.Model):
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)

# class User(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField(unique=True, max_length=50)
#     password = models.CharField(max_length=20)

#     class Meta:
#         db_table = 'users'


    