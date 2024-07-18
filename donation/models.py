from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Institution(models.Model):
    FUNDACJA = 'fundacja'
    ORGANIZACJA_POZARZADOWA = 'organizacja pozarządowa'
    ZBIORKA_LOKALNA = 'zbiórka lokalna'
    TYPE_CHOICES = [
        (FUNDACJA, 'Fundacja'),
        (ORGANIZACJA_POZARZADOWA, 'Organizacja Pozarządowa'),
        (ZBIORKA_LOKALNA, 'Zbiórka Lokalna'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(
        max_length=40,
        choices=TYPE_CHOICES,
        default=FUNDACJA,
    )
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

class Donation(models.Model):
    quantity = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Donation of {self.quantity} bags to {self.institution}"

class Bag(models.Model):
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} bags"
