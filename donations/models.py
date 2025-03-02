from django.db import models


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


class DonationDistribution(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date = models.DateField()
