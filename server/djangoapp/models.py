from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class CarMake(models.Model):
    """Stores car Manufacturers"""
    name = models.CharField(max_length=100)  # Name of the car make
    description = models.TextField()  # Longer text description

    def __str__(self):
        """Returns the name when model is printed/converted to string"""
        return self.name


class CarModel(models.Model):
    """Represents a specific car model"""
    car_make = models.ForeignKey(
        CarMake,
        on_delete=models.CASCADE
    )  # Foreign key to CarMake (deletes when carmake is deleted)
    name = models.CharField(max_length=100)  # Model name
    CAR_TYPES = [
        ("SEDAN", "Sedan"),
        ("SUV", "SUV"),
        ("WAGON", "Wagon"),
        ("HATCHBACK", "Hatchback"),
        ("COUPE", "Coupe"),
    ]
    type = models.CharField(
        max_length=10,
        choices=CAR_TYPES,
        default="SUV"
    )  # Limited to predefined choices with default SUV

    year = models.IntegerField(
        default=2023,
        validators=[
            MaxValueValidator(2023),
            MinValueValidator(2015),
        ],
    )  # Integer between 2015-2023 (default 2023)

    def __str__(self):
        """Returns 'Make Name Model Name' format"""
        return f"{self.car_make.name} {self.name}"
    