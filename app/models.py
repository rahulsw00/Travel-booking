from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class city(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class travelOptions(models.Model):

    travelType = models.CharField(max_length=6, choices=(("TRAIN", "Train"),("FLIGHT", "Flight"),("BUS", "Bus")))
    source = models.ForeignKey(city, related_name='departure', on_delete=models.CASCADE)
    destination = models.ForeignKey(city, related_name='arrival', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    dateTime = models.DateTimeField()
    availableSeats = models.IntegerField()

    def __str__(self):
        return f"{self.source} to {self.destination} via {self.travelType}"


class booking(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    travelOption = models.ForeignKey(travelOptions, on_delete=models.CASCADE)
    numberOfSeats = models.IntegerField()
    totalPrice = models.DecimalField(max_digits=10, decimal_places=2)
    bookingDate = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=9, choices=(("CONFIRMED", "Confirmed"), ("CANCELLED", "Cancelled")))