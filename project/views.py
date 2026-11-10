from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Parcel

# Create your views here.

def home(request):
    return render(request, "home.html")

def parcel_list(request):
    tracking_number = request.GET.get('tracking_number')
    if tracking_number:
        parcels = Parcel.objects.filter(tracking_number__icontains=tracking_number)
    else:
        parcels = Parcel.objects.all()
    return render(request, "parcel_list.html", {"parcels": parcels})

def parcel_detail(request, parcel_id):
    try:
        parcel = Parcel.objects.get(id=parcel_id)
    except Parcel.DoesNotExist:
        return HttpResponse("Parcel not found", status=404)
    return render(request, "parcel_detail.html", {"parcel": parcel})