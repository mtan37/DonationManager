from .forms import ContactForm
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView, UpdateView
from donations.models import Donation, Donor
from django.shortcuts import get_object_or_404
from django.views import generic


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

    def get_context_data(self, **kwargs):
        context = super(DonationCreateView, self).get_context_data(**kwargs)
        self.donor_obj = get_object_or_404(Donor, pk=self.kwargs["donor_id"])
        self.donor_name = self.donor_obj.name
        context["donor"] = self.kwargs["donor_id"]
        return context


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
