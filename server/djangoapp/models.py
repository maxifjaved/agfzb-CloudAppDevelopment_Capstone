import json
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
class CarDealer:
  def __init__(self, address, city, state, full_name, id, lat, long, short_name, st, zip):
    # Dealer address
    self.address = address
    # Dealer city
    self.city = city
    # Dealer state
    self.state = state
    # Dealer Full Name
    self.full_name = full_name
    # Dealer id
    self.id = id
    # Location lat
    self.lat = lat
    # Location long
    self.long = long
    # Dealer short name
    self.short_name = short_name
    # Dealer state
    self.st = st
    # Dealer zip
    self.zip = zip
  def __str__(self):
    return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
  def __init__(self, dealership, name, purchase, review):
    # Required attributes
    self.dealership = dealership
    self.name = name
    self.purchase = purchase
    self.review = review
    # Optional attributes
    self.purchase_date = ""
    self.purchase_make = ""
    self.purchase_model = ""
    self.purchase_year = ""
    self.sentiment = ""
    self.id = ""

  def __str__(self):
    return "Review: " + self.review

  def to_json(self):
    return json.dumps(self, default=lambda o: o.__dict__,
                      sort_keys=True, indent=4)
