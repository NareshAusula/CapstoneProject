from django.db import models

from django.core.validators import MaxValueValidator, MinValueValidator


# represents a car manufacture/make
class CarMake(models.Model):  # Stores car Manufacturers
    name = models.CharField(max_length=100)  # For eg name of the car
    description = models.TextField()  # For longer text Description

    def __str__(self):  # Returns the name when model is printed/converted to string
        return self.name


# Represents a specific car model
class CarModel(models.Model):
    car_make = models.ForeignKey(
        CarMake, on_delete=models.CASCADE
    )  # Forgein key to CarMake(Deletes when carmake is deleted)
    name = models.CharField(max_length=100)  # model name
    CAR_TYPES = [
        ("SEDAN", "Sedan"),
        ("SUV", "SUV"),
        ("WAGON", "Wagon"),
        ("HATCHBACK", "Hatchback"),
        ("COUPE", "Coupe"),
    ]
    type = models.CharField(
        max_length=10, choices=CAR_TYPES, default="SUV"
    )  # Limited to predefined choices (Sedan/SUV/Wagon) with default SUV
    year = models.IntegerField(
        default=2023,
        validators=[  # Integer between 2015-2023 (default 2023)
            MaxValueValidator(2023),
            MinValueValidator(2015),
        ],
    )

    def __str__(self):  # Returns "Make Name Model Name" format
        return f"{self.car_make.name}  {self.name}"
