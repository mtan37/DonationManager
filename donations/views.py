from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from datetime import datetime
from django.contrib.admin.widgets import AdminDateWidget

from donations.forms import DonationDistributionCreateForm, get_inventory
from donations.models import Donation, DonationType, Donor, DonationDistribution


class DonationView(generic.ListView):
    model = Donation
    template_name = "donations.html"

    def get_queryset(self):
        return Donation.objects.all()


class DonationCreateView(CreateView):
    template_name = "donation_create.html"
    model = Donation
    fields = ["donation_type", "quantity", "date", "note"]
    success_url = "/donation"
    donor_obj = None
    donor_name = ""

    def get_form(self, *args, **kwargs):
        form = super(DonationCreateView, self).get_form(*args, **kwargs)
        form.fields["note"].required = False
        form.fields["date"].widget = AdminDateWidget(attrs={"type": "date"})
        return form

    def get_context_data(self, **kwargs):
        context = super(DonationCreateView, self).get_context_data(**kwargs)
        self.donor_obj = get_object_or_404(Donor, pk=self.kwargs["donor_id"])
        self.donor_name = self.donor_obj.name
        return context

    def form_valid(self, form):
        self.donor_obj = get_object_or_404(Donor, pk=self.kwargs["donor_id"])
        form.instance.donor = self.donor_obj
        return super().form_valid(form)


class DonationUpdateView(UpdateView):
    template_name = "donation_update.html"
    model = Donation
    fields = ["donation_type", "donor", "quantity", "date", "note"]
    success_url = "/donation"


class DonorSelectView(generic.ListView):
    model = Donor
    template_name = "donor_select.html"

    def get_queryset(self):
        return Donor.objects.all()

    def get_context_data(self, **kwargs):
        context = super(DonorSelectView, self).get_context_data(**kwargs)
        self.select_donor = self.kwargs["select_donor"]
        return context


class DonorCreateView(CreateView):
    template_name = "donor_create.html"
    model = Donor
    fields = ["name", "address", "email"]
    success_url = "/donor"


class DonorUpdateView(UpdateView):
    template_name = "donor_update.html"
    model = Donor
    fields = ["name", "address", "email"]
    success_url = "/donor"


class DonationTypeCreateView(CreateView):
    template_name = "donation_type_create.html"
    model = DonationType
    fields = ["name"]
    success_url = "/donation"


class DonationDistributionView(generic.ListView):
    model = DonationDistribution
    template_name = "distributions.html"

    def get_queryset(self):
        return DonationDistribution.objects.all()


class DonationDistributionCreateView(CreateView):
    template_name = "distribution_create.html"
    form_class = DonationDistributionCreateForm
    success_url = "/distribution"

    def get_form(self, *args, **kwargs):
        form = super(DonationDistributionCreateView, self).get_form(*args, **kwargs)
        form.fields["date"].widget = AdminDateWidget(attrs={"type": "date"})
        return form


class InventoryView(TemplateView):
    template_name = "inventories.html"

    class Inventory:
        def __init__(self, type, quantity):
            self.type = type
            self.quantity = quantity

        type: str = ""
        quantity: int = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["inventory_list"] = []

        for donation_type in DonationType.objects.all():
            inv = InventoryView.Inventory(
                donation_type.name,
                get_inventory(donation_type.name, datetime.now().date()),
            )
            context["inventory_list"].append(inv)
        return context
