from django.db import models
from django.contrib.auth.models import User


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('COUPE', 'Coupe'),
        ('CONVERTIBLE', 'Convertible'),
        ('HATCHBACK', 'Hatchback'),
    ]
    type = models.CharField(max_length=20, choices=CAR_TYPES, default='SEDAN')
    year = models.IntegerField()

    def __str__(self):
        return f"{self.car_make.name} {self.name}"


class CarDealer(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    st = models.CharField(max_length=2)  # State abbreviation
    address = models.CharField(max_length=200)
    zip = models.CharField(max_length=10)
    lat = models.FloatField()
    long = models.FloatField()
    short_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200)

    def __str__(self):
        return self.full_name


class DealerReview(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    dealership = models.IntegerField()
    review = models.TextField()
    purchase = models.BooleanField(default=False)
    purchase_date = models.DateField(null=True, blank=True)
    car_make = models.CharField(max_length=100, null=True, blank=True)
    car_model = models.CharField(max_length=100, null=True, blank=True)
    car_year = models.IntegerField(null=True, blank=True)
    sentiment = models.CharField(max_length=20, default='neutral')
    
    def __str__(self):
        return f"Review by {self.name} for dealership {self.dealership}"