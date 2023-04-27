from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('form/<event_name>', views.registration, name='registration'),
    path('registered/<enc>', views.registered, name='registered')
]
