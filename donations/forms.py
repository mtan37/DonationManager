from datetime import datetime
from django import forms

from donations.models import Donation, DonationDistribution


def get_inventory(type_name: str, date: datetime.date):
    inventory = 0
    for donation in Donation.objects.filter(
        donation_type__name=type_name,
        date__lte=date,
    ):
        inventory += donation.quantity
    for distribution in DonationDistribution.objects.filter(
        type__name=type_name,
        date__lte=date,
    ):
        inventory -= distribution.quantity

    return inventory


class DonationDistributionCreateForm(forms.ModelForm):
    """
    Make sure there are enough existing inventory of the donation of the same
    type.
    """

    def is_valid(self):
        if not super().is_valid():
            return False

        quantity = self.cleaned_data["quantity"]
        date: datetime.date = self.cleaned_data["date"]

        if quantity <= 0:
            self.add_error("quantity", "The given quantity has to be larger than 0")
            return False

        # Check inventory at current distribution date.
        inventory = get_inventory(self.cleaned_data["type"].name, date)

        if inventory < quantity:
            self.add_error(
                "quantity", "The distribution quantity can't exceed inventory limit."
            )
            return False

        # Check if the new distribution would affect any existing future
        # invetory.
        future_donation_list = list(
            Donation.objects.order_by("-date").filter(
                donation_type__name=self.cleaned_data["type"].name,
                date__gt=date,
            )
        )
        future_distribution_list = list(
            DonationDistribution.objects.order_by("-date").filter(
                type__name=self.cleaned_data["type"].name,
                date__gt=date,
            )
        )

        while len(future_distribution_list) > 0 and len(future_donation_list) > 0:
            # Process distribution with the oldest date.
            if future_distribution_list[-1].date < future_donation_list[-1].date:
                inventory -= future_distribution_list.pop().quantity
                if inventory < quantity:
                    self.add_error(
                        "quantity",
                        "The distribution quantity can't exceed inventory limit.",
                    )
                    return False
            # Process donation with the oldest date.
            else:
                inventory += future_donation_list.pop().quantity
        # Process the rest of either list.
        while len(future_distribution_list) > 0:
            inventory -= future_distribution_list.pop().quantity
            if inventory < quantity:
                self.add_error(
                    "quantity",
                    "The distribution quantity can't exceed inventory limit.",
                )
                return False
        while len(future_donation_list) > 0:
            inventory += future_donation_list.pop().quantity
        return True

    class Meta:
        model = DonationDistribution
        fields = ["type", "quantity", "date"]
