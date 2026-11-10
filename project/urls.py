from django.urls import path

from . import views


app_name = "project"

urlpatterns = [
    path("", views.home, name="home"),
    path("parcels/", views.parcel_list, name="parcel_list"),
    path("parcels/<int:parcel_id>/", views.parcel_detail, name="parcel_detail"),
]