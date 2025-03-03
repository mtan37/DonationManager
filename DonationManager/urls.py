"""
URL configuration for DonationManager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from donations import views

urlpatterns = [
    path("", views.DonationView.as_view(), name="home"),
    path("donation/", views.DonationView.as_view(), name="donations"),
    path(
        "update_donation/<int:pk>/'",
        views.DonationUpdateView.as_view(),
        name="donation_update",
    ),
    path(
        "add_donation/<int:donor_id>/",
        views.DonationCreateView.as_view(),
        name="donation_creation",
    ),
    path(
        "donor/",
        views.DonorSelectView.as_view(),
        {"select_donor": False},
        name="donors",
    ),
    path(
        "select_donor/",
        views.DonorSelectView.as_view(),
        {"select_donor": True},
        name="select_donor",
    ),
    path(
        "update_donor/<int:pk>/", views.DonorUpdateView.as_view(), name="donor_update"
    ),
    path("add_donor/", views.DonorCreateView.as_view(), name="donor_creation"),
    path(
        "add_donation_type",
        views.DonationTypeCreateView.as_view(),
        name="add_donation_type",
    ),
    path(
        "distribution/", views.DonationDistributionView.as_view(), name="distributions"
    ),
    path(
        "add_donation_distribution/",
        views.DonationDistributionCreateView.as_view(),
        name="add_donation_distribution",
    ),
    path("inventory/", views.InventoryView.as_view(), name="inventory"),
    path("admin/", admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
