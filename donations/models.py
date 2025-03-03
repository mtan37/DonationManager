from datetime import datetime
from django.db import models
from django.forms import ValidationError


class DonationType(models.Model):
    name = models.CharField(max_length=30, primary_key=True)


class Donor(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=250, default="")
    email = models.EmailField(default="")


class Donation(models.Model):
    donation_type = models.ForeignKey(DonationType, on_delete=models.CASCADE)
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date = models.DateField()
    note = models.CharField(max_length=250)

    def clean(self):
        super().clean()
        if datetime.now().date() < self.date:
            raise ValidationError("Donation date can't be later than today.")


class DonationDistribution(models.Model):
    type = models.ForeignKey(DonationType, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date = models.DateField()

    def clean(self):
        super().clean()
        if datetime.now().date() < self.date:
            raise ValidationError(
                "Donation distribution date can't be later than today."
            )
