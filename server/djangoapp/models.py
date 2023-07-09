from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return "Name: " + str(self.name) + "," + \
                "Description: " + str(self.description)

class CarModel(models.Model):
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    CAR_TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
    ]

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dealer_id = models.IntegerField()
    type = models.CharField(
        max_length=5,
        choices=CAR_TYPE_CHOICES,
        default=SEDAN,
    )
    year = models.DateField(default=now)

    def __str__(self):
        return "Name: " + str(self.name) + "," + \
                "Dealer ID: " + str(self.dealer_id) + "," + \
                "Type: " + str(self.type) + "," + \
                "Year: " + str(self.year)


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
