from django import forms
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from .models import NetworkMonitorDB
from .thread_ping import *


class NewUrlForm(forms.Form):
    name = forms.CharField(
        label="ชื่อเว็บไซต์",
        widget=forms.TextInput(attrs={"class": "input input-bordered"}),
    )
    url = forms.URLField(
        label="URL", widget=forms.TextInput(attrs={"class": "input input-bordered"})
    )
    status = forms.CharField(
        label="สถานะ",
        widget=forms.TextInput(attrs={"class": "input input-bordered"}),
        required=False,
    )
class UpdateUrlForm(forms.Form):
    name_update = forms.CharField(
        label="ชื่อเว็บไซต์",
        widget=forms.TextInput(attrs={"class": "input input-bordered"}),
    )
    url_update = forms.URLField(
        label="URL", widget=forms.TextInput(attrs={"class": "input input-bordered"})
    )
    status_update = forms.CharField(
        label="สถานะ",
        widget=forms.TextInput(attrs={"class": "input input-bordered"}),
        required=False,disabled=True
    )


def index(req):
    return render(
        req,
        "network_monitor/index.html",
        {"network_monitor": NetworkMonitorDB.objects.all(), "form": NewUrlForm(),"form_update":UpdateUrlForm()},
    )


def remove_data(request,id):
    try:
        NetworkMonitorDB.objects.get(id=id).delete()
        return redirect("network_monitor:index")
    except ObjectDoesNotExist:
        return redirect("network_monitor:index")


def add_data(req):
    if req.method == "POST":
        form = NewUrlForm(req.POST)
        if form.is_valid():
            NetworkMonitorDB.objects.create(
                name=form.cleaned_data["name"],
                url=form.cleaned_data["url"],
                status="400"
                if form.cleaned_data["status"] == ""
                else form.cleaned_data["status"],
            )
            return redirect("network_monitor:index")

    return render(
        req,
        "network_monitor/index.html",
        {"network_monitor": NetworkMonitorDB.objects.all(), "form": form},
    )

def table_data_view(request):
    # Query the database or any other data source to get the updated table data
    entries = NetworkMonitorDB.objects.all()

    # Format the data as a list of dictionaries containing the required fields
    data = [
        {
            'id': entry.id,
            'status': entry.status,
            'latency': entry.latency,
        }
        for entry in entries
    ]

    # Return the data as a JSON response
    return JsonResponse(data, safe=False)

def update_data(req,id):
    if req.method == "POST":
        form = UpdateUrlForm(req.POST)
        if form.is_valid():
            entry = NetworkMonitorDB.objects.get(id=id)
            entry.name = form.cleaned_data["name_update"]
            entry.url = form.cleaned_data["url_update"]
            entry.save()
            return redirect("network_monitor:index")
    else:
        entry = NetworkMonitorDB.objects.get(id=id)
        try:
            return JsonResponse({"name":entry.name,"url":entry.url,"status":entry.status})
        except ObjectDoesNotExist:
            return redirect("network_monitor:index")
