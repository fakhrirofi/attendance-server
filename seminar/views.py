from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'seminar/index.html')

def registration(request):
    return render(request, 'seminar/registration.html')