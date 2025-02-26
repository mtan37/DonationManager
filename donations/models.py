from django.db import models
from django.core import validators

class DonationType(models.Model):
    name = models.CharField(max_length=30)

class Donor(models.Model):
    name = models.CharField(max_length=30)

class Donation(models.Model):
    donation_type = models.ForeignKey(DonationType, on_delete=models.CASCADE)
    donor = models.ForeignKey(DonationType, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=validators.MinLengthValidator)
    date = models.DateField()
    note = models.CharField(max_length=250)

class DonationDistribution(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=validators.MinLengthValidator)
    date = models.DateField()